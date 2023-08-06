# Plotting API for genotype-phenotype maps

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import warnings

def mpl_missing(function):
    """ Function wrapper to check that matplotlib is install. """
    def wrapper(*args, **kwargs):
        try:
            import matplotlib
            return function(*args, **kwargs)
        except ImportError:
            warnings.filterwarnings("once")
            warnings.warn("""Looks like `matplotlib` is not installed, so plots can't be constructed.
                        Install matplotlib before trying to use this method.""", ImportWarning)
    return wrapper

class PlottingContainer(object):

    @mpl_missing
    def __init__(self, gpm):
        """A class for quickly building plots from genotype-phenotype maps
        """
        self._gpm = gpm

    def phenotypes(self, with_err=False, horizontal=False):
        """Plot the phenotypes of a genotype phenotype map"""
        if horizontal:
            raise Warning(""" Horizontal plot not implemented yet. """)
        else:
            # construct plot
            if self._gpm.tranformed:
                # Get the non-transformed data

                # Plot error?
                if with_err:
                    err = self._gpm.err.upper
                else:
                    err = None

                fig, ax = phenotypes_barh(self._gpm.genotypes,
                    self._gpm.phenotypes,
                    wildtype=self._gpm.wildtype,
                    errors=err,
                )
            else:

                # Plot error?
                if with_err:
                    err = [self._gpm.err.upper, self._gpm.err.lower]
                else:
                    err = None

                fig, ax = phenotypes_barh(self._gpm.genotypes,
                    self._gpm.phenotypes,
                    wildtype=self._gpm.wildtype,
                    errors=err,
                )
        return fig, ax

@mpl_missing
def phenotypes_barh(genotypes, phenotypes, wildtype=None, errors=None, xlabel="", title="", figsize=(), **kwargs):
    """Plot phenotypes as horizontal bars.
    """
    n_genotypes = len(genotypes)

    if figsize == ():
        figsize = (5, n_genotypes/5.0)

    fig, ax = mpl.pyplot.subplots(figsize=figsize)


    # default graph styling
    graph_properties = {'color':"k", 'alpha':0.5, 'error_kw':{'ecolor': '0.3'}}

    # Add user defined
    for key in kwargs:
        graph_properties[key] = kwargs[key]

    # plot
    ax.barh(range(n_genotypes), phenotypes, 1, xerr=errors, align='center', **graph_properties)

    # -------------------------
    # Prettify graph
    # -------------------------

    xlimits = list(ax.get_xlim())

    ax.axis('tight')
    # Get current axis limits
    extra_limit_frac = 0.02

    xlimits = list(ax.get_xlim())
    ylimits = list(ax.get_ylim())
    xticks = list(ax.get_xticks())
    yticks = list(ax.get_yticks())

    # Extend the graph by 5 percent on all sides
    xextra = extra_limit_frac*(xlimits[1] - xlimits[0])
    yextra = extra_limit_frac*(ylimits[1] - ylimits[0])

    # set ticks and tick labels
    ax.set_xlim(xlimits[0] - xextra, xlimits[1] + xextra)
    ax.set_ylim(ylimits[0] - yextra, ylimits[1] + yextra)

    # Remove right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set the bounds for visible axes
    ax.spines['bottom'].set_bounds(xticks[1], xticks[-2])
    ax.spines['left'].set_bounds(ylimits[0], ylimits[1])

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('bottom')

    # Make ticks face outward and thicken them
    ax.tick_params(direction='out')#, width=spine_widths)

    fontProperties = {'family':'monospace'}

    ax.set_yticks(range(n_genotypes))
    ax.set_yticklabels(genotypes, fontProperties)

    # Label axis and title
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    return fig, ax


class MonteCarloSimulationPlotting(object):

    @mpl_missing
    def __init__(self, simulation):

        self._simulation = simulation

class TrajectoriesPlotting(object):

    @mpl_missing
    def __init__(self, trajectories):
        """An object for visualizing trajectory data.
        """
        self._trajectories = trajectories

    def spectrum(self, ax=None, figsize=(6,4), **kwargs):
        """Plots a spectrum of forward trajectories' probabilities, labeled by their index.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.get_figure()

        # Calculate possible paths
        possible = self._trajectories.possible
        paths = [tuple(path) for path in possible]

        indices = range(len(paths))
        counts = self._trajectories.forward
        N = sum(list(counts.values()))

        # Iterate through trajectories to construct probabilities array.
        probabilities = []
        for p in paths:
            # Try to see probability.
            try:
                fraction = counts[p]/N
                probabilities.append(fraction)
            # If path is not in counts, it has 0 probabilities
            except KeyError:
                probabilities.append(0)

        # Create plot
        ax.plot(indices, probabilities)
        ax.set_xlabel("Trajectory ID")
        ax.set_ylabel("Probability of Trajectory")

        return fig, ax
