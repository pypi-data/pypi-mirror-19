import numpy as np
from collections import OrderedDict
import inspect
import sys
import io
import matplotlib.pyplot as plt

import elfi.visualization as vis


"""
Implementations related to results and post-processing.
"""


class Result(object):
    """Container for results from ABC methods. Allows intuitive syntax for plotting etc.

    Parameters
    ----------
    samples_list : list of np.arrays
    nodes : list of parameter nodes
    """
    def __init__(self, samples_list, nodes, **kwargs):
        self.samples = OrderedDict()
        for ii, n in enumerate(nodes):
            self.samples[n.name] = samples_list[ii]
        self.n_samples = len(list(self.samples.values())[0])
        self.n_params = len(self.samples)

        # get name of the ABC method
        stack10 = inspect.stack()[1][0]
        self.method = stack10.f_locals["self"].__class__.__name__

        # store arbitrary keyword arguments here
        self.meta = kwargs

    def __getattr__(self, item):
        """Allows more convenient access to items under self.meta.
        """
        if item in self.__dict__:
            return self.item
        elif item in self.meta.keys():
            return self.meta[item]

    def __dir__(self):
        """Allows autocompletion for items under self.meta.
        http://stackoverflow.com/questions/13603088/python-dynamic-help-and-autocomplete-generation
        """
        items = dir(type(self)) + list(self.__dict__.keys())
        items.extend(self.meta.keys())
        return items

    @property
    def samples_list(self):
        """
        Return the samples as a list in the same order as in the OrderedDict samples.

        Returns
        -------
        list of np.arrays
        """
        return list(self.samples.values())

    @property
    def names_list(self):
        """
        Return the parameter names as a list in the same order as in the OrderedDict samples.

        Returns
        -------
        list of strings
        """
        return list(self.samples.keys())

    def __str__(self):
        # create a buffer for capturing the output from summary's print statement
        stdout0 = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer
        self.summary()
        sys.stdout = stdout0  # revert to original stdout
        return buffer.getvalue()

    def __repr__(self):
        return self.__str__()

    def summary(self):
        """Print a verbose summary of contained results.
        """
        # TODO: include __str__ of Inference Task, seed?
        desc = "Method: {}\nNumber of posterior samples: {}\n"\
               .format(self.method, self.n_samples)
        if hasattr(self, 'n_sim'):
            desc += "Number of simulations: {}\n".format(self.n_sim)
        if hasattr(self, 'threshold'):
            desc += "Threshold: {:.3g}\n".format(self.threshold)
        print(desc, end='')
        self.posterior_means()

    def posterior_means(self):
        """Print a representation of posterior means.
        """
        s = "Posterior means: "
        s += ', '.join(["{}: {:.3g}".format(k, np.mean(v)) for k,v in self.samples.items()])
        print(s)

    def plot_marginals(self, selector=None, bins=20, axes=None, **kwargs):
        """Plot marginal distributions for parameters.

        Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional

        Returns
        -------
        axes : np.array of plt.Axes
        """
        return vis.plot_marginals(self.samples, selector, bins, axes, **kwargs)

    def plot_pairs(self, selector=None, bins=20, axes=None, **kwargs):
        """Plot pairwise relationships as a matrix with marginals on the diagonal.

        The y-axis of marginal histograms are scaled.

         Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional

        Returns
        -------
        axes : np.array of plt.Axes
        """
        return vis.plot_pairs(self.samples, selector, bins, axes, **kwargs)


class Result_SMC(Result):
    """Container for results from SMC-ABC.
    """
    def posterior_means_all_populations(self):
        """Print a representation of posterior means for all populations.

        Returns
        -------
        out : string
        """
        samples = self.samples_history + [self.samples_list]
        weights = self.weights_history + [self.weights]
        n = self.names_list
        out = ''
        for ii in range(self.n_populations):
            s = samples[ii]
            w = weights[ii]
            out += "Posterior means for population {}: ".format(ii)
            out += ', '.join(["{}: {:.3g}".format(n[jj], np.average(s[jj], weights=w, axis=0)[0])
                              for jj in range(self.n_params)])
            out += '\n'
        print(out)

    def plot_marginals_all_populations(self, selector=None, bins=20, axes=None, **kwargs):
        """Plot marginal distributions for parameters for all populations.

        Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional
        """
        samples = self.samples_history + [self.samples_list]
        fontsize = kwargs.pop('fontsize', 13)
        for ii in range(self.n_populations):
            s = OrderedDict()
            for jj, n in enumerate(self.names_list):
                s[n] = samples[ii][jj]
            ax = vis.plot_marginals(s, selector, bins, axes, **kwargs)
            plt.suptitle("Population {}".format(ii), fontsize=fontsize)

    def plot_pairs_all_populations(self, selector=None, bins=20, axes=None, **kwargs):
        """Plot pairwise relationships as a matrix with marginals on the diagonal for all populations.

        The y-axis of marginal histograms are scaled.

         Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional
        """
        samples = self.samples_history + [self.samples_list]
        fontsize = kwargs.pop('fontsize', 13)
        for ii in range(self.n_populations):
            s = OrderedDict()
            for jj, n in enumerate(self.names_list):
                s[n] = samples[ii][jj]
            ax = vis.plot_pairs(s, selector, bins, axes, **kwargs)
            plt.suptitle("Population {}".format(ii), fontsize=fontsize)

class Result_BOLFI(Result):
    """Container for results from BOLFI.
    """
    pass