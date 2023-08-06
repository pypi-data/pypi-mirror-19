# -*- coding: utf-8 -*-

import collections
import yaml


def global_init_yaml():
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return collections.OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(collections.OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)


global_init_yaml()


def yaml_dump(obj, *a, **kwargs):
    return yaml.dump(obj, *a, default_flow_style=False, allow_unicode=True, **kwargs)
