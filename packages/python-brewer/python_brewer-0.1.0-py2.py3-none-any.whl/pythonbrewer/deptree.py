# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future.utils import iteritems

from copy import deepcopy
import pip
from pipdeptree import build_dist_index, construct_tree, sorted_tree

from pythonbrewer.errors import *

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "build_dep_tree",
    "ordered_deps",
    "dedup_deps"
]


def get_children(key_tree, n):
    return key_tree.get(n.key, [])


def recursive_build_tree(key_tree, n):
    tree = dict()
    for child in get_children(key_tree, n):
        tree[child.project_name] = child.as_dict()
        tree[child.project_name]['deps'] = recursive_build_tree(key_tree, child)
    return tree if len(tree) else None


def recursive_extract_dep_list(key_tree, cur_key):
    deps = []
    for package in key_tree[cur_key]:
        # if this package has dependencies, add those first
        if len(key_tree[package.key]) > 0:
            deps.extend(recursive_extract_dep_list(key_tree, package.key))

        # add this package as a dependency
        deps.append(package)

    return deps


def build_dep_list(package_name, local_only=True):
    """Builds a dependency list for the given package, assuming the given package has already been
    installed. The dependency list is provided in the order in which it needs to be installed.

    Args:
        package_name: The name of the package for which to build a dependency tree.
        local_only: Look in local distribution? Default: True.

    Returns:
        A Python list containing information about the dependencies for that package.
    """
    packages = pip.get_installed_distributions(local_only=local_only)
    dist_index = build_dist_index(packages)
    tree = sorted_tree(construct_tree(dist_index))
    nodes = tree.keys()
    # filter by our desired package only
    nodes = [p for p in nodes if p.key == package_name or p.project_name == package_name]
    if len(nodes) == 0:
        raise PackageNotFoundError(package_name)
    if len(nodes) > 1:
        raise MultiplePackagesFoundError(package_name)

    key_tree = dict((k.key, v) for k, v in iteritems(tree))
    deps = recursive_extract_dep_list(key_tree, 'statik')
    import pdb; pdb.set_trace()
    return deps


def ordered_deps(dep_tree):
    """Computes the best order in which to install dependencies from the given dependency tree.

    Args:
        dep_tree: The result of calling build_dep_tree().

    Returns:
        A list of packages' details in the order in which they should be installed.
    """
    result = []
    if dep_tree['deps'] is not None:
        for package_name, package_info in iteritems(dep_tree['deps']):
            result.extend(ordered_deps(package_info))

    dep_tree_copy = deepcopy(dep_tree)
    del dep_tree_copy['deps']
    result.append(dep_tree_copy)
    return result


def dedup_deps(deps):
    """Deduplicates a list of ordered dependencies."""
    result = []
    seen_deps = set()
    for dep in deps:
        if dep['package_name'] not in seen_deps:
            seen_deps.add(dep['package_name'])
            result.append(dep)
        else:
            logger.debug("Found duplicate dependency: %s" % dep['package_name'])
    return result
