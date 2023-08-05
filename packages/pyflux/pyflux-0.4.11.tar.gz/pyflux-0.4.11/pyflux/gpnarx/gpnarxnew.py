import sys
if sys.version_info < (3,):
    range = xrange

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.stats as ss
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import seaborn as sns

from .. import arma
from .. import inference as ifr
from .. import distributions as dst
from .. import output as op
from .. import tests as tst
from .. import tsm as tsm
from .. import data_check as dc

from .kernels import *

class GPNARX(tsm.TSM):
    """ Inherits time series methods from TSM class.

    **** GAUSSIAN PROCESS NONLINEAR AUTOREGRESSIVE (GP-NARX) MODELS ****

    Parameters
    ----------
    data : pd.DataFrame or np.array
        Field to specify the time series data that will be used.

    ar : int
        Field to specify how many AR terms the model will have.

    kernel_type : GP kernel object
        E.g. SquaredExponential()

    integ : int (default : 0)
        Specifies how many time to difference the time series.

    target : str (pd.DataFrame) or int (np.array)
        Specifies which column name or array index to use. By default, first
        column/array will be selected as the dependent variable.

    conjugate_gradient : Boolean
        Whether to use CG for approximate inverse; if False, use Cholesky decomposition
    """

    def __init__(self,data,ar,kernel_type=None,integ=0,target=None,conjugate_gradient=True):

        # Initialize TSM object
        super(GPNARX,self).__init__('GPNARX')

        # Latent Variables
        self.ar = ar
        self.integ = integ
        self.max_lag = self.ar
        self.model_name = 'GPNARX(' + str(self.ar) + ')'
        self._z_hide = 0 # Whether to cutoff variance latent variables from results
        self.supported_methods = ["MLE","PML","Laplace","M-H","BBVI"]
        self.default_method = "MLE"     
        self.kernel_type = kernel_type
        self.multivariate_model = False
        self.conjugate_gradient = True

        # Format the data
        self.data, self.data_name, self.is_pandas, self.index = dc.data_check(data,target)
        self.data_original = self.data.copy()

        # Difference data
        for order in range(self.integ):
            self.data = np.diff(self.data)
            self.data_name = "Differenced " + self.data_name
        self.index = self.index[self.integ:len(self.index)]

        # Apply normalization
        self.data_full = self.data.copy()       
        self.data = np.array(self.data_full[self.max_lag:self.data_full.shape[0]]) # adjust for lags
        self._norm_mean = np.mean(self.data)
        self._norm_std = np.std(self.data)  
        self.data = (self.data - self._norm_mean) / self._norm_std
        self.data_full = (self.data_full - self._norm_mean) / self._norm_std

        # Create kernel instance
        self.kernel = self.kernel_type(self.X())

        # Create latent variables
        self._create_latent_variables()

    def _alpha(self,L):
        """ Covariance-derived term to construct expectations. See Rasmussen & Williams.

        Latent variables
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        The alpha matrix/vector
        """     

        return np.linalg.solve(np.transpose(L),np.linalg.solve(L,np.transpose(self.data)))

    def _alpha_cg(self,beta):
        parm = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])
        return sp.linalg.cg(self.kernel.K(parm[1:]),np.transpose(self.data))[0]

    def _construct_predict(self,beta,h):    
        """ Creates h-step ahead forecasts for the Gaussian process

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        h: int
            How many steps ahead to forecast

        Returns
        ----------
        - predictions
        - variance of predictions
        """             

        # Refactor this entire code
        Xstart = self.X().copy()
        Xstart = [i for i in Xstart]
        predictions = np.zeros(h)
        variances = np.zeros(h)

        for step in range(0,h):
            Xstar = []

            for lag in range(0,self.max_lag):
                if lag == 0:
                    if step == 0:
                        Xstar.append([self.data[-1]])
                        Xstart[0] = np.append(Xstart[0],self.data[-1])
                    else:
                        Xstar.append([predictions[step-1]])
                        Xstart[0] = np.append(Xstart[0],predictions[step-1])
                else:
                    Xstar.append([Xstart[lag-1][-2]])
                    Xstart[lag] = np.append(Xstart[lag],Xstart[lag-1][-2])

            Kstar = self.kernel.Kstar(beta[1:],np.transpose(np.array(Xstar)))

            if self.conjugate_gradient is True:
                alpha = self._alpha_cg(beta)
            else:
                L = self._L(beta)
                alpha = self._alpha(L)

            predictions[step] = np.dot(np.transpose(Kstar), alpha)
            variances[step] = self.kernel.Kstarstar(beta[1:],np.transpose(np.array(Xstar))) 
            - np.dot(np.dot(np.transpose(self.kernel.Kstar(beta[1:],np.transpose(np.array(Xstar)))),
                np.linalg.pinv(self.kernel.K(beta[1:]) + np.identity(self.kernel.K(beta[1:]).shape[0])*self.latent_variables.z_list[0].prior.transform(beta[0]))),
                self.kernel.Kstar(beta[1:], np.transpose(np.array(Xstar)))) + self.latent_variables.z_list[0].prior.transform(beta[0])  

        return predictions, variances, predictions - 1.98*np.power(variances,0.5), predictions + 1.98*np.power(variances,0.5)

    def _create_latent_variables(self):
        """ Creates model latent variables

        Returns
        ----------
        None (changes model attributes)
        """

        # Create latent variables
        for no, i in enumerate(self.kernel.build_latent_variables()):
            self.latent_variables.add_z(i[0],i[1],i[2])
            self.latent_variables.z_list[no].start = i[3]

        self.z_no = len(self.kernel.build_latent_variables())

        arma_start = arma.ARIMA(self.data,ar=self.ar,ma=0,integ=self.integ)
        x = arma_start.fit()
        arma_starting_values = arma_start.latent_variables.get_z_values()
        self.latent_variables.z_list[0].start = np.log(np.exp(np.power(arma_starting_values[-1],2)))

        """
        else:
            self.latent_variables.add_z('l',ifr.Uniform(transform='exp'),dst.q_Normal(0,3))

            if self.kernel_type == 'SE':
                self.kernel = SquaredExponential(self.X(),1,1)
            elif self.kernel_type == 'OU':
                self.kernel = OrnsteinUhlenbeck(self.X(),1,1)
            elif self.kernel_type == 'Periodic':
                self.kernel = Periodic(self.X(),1,1)
            elif self.kernel_type == 'RQ':
                self.latent_variables.add_z('alpha',ifr.Uniform(transform='exp'),dst.q_Normal(0,3))
                self.kernel = RationalQuadratic(self.X(),1,1,1)

        """

    def _L(self,beta):
        """ Creates cholesky decomposition of covariance matrix

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent_variables

        Returns
        ----------
        The cholesky decomposition (L) of K
        """ 
        return np.linalg.cholesky(self.kernel.K(beta[1:])) + np.identity(self.data.shape[0])*self.latent_variables.z_list[0].prior.transform(beta[0])

    def X(self):
        """ Creates design matrix of variables to use in GP regression

        Returns
        ----------
        The design matrix
        """     

        for i in range(0,self.ar):
            datapoint = self.data_full[(self.max_lag-i-1):-i-1]         
            if i==0:
                X = datapoint
            else:
                X = np.vstack((X,datapoint))
        return X

    def expected_values(self,beta):
        """ Expected values of the function given the covariance matrix and hyperparameters

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        The expected values of the function
        """     
        parm = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])
        
        if self.conjugate_gradient is True:
            alpha = self._alpha_cg(beta)
            return np.dot(np.transpose(self.kernel.K(parm[1:])),alpha)
        else:
            L = self._L(parm)
            return np.dot(np.transpose(self.kernel.K(parm[1:])),self._alpha(L))

    def variance_values(self,beta):
        """ Covariance matrix for the estimated function

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for parameters

        Returns
        ----------
        Covariance matrix for the estimated function 
        """     
        parm = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])
        return self.kernel.K(parm[1:]) - np.dot(np.dot(np.transpose(self.kernel.K(parm[1:])),np.linalg.pinv(self.kernel.K(parm[1:]) + np.identity(self.kernel.K(parm[1:]).shape[0])*self.latent_variables.z_list[0].prior.transform(beta[0]))),self.kernel.K(parm[1:])) + self.latent_variables.z_list[0].prior.transform(beta[0])

    def neg_loglik(self,beta):
        """ Creates the negative log marginal likelihood of the model

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        The negative log marginal logliklihood of the model
        """             
        parm = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])
        
        if self.conjugate_gradient is True:
            alpha = self._alpha_cg(beta)
            return -(-0.5*(np.dot(np.transpose(self.data),alpha)) - 0.5*np.linalg.slogdet(self.kernel.K(parm[1:]))[1] - (self.data.shape[0]/2)*np.log(2*np.pi))
        else:
            L = self._L(parm)
            return -(-0.5*(np.dot(np.transpose(self.data),self._alpha(L))) - np.trace(np.log(np.diag(L))) - (self.data.shape[0]/2)*np.log(2*np.pi))

    def plot_fit(self,intervals=True,**kwargs):
        """ Plots the fit of the Gaussian process model to the data

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        intervals : Boolean
            Whether to plot uncertainty intervals or not

        Returns
        ----------
        None (plots the fit of the function)
        """

        figsize = kwargs.get('figsize',(10,7))

        date_index = self.index[self.max_lag:]
        expectation = self.expected_values(self.latent_variables.get_z_values())
        posterior = multivariate_normal(expectation,self.variance_values(self.latent_variables.get_z_values()),allow_singular=True)
        simulations = 500
        sim_vector = np.zeros([simulations,len(expectation)])

        for i in range(simulations):
            sim_vector[i] = posterior.rvs()

        error_bars = []
        for pre in range(5,100,5):
            error_bars.append([(np.percentile(i,pre)*self._norm_std + self._norm_mean) for i in sim_vector.transpose()] 
                - (expectation*self._norm_std + self._norm_mean))

        plt.figure(figsize=figsize) 

        plt.subplot(2, 2, 1)
        plt.title(self.data_name + " Raw")  
        plt.plot(date_index,self.data*self._norm_std + self._norm_mean,'k')

        plt.subplot(2, 2, 2)
        plt.title(self.data_name + " Raw and Expected") 
        plt.plot(date_index,self.data*self._norm_std + self._norm_mean,'k',alpha=0.2)
        plt.plot(date_index,self.expected_values(self.latent_variables.get_z_values())*self._norm_std + self._norm_mean,'b')

        plt.subplot(2, 2, 3)
        plt.title(self.data_name + " Raw and Expected (with intervals)")    

        if intervals == True:
            alpha =[0.15*i/float(100) for i in range(50,12,-2)]
            for count, pre in enumerate(error_bars):
                plt.fill_between(date_index, (expectation*self._norm_std + self._norm_mean)-pre, 
                    (expectation*self._norm_std + self._norm_mean)+pre,alpha=alpha[count])      

        plt.plot(date_index,self.data*self._norm_std + self._norm_mean,'k',alpha=0.2)
        plt.plot(date_index,self.expected_values(self.latent_variables.get_z_values())*self._norm_std + self._norm_mean,'b')

        plt.subplot(2, 2, 4)

        plt.title("Expected " + self.data_name + " (with intervals)")   

        if intervals == True:
            alpha =[0.15*i/float(100) for i in range(50,12,-2)]
            for count, pre in enumerate(error_bars):
                plt.fill_between(date_index, (expectation*self._norm_std + self._norm_mean)-pre, 
                    (expectation*self._norm_std + self._norm_mean)+pre,alpha=alpha[count])      

        plt.plot(date_index,self.expected_values(self.latent_variables.get_z_values())*self._norm_std + self._norm_mean,'b')

        plt.show()

    def plot_predict(self,h=5,past_values=20,intervals=True,**kwargs):

        """ Plots forecast with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps ahead would you like to forecast?

        past_values : int (default : 20)
            How many past observations to show on the forecast graph?

        intervals : Boolean
            Would you like to show 95% prediction intervals for the forecast?

        Returns
        ----------
        - Plot of the forecast
        - Error bars, forecasted_values, plot_values, plot_index
        """     

        figsize = kwargs.get('figsize',(10,7))

        if self.latent_variables.estimated is False:
            raise Exception("No latent variables estimated!")
        else:

            predictions, variance, lower, upper = self._construct_predict(self.latent_variables.get_z_values(),h) 
            full_predictions = np.append(self.data,predictions)
            full_lower = np.append(self.data,lower)
            full_upper = np.append(self.data,upper)
            date_index = self.shift_dates(h)

            # Plot values (how far to look back)
            plot_values = full_predictions[-h-past_values:]*self._norm_std + self._norm_mean
            plot_index = date_index[-h-past_values:]

            # Lower and upper intervals
            lower = np.append(full_predictions[-h-1],lower)
            upper = np.append(full_predictions[-h-1],upper)

            plt.figure(figsize=figsize)
            if intervals == True:
                plt.fill_between(date_index[-h-1:], 
                    lower*self._norm_std + self._norm_mean, 
                    upper*self._norm_std + self._norm_mean,
                    alpha=0.2)          
            
            plt.plot(plot_index,plot_values)
            plt.title("Forecast for " + self.data_name)
            plt.xlabel("Time")
            plt.ylabel(self.data_name)
            plt.show()

    def predict_is(self,h=5):
        """ Makes dynamic in-sample predictions with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps would you like to forecast?

        Returns
        ----------
        - pd.DataFrame with predicted values
        """     

        predictions = []

        for t in range(0,h):
            x = GPNARX(ar=self.ar,kernel_type=self.kernel_type,integ=self.integ,data=self.data_original[:-h+t])
            if t == 0:
                x.fit(printer=False)
                predictions = x.predict(1)  
            else:
                x.fit(printer=False)
                predictions = pd.concat([predictions,x.predict(1)])

        predictions.rename(columns={0:self.data_name}, inplace=True)
        predictions.index = self.index[-h:]

        return predictions

    def plot_predict_is(self,h=5,**kwargs):
        """ Plots forecasts with the estimated model against data
            (Simulated prediction with data)

        Parameters
        ----------
        h : int (default : 5)
            How many steps to forecast

        Returns
        ----------
        - Plot of the forecast against data 
        """     

        figsize = kwargs.get('figsize',(10,7))

        plt.figure(figsize=figsize)
        date_index = self.index[-h:]
        predictions = self.predict_is(h)
        data = self.data[-h:]

        plt.plot(date_index,data*self._norm_std + self._norm_mean,label='Data')
        plt.plot(date_index,predictions,label='Predictions',c='black')
        plt.title(self.data_name)
        plt.legend(loc=2)   
        plt.show()          

    def predict(self,h=5):
        """ Makes forecast with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps ahead would you like to forecast?

        Returns
        ----------
        - pd.DataFrame with predicted values
        """     

        if self.latent_variables.estimated is False:
            raise Exception("No latent variables estimated!")
        else:

            predictions, _, _, _ = self._construct_predict(self.latent_variables.get_z_values(),h)    
            predictions = predictions*self._norm_std + self._norm_mean  
            date_index = self.shift_dates(h)
            result = pd.DataFrame(predictions)
            result.rename(columns={0:self.data_name}, inplace=True)
            result.index = date_index[-h:]

            return result