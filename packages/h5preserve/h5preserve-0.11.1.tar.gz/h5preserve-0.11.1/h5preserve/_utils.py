# coding: utf-8
"""
Internal utilities for h5preserve

:copyright: (c) 2016 James Tocknell
:license: 3-clause BSD
"""
from collections import namedtuple, Callable

H5PRESERVE_ATTR_NAMESPACE = "_h5preserve_namespace"
H5PRESERVE_ATTR_LABEL = "_h5preserve_label"
H5PRESERVE_ATTR_VERSION = "_h5preserve_version"
H5PRESERVE_ATTR_ON_DEMAND = "_h5preserve_on_demand"

DumperMap = namedtuple("DumperMap", "label func")


def get_group_items(h5py_obj, attrs, registries, load_on_demand):
    """
    Return group items considering the use of on-demand support
    """
    if attrs.get(H5PRESERVE_ATTR_ON_DEMAND, False) and not load_on_demand:
        return {
            name: get_on_demand_group_item(h5py_obj, name, registries)
            for name in h5py_obj
        }
    return {
        # pylint: disable=protected-access
        name: registries._h5py_to_h5preserve(item)
        # pylint: enable=protected-access
        for name, item in h5py_obj.items()
    }


def get_on_demand_group_item(h5py_obj, name, registries):
    """
    Return item from group as an on demand item
    """
    def get_item():
        """
        func for OnDemandWrapper
        """
        return registries.load(
            # pylint: disable=protected-access
            registries._h5py_to_h5preserve(
                h5py_obj[name], load_on_demand=True
            )
            # pylint: enable=protected-access
        )
    return OnDemandWrapper(get_item)


def get_dataset_data(h5py_obj, attrs, load_on_demand):
    """
    Return the actual data from a dataset considering the use of on-demand
    support.
    """
    if attrs.get(H5PRESERVE_ATTR_ON_DEMAND, False) and not load_on_demand:
        return OnDemandWrapper(lambda: h5py_obj[()])
    return h5py_obj[()]


def on_demand_group_dumper_generator(registry_container, h5py_group):
    """
    Generate the support function for on-demand dumping for the dumpable
    object.
    """
    def on_demand_dumper(key, val):
        """
        Support function for on-demand dumping
        """
        registry_container.to_file(
            h5py_group, key, registry_container.dump(val)
        )
        return get_on_demand_group_item(h5py_group, key, registry_container)
    return on_demand_dumper


class OnDemandWrapper(Callable):
    """
    Wrapper which represents a container which can be accessed on demand.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, func):
        self._func = func

    def __call__(self):
        return self._func()
