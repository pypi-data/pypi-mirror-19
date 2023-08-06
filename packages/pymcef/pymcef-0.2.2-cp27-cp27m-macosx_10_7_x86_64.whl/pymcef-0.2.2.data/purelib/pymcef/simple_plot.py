from copy import deepcopy
from operator import itemgetter
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

import numpy as np
import matplotlib.pyplot as plt

from pymcef.simple import SimpleEF, RiskMeasure, _check_kwargs

plot_font = 'Bitstream Vera Sans'

def _compute_cvar(port, cvar_q, cvar_target):
    returns = port['returns']
    quantile = np.percentile(returns, cvar_q*100)
    cvar = np.mean(cvar_target - returns[returns < quantile])
    return cvar

class SimpleEFp(SimpleEF):
    def __init__(self, **kwargs):
        SimpleEF.__init__(self, **kwargs)

    def _get_axis_label_for_risk(self):
        if self.risk_measure == RiskMeasure.AbsoluteSemiDeviation:
            xlabel = 'In Sample Risk (absolute semi-deviation)'
        elif self.risk_measure == RiskMeasure.FixTargetUnderPerformance:
            xlabel = 'In Sample Risk (expected under-performance to target '+str(self.target)+')'
        else:
            raise ValueError("Unsupported Risk Measure enum value:" + str(self.risk_measure))
        return xlabel

    def plot_ef(self, tag='-', **kwargs):
        n = len(self.frontier_in_sample)
        xs = [self.frontier_in_sample[i]['risk'] for i in range(n)]
        ys = [self.frontier_in_sample[i]['reward'] for i in range(n)]
        port = self.critical_port_in_sample['Max Sharpe']['Portfolio']
        x = port['risk']
        y = port['reward']
        num_subplots = 1 if self.frontier_validation is None else 2
        fig = plt.figure(figsize=(6 * num_subplots, 4.5))
        ax = fig.add_subplot(1, num_subplots, 1)
        ax.plot(xs, ys, tag)
        ax.plot(x, y, 'r.')
        ax.text(x * 1.05, y, 'Max Sharpe ratio portfolio', fontsize=8)
        #xlabel = 'In Sample Risk (expected under-performance to target '+str(self.target)+')'
        xlabel = self._get_axis_label_for_risk()
        ax.set_xlabel(xlabel, fontname=plot_font)
        ax.set_ylabel('Reward(Mean return)', fontname=plot_font)
        ax.set_title('In sample efficient frontier', fontname=plot_font)
        if num_subplots == 2:
            _check_kwargs(kwargs, ['CVar_q'])
            cvar_q = kwargs.get('CVar_q', 0.05)
            xs = []
            for port in self.frontier_validation:
                xs.append(_compute_cvar(port, cvar_q, self.target))
            ys = [self.frontier_validation[i]['reward'] for i in range(n)]
            port = self.critical_port_validation['Max Sharpe']['Portfolio']
            x = _compute_cvar(port, cvar_q, self.target)
            y = port['reward']
            ax = fig.add_subplot(1, num_subplots, 2)
            ax.plot(xs, ys, tag)
            ax.plot(x, y, 'r.')
            ax.text(x * 1.05, y, 'Max Sharpe ratio portfolio', fontsize=8)
            ax.set_xlabel('CVar('+str(cvar_q)+')', fontname=plot_font)
            ax.set_ylabel('Reward(Mean return)', fontname=plot_font)
            ax.set_title('Validation efficient frontier', fontname=plot_font)
        return fig

    def plot_performance(self, tag='-', **kwargs):
        n = len(self.frontier_in_sample)
        xs = [self.frontier_in_sample[i]['lambda_l'] for i in range(n)]
        ys = [self.frontier_in_sample[i]['Sharpe'] for i in range(n)]
        num_subplots = 1 if self.frontier_validation is None else 2
        fig = plt.figure(figsize=(6*num_subplots, 4.5))
        ax = fig.add_subplot(1, num_subplots, 1)
        ax.plot(xs, ys, tag, label='In sample')
        if self.frontier_validation is not None:
            ys = [self.frontier_validation[i]['Sharpe'] for i in range(n)]
            ax.plot(xs, ys, tag, label='Validation')
        ax.set_xlabel('$\\lambda$', fontname=plot_font)
        ax.set_ylabel('Sharpe Ratio', fontname=plot_font)
        ax.legend(fontsize=10, handlelength=5, frameon=False)
        if self.frontier_validation is not None:
            ax = fig.add_subplot(1, num_subplots, 2)
            _check_kwargs(kwargs, ['CVar_q'])
            cvar_q = kwargs.get('CVar_q', 0.05)
            ys = []
            for port in self.frontier_validation:
                ys.append(port['reward']/_compute_cvar(port, cvar_q, self.target))
            ax.plot(xs, ys, tag)
            ax.set_xlabel('$\\lambda$', fontname=plot_font)
            ax.set_ylabel('Reward / Validation CVar('+str(cvar_q)+')', fontname=plot_font)
            ax.set_title('Performance in validation portfolios', fontsize=10)
        return fig

    def plot_weights(self, max_num_assets=20, tag='-'):
        fig = plt.figure(figsize=(6, 4.5))
        ax = fig.add_subplot(1, 1, 1)
        num_assets = 0
        weights_risk = Q.Queue(maxsize=len(self.frontier_in_sample))
        xs1 = []
        ys1 = []
        for port in self.frontier_in_sample:
            weights_risk.put((deepcopy(port['weight']), port['risk']))
            xs1.append(port['risk'])
            ys1.append(port['lambda_l'])
        while num_assets < max_num_assets and (not weights_risk.empty()):
            weights, risk = weights_risk.get()
            for k, v in sorted(weights.items(), key=itemgetter(1), reverse=True):
                ws = [v]
                rs = [risk]
                m = weights_risk.qsize() # single thread here, qsize is exact size
                for i in range(m): # pylint: disable=W0612
                    w, r = weights_risk.get()
                    rs.append(r)
                    if k in w:
                        ws.append(w[k])
                        del w[k]
                    else:
                        ws.append(0.0)
                    if len(w) > 0:
                        weights_risk.put((w, r))
                num_assets += 1
                ax.plot(rs, ws, tag)
                ax.text(rs[0]*0.95, ws[0]+0.02, self.asset_names[k],\
                        fontsize=6, horizontalalignment='right')
        port = self.critical_port_in_sample['Max Sharpe']['Portfolio']
        ax.axvline(x=port['risk'], ls='dotted', c='black')
        ax.text(port['risk'], 1.02, 'Max Sharpe ratio portfolio', fontsize=6)
        ys = list(port['weight'].values())
        xs = [port['risk']] * len(ys)
        ax.plot(xs, ys, '.k')
        xlabel = self._get_axis_label_for_risk()
        ax.set_xlabel(xlabel, fontname=plot_font)
        ax.set_ylabel('Weights', fontname=plot_font)
        ax1 = ax.twinx()
        ax1.plot(xs1, ys1, '--k', label='$\\lambda$', dashes=(12, 3))
        ax1.set_ylabel('$\\lambda$', fontname=plot_font)
        ax1.set_xlim(right=max(xs1))
        ax1.legend(loc='upper center', fontsize=10, handlelength=5, frameon=False)
        return fig

