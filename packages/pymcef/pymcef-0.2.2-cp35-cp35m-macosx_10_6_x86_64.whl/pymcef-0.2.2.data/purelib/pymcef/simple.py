from __future__ import print_function

import numpy as np
from pymcef import ppslp

__all__ = ['SimpleEF', 'RiskMeasure']

def _get_portfolio(port):
    prt = {}
    prt['weight'] = port.Weights().asdict()
    prt['risk'] = port.Risk()
    prt['reward'] = port.Reward()
    prt['Omega'] = port.Omega()
    prt['sd'] = port.Sd()
    prt['Sharpe'] = port.Sharpe()
    prt['lambda_l'] = port.Lambda_lower()
    prt['lambda_u'] = port.Lambda_upper()
    return prt

def _check_kwargs(kwargs, supported):
    for arg_name in kwargs.keys():
        if arg_name not in supported:
            raise TypeError(arg_name+" is a invalid keyword argument for this function")

class RiskMeasure:
    AbsoluteSemiDeviation, FixTargetUnderPerformance = range(2)

class SimpleEF:
    def __init__(self, **kwargs):
        kws = ['risk_measure', 'target_return', 'training_set', 'validation_set', 'asset_names']
        _check_kwargs(kwargs, kws)
        if 'training_set' not in kwargs:
            raise TypeError("required keyword argument training_set missing")
        self.training_set = kwargs['training_set']
        if 'asset_names' in kwargs:
            self.asset_names = kwargs['asset_names']
        else:
            self.asset_names = ['asset '+str(i) for i in range(self.training_set.shape[0])]
        if len(self.asset_names) != self.training_set.shape[0]:
            raise ValueError("Dimension of input arguments mismatch")
        self.risk_measure = kwargs.get('risk_measure', RiskMeasure.AbsoluteSemiDeviation)
        self.target = kwargs.get('target_return', 0.0)
        if self.risk_measure == RiskMeasure.AbsoluteSemiDeviation:
            self.dic = ppslp.dictionary(self.training_set)
        elif self.risk_measure == RiskMeasure.FixTargetUnderPerformance:
            self.dic = ppslp.dictionary(self.training_set, self.target)
        else:
            raise ValueError("Unsupported Risk Measure enum value:" + str(self.risk_measure))
        self.dic.find_lambdalower_encol_entype()
        self.frontier_in_sample = []
        self.frontier_in_sample.append(_get_portfolio(self.dic.Current_portfolio()))
        while not self.dic.isentire():
            self.dic.find_lecol_then_pivot()
            self.dic.find_lambdalower_encol_entype()
            self.frontier_in_sample.append(_get_portfolio(self.dic.Current_portfolio()))
        self.frontier_in_sample.pop() # discard the last portfolio
        max_sharpe_port_index = self.dic.Max_sharpe_index()
        max_omega_port_index = self.dic.Max_omega_index()
        max_sharpe_port = _get_portfolio(self.dic.Max_sharpe_portfolio())
        max_omega_port = _get_portfolio(self.dic.Max_omega_portfolio())
        self.critical_port_in_sample = {}
        self.critical_port_in_sample['Max Sharpe'] = {'Index' : max_sharpe_port_index,
                                                      'Portfolio' : max_sharpe_port}
        self.critical_port_in_sample['Max Omega'] = {'Index' : max_omega_port_index,
                                                     'Portfolio' : max_omega_port}
        print("Sample efficient frontier contains " + \
              str(len(self.frontier_in_sample)) + " portfolios")
        print("Max Sharpe portfolio is the " + str(max_sharpe_port_index) + "th")
        #print("Max Omega portfolio is the " + str(max_sharpe_omega_index) + "th")
        if 'validation_set' in kwargs:
            self.validation_set = kwargs['validation_set']
            if self.validation_set.shape[0] != self.training_set.shape[0]:
                raise ValueError("training set and validation set have different number of assets")
            self.frontier_validation = []
            max_sharpe_index, max_sharpe = 0, 0.0
            counter = 0
            for port in self.frontier_in_sample:
                rewards = np.zeros(self.validation_set.shape[1])
                port_validation = {}
                for index, weight in port['weight'].items():
                    rewards += weight * self.validation_set[index]
                reward = np.mean(rewards)
                port_validation['returns'] = rewards
                port_validation['reward'] = reward
                port_validation['sd'] = np.std(rewards)
                port_validation['Sharpe'] = port_validation['reward'] / port_validation['sd']
                if port_validation['Sharpe'] > max_sharpe:
                    max_sharpe = port_validation['Sharpe']
                    max_sharpe_index = counter
                # out of sample absolute semi-deviation as risk
                port_validation['risk'] = np.sum(rewards[rewards > reward] - reward) / len(rewards)
                self.frontier_validation.append(port_validation)
                counter += 1
            self.critical_port_validation = {}
            self.critical_port_validation['Max Sharpe'] = \
              {'Index' : max_sharpe_index, 'Portfolio' : self.frontier_validation[max_sharpe_index]}
        else:
            self.validation_set = None
            self.frontier_validation = None
            self.critical_port_validation = None

