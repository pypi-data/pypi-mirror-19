import logging
import operator

import numpy as np
from dask.delayed import delayed

from scipy.optimize import differential_evolution

logger = logging.getLogger(__name__)

def make_key(id, sl):
    """Makes the dask key for the outputs of nodes

    Parameters
    ----------
    id : string
        id of the output (see also `make_key_id`)
    sl : slice
        data slice that is covered by this output
    version : identifier for the current version of the key
        allows one to separate results after node resets

    Returns
    -------
    a tuple key
    """
    n = slen(sl)
    if n <= 0:
        ValueError("Slice has no length")
    return (id, sl.start, n)


def make_key_id(task_name, node_name, node_version):
    return "{}.{}.{}".format(task_name, node_name, node_version)


def is_elfi_key(key):
    return isinstance(key, tuple) and len(key) == 3 and isinstance(key[0], str)


def get_key_id(key):
    return key[0]


def get_key_index(key):
    return key[1]


def get_key_batch_size(key):
    return key[2]


def get_key_slice(key):
    """Returns the corresponding slice from 'key'.
    """
    index = get_key_index(key)
    batch_size = get_key_batch_size(key)
    return slice(index, index + batch_size)


def reset_key_slice(key, new_sl):
    """Resets the slice from 'key' to 'new_sl'

    Returns
    -------
    a new key
    """
    return make_key(get_key_id(key), new_sl)


def reset_key_id(key, new_id):
    """Resets the name from 'key' to 'name'

    Returns
    -------
    a new key
    """
    return make_key(new_id, get_key_slice(key))


def get_named_item(output, item, name=None):
    """Makes a delayed object by appending "-name" to the output key name

    Parameters
    ----------
    output : delayed node output
    item : str
       item to take from the output
    name : str
       delayed key name (default: item)

    Returns
    -------
    delayed object yielding the item
    """
    name = name or item
    new_key_name = get_key_id(output.key) + '/' + str(name)
    new_key = reset_key_id(output.key, new_key_name)
    return delayed(operator.getitem)(output, item, dask_key_name=new_key)


def to_slice(item):
    """Converts item specifier to slice

    Currently handles only either slices or integers

    Parameters
    ----------
    item
       The things that is passed to `__getitem__` from object[item]

    Returns
    -------
    slice

    """
    if not isinstance(item, slice):
        item = slice(item, item + 1)
    return item


def slice_intersect(sl1, sl2=None, offset=0):
    sl2 = sl2 or sl1
    intsect_sl = slice(max(sl2.start, sl1.start) - offset, min(sl2.stop, sl1.stop) - offset)
    if intsect_sl.stop - intsect_sl.start <= 0:
        intsect_sl = slice(offset, offset)
    return intsect_sl


def slen(sl):
    return sl.stop - sl.start


def atleast_2d(data):
    """Translates data into at least 2d format used by the core.

    Parameters
    ----------
    data : any object
        User-originated data.

    Returns
    -------
    ret : np.ndarray

    If type(data) is not list, tuple or np.ndarray:
        ret.shape == (1, 1), ret[0][0] == data
    If type(data) is list or tuple:
        data is converted to atleast 1D numpy array, after which
    If data.ndim == 1:
        ret.shape == (len(data), 1), ret[i][0] == data[i] for all i
    If data.ndim > 1:
        ret = data

    Examples
    --------
    Plain data
    >>> atleast_2d(1)
    array([[1]])

    1D data
    >>> atleast_2d([1])
    array([[1]])
    >>> atleast_2d([1, 2])
    array([[1],
           [2]])

    2D data
    >>> atleast_2d([[1, 2]])
    array([[1, 2]])
    """
    data = np.atleast_1d(data)
    if data.ndim == 1:
        data = data[:, None]
    return data


"""
Method utils
"""


def normalize_weights(weights):
    w = np.atleast_1d(weights)
    if np.any(w < 0):
        raise ValueError("Weights must be positive")
    ws = np.sum(weights)
    if ws == 0:
        raise ValueError("All weights are zero")
    return w/ws


def weighted_cov(x, weights):
    """Unbiased weighted covariance

    Parameters
    ----------
    x : np.ndarray
        2d array with observations is rows
    weights : np.ndarray
        1d array of weights equal or greater than 0

    """

    w = normalize_weights(weights)
    x = x - np.average(x, axis=0, weights=w)

    with np.errstate(divide='ignore'):
        a = 1/(1-np.sum(w**2))
    if np.isinf(a):
        logger.warning("Could not compute weighted covariance (division by zero). "
                       "Returning a unit covariance.")
        return np.diag([1]*x.shape[1])

    cov = np.dot(x.T, w[:,None]*x)

    return a*cov


def stochastic_optimization(fun, bounds, its, polish=False):
    """ Called to find the minimum of function 'fun' in 'its' iterations """
    result = differential_evolution(func=fun, bounds=bounds, maxiter=its,
                                    popsize=30, tol=0.01, mutation=(0.5, 1),
                                    recombination=0.7, disp=False,
                                    polish=polish, init='latinhypercube')
    return result.x, result.fun
