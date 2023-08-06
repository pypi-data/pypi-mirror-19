import sys
if sys.version_info < (3,):
    range = xrange

import numpy as np
import pandas as pd
import scipy.stats as ss
import scipy.special as sp

from .. import families as fam
from .. import tsm as tsm
from .. import data_check as dc

from .scores import *

from .gas_core_recursions import gas_recursion

class DoubleGASRank(tsm.TSM):
    """ Inherits time series methods from TSM class.

    **** GENERALIZED AUTOREGRESSIVE SCORE (GAS) RANK MODELS ****

    Parameters
    ----------
    data : pd.DataFrame
        Field to specify the univariate time series data that will be used.

    team_1 : str (pd.DataFrame)        
        Specifies which column contains the home team

    team_2 : str (pd.DataFrame)        
        Specifies which column contains the away team

    family : GAS family object
        Which distribution to use, e.g. GASNormal()

    score_diff : str (pd.DataFrame)        
        Specifies which column contains the score

    gradient_only : Boolean (default: True)
        If true, will only use gradient rather than second-order terms
        to construct the modified score.
    """

    def __init__(self, data, team_1, team_2, family, team_1_score, team_2_score, gradient_only=False):

        # Initialize TSM object     
        super(DoubleGASRank,self).__init__('DoubleGASRank')

        self.gradient_only = gradient_only
        self.z_no = 2
        self.max_lag = 0
        self._z_hide = 0 # Whether to cutoff variance latent variables from results
        self.supported_methods = ["MLE","PML","Laplace","M-H","BBVI"]
        self.default_method = "MLE"
        self.multivariate_model = False

        self.home_id, self.away_id = self._create_ids(data[team_1].values,data[team_2].values)
        self.team_strings = sorted(list(set(np.append(data[team_1].values,data[team_2].values))))
        self.team_dict = dict(zip(self.team_strings, range(len(self.team_strings))))
        self.home_count, self.away_count = self._match_count()
        self.max_team = max(np.max(self.home_id),np.max(self.away_id))
        self.original_dataframe = data
        self.data_1, self.data_name_1, self.is_pandas, self.index = dc.data_check(data, team_1_score)
        self.data_2, self.data_name_2, _, _ = dc.data_check(data, team_1_score)

        self.data_1_original = self.data_1.copy()
        self.data_1_length = self.data_1.shape[0]
        self.data_2_original = self.data_2.copy()
        self.data_2_length = self.data_2.shape[0]
        self.data_name = self.data_name_1 + ', ' + self.data_name_2
        self._create_latent_variables()

        self.family = family
        
        self.model_name2, self.link, self.scale, self.shape, self.skewness, self.mean_transform, _ = self.family.setup()
        self.model_name = self.model_name2 + "GAS Rank "

        for no, i in enumerate(self.family.build_latent_variables()):
            self.latent_variables.add_z(i[0],i[1],i[2])
            self.latent_variables.z_list[2+no].start = i[3]
        self.latent_variables.z_list[0].start = self.mean_transform(np.mean(self.data_1))
        self.latent_variables.z_list[1].start = self.mean_transform(np.mean(self.data_2))
        self.latent_variables.z_list[2].start = -7.0
        self.latent_variables.z_list[3].start = -7.0
        
        self._model = self._model_one_components

        self.family_z_no = len(self.family.build_latent_variables())
        self.z_no = len(self.latent_variables.z_list)

    def _create_ids(self, home_teams, away_teams):
        """
        Creates IDs for both players/teams
        """
        categories = pd.Categorical(np.append(home_teams,away_teams))
        home_id, away_id = categories.codes[0:int(len(categories)/2)], categories.codes[int(len(categories)/2):len(categories)+1]
        return home_id, away_id

    def _match_count(self):
        home_count, away_count = np.zeros(len(self.home_id)), np.zeros(len(self.away_id))

        for t in range(0,len(home_count)):
            home_count[t] = len(self.home_id[0:t+1][self.home_id[0:t+1]==self.home_id[t]]) + len(self.away_id[0:t+1][self.away_id[0:t+1]==self.home_id[t]]) 
            away_count[t] = len(self.home_id[0:t+1][self.home_id[0:t+1]==self.away_id[t]]) + len(self.away_id[0:t+1][self.away_id[0:t+1]==self.away_id[t]]) 

        return home_count, away_count       

    def _match_count_2(self):
        home_count, away_count = np.zeros(len(self.home_2_id)), np.zeros(len(self.away_2_id))

        for t in range(0,len(home_count)):
            home_count[t] = len(self.home_2_id[0:t+1][self.home_2_id[0:t+1]==self.home_2_id[t]]) + len(self.away_2_id[0:t+1][self.away_2_id[0:t+1]==self.home_2_id[t]]) 
            away_count[t] = len(self.home_2_id[0:t+1][self.home_2_id[0:t+1]==self.away_2_id[t]]) + len(self.away_2_id[0:t+1][self.away_2_id[0:t+1]==self.away_2_id[t]]) 

        return home_count, away_count       

    def _create_latent_variables(self):
        """ Creates model latent variables

        Returns
        ----------
        None (changes model attributes)
        """

        self.latent_variables.add_z('Constant 1', fam.Normal(0,10,transform=None), fam.Normal(0,3))
        self.latent_variables.add_z('Constant 2', fam.Normal(0,10,transform=None), fam.Normal(0,3))
        self.latent_variables.add_z('Attack Ability Scale', fam.Normal(0,1,transform=None), fam.Normal(0,3))
        self.latent_variables.add_z('Defence Ability Scale', fam.Normal(0,1,transform=None), fam.Normal(0,3))

    def _get_scale_and_shape(self,parm):
        """ Obtains appropriate model scale and shape latent variables

        Parameters
        ----------
        parm : np.array
            Transformed latent variable vector

        Returns
        ----------
        None (changes model attributes)
        """

        if self.scale is True:
            if self.shape is True:
                model_shape = parm[-1]  
                model_scale = parm[-2]
            else:
                model_shape = 0
                model_scale = parm[-1]
        else:
            model_scale = 0
            model_shape = 0 

        if self.skewness is True:
            model_skewness = parm[-3]
        else:
            model_skewness = 0

        return model_scale, model_shape, model_skewness

    def _get_scale_and_shape_sim(self, transformed_lvs):
        """ Obtains model scale, shape, skewness latent variables for
        a 2d array of simulations.

        Parameters
        ----------
        transformed_lvs : np.array
            Transformed latent variable vector (2d - with draws of each variable)

        Returns
        ----------
        - Tuple of np.arrays (each being scale, shape and skewness draws)
        """

        if self.scale is True:
            if self.shape is True:
                model_shape = self.latent_variables.z_list[-1].prior.transform(transformed_lvs[-1, :]) 
                model_scale = self.latent_variables.z_list[-2].prior.transform(transformed_lvs[-2, :])
            else:
                model_shape = np.zeros(transformed_lvs.shape[1])
                model_scale = self.latent_variables.z_list[-1].prior.transform(transformed_lvs[-1, :])
        else:
            model_scale = np.zeros(transformed_lvs.shape[1])
            model_shape = np.zeros(transformed_lvs.shape[1])

        if self.skewness is True:
            model_skewness = self.latent_variables.z_list[-3].prior.transform(transformed_lvs[-3, :])
        else:
            model_skewness = np.zeros(transformed_lvs.shape[1])

        return model_scale, model_shape, model_skewness

    def _model_one_components(self,beta):
        """ Creates the structure of the model

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        theta : np.array
            Contains the predicted values for the time series

        Y : np.array
            Contains the length-adjusted time series (accounting for lags)

        scores : np.array
            Contains the scores for the time series
        """

        parm = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])
        scale, shape, skewness = self._get_scale_and_shape(parm)
        attack_state_vectors = np.zeros(shape=(self.max_team+1))
        defence_state_vectors = np.zeros(shape=(self.max_team+1))
        theta_1 = np.zeros(shape=(self.data_1.shape[0]))
        theta_2 = np.zeros(shape=(self.data_1.shape[0]))

        for t in range(0,self.data_1.shape[0]):
            theta_1[t] = parm[0] + attack_state_vectors[self.home_id[t]] - defence_state_vectors[self.away_id[t]]
            theta_2[t] = parm[1] + attack_state_vectors[self.away_id[t]] - defence_state_vectors[self.home_id[t]]

            attack_state_vectors[self.home_id[t]] += np.exp(parm[2])*self.family.score_function(self.data_1[t], self.link(theta_1[t]), scale, shape, skewness)
            defence_state_vectors[self.away_id[t]] += -np.exp(parm[3])*self.family.score_function(self.data_1[t], self.link(theta_1[t]), scale, shape, skewness)
            
            attack_state_vectors[self.away_id[t]] += np.exp(parm[2])*self.family.score_function(self.data_2[t], self.link(theta_2[t]), scale, shape, skewness)
            defence_state_vectors[self.home_id[t]] += -np.exp(parm[3])*self.family.score_function(self.data_2[t], self.link(theta_2[t]), scale, shape, skewness)

        return theta_1, theta_2, self.data_1, self.data_2, attack_state_vectors, defence_state_vectors

    def neg_loglik(self, beta):
        theta_1, theta_2, Y_1, Y_2, _, _ = self._model(beta)
        parm = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])
        model_scale, model_shape, model_skewness = self._get_scale_and_shape(parm)
        return self.family.neg_loglikelihood(Y_1,self.link(theta_1),model_scale,model_shape,model_skewness) + self.family.neg_loglikelihood(Y_2,self.link(theta_2),model_scale,model_shape,model_skewness)
