import numpy as np

def probability_of_path(paths, transition_matrix):
    """Calculate the probability of a given trajectory by calculating the
    string of conditional probabilities from a transition matrix.

    Parameters
    ----------
    paths : list of lists
        List of the indicies matching the state indices in transition matrix
    transition matrix : 2d array
        Transition matrix. elements represent the probability of transitions from
        state i --> j and vice versa.

    Returns
    -------
    probabilities : array (length = len(paths))
        Probabilities for array of paths.
    """
    if type(paths) == tuple:
        paths = [paths]

    # Get the path length
    path_length = len(paths[0])

    # Build a list of probabilities
    probabilities = list()

    # Iterate through all paths in paths-list
    for p in paths:

        # Begin by giving this path a probability of 1.
        pi = 1

        # Iterate through edges and multiply by the
        # transition probability of that edge.
        for i in range(path_length-1):
            pi *= transition_matrix[p[i],p[i+1]]

        # Append pi to probabilities
        probabilities.append(pi)

    probabilities = np.array(probabilities)

    # Return normalized probabilities. If sum(probabilities) is zero, return
    # a vector of zeros.
    if sum(probabilities) == 0 :
        return probabilities
    else:
        return probabilities/sum(probabilities)
