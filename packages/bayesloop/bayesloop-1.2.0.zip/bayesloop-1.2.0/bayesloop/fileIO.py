#!/usr/bin/env python
"""
This file includes functions for saving and loading instances of Study objects using dill.
"""

from __future__ import division, print_function
import dill


def save(filename, study):
    """
    Save an instance of a bayesloop study class to file.

    Args:
        filename(str): Path + filename to store bayesloop study
        study: Instance of study class (Study, RasterStudy, etc.)
    """
    with open(filename, 'wb') as f:
        dill.dump(study, f, protocol=dill.HIGHEST_PROTOCOL)
    print('+ Successfully saved current study.')


def load(filename):
    """
    Load a instance of a bayesloop study class that was saved using the bayesloop.save() function.

    Args:
        filename(str): Path + filename to stored bayesloop study

    Returns:
        Study instance
    """
    with open(filename, 'rb') as f:
        S = dill.load(f)
    print('+ Successfully loaded study.')

    return S
