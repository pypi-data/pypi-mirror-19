# -*- coding: utf-8 -*-
"""
Thin wrapper around PyYAML library it creates a Dumper
and Loader derived from SafeDumper and SafeLoader for 
odict data manipulation.

ODictDumper makes block style by default.

Original code not always straightforward for me.

:copyright: (c) 2014 by Szabolcs Blága
:license: see LICENSE for more details   
"""

__all__ = ['odict', 'load', 'load_all', 'dump', 'dump_all']

__version__ = '0.1-dev'

import yaml

# upstream
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import SafeConstructor, ConstructorError
from yaml.resolver import Resolver
from yaml.representer import SafeRepresenter
from yaml.serializer import Serializer
from yaml.emitter import Emitter
# downstream

from yaml.nodes import MappingNode, ScalarNode
# from yaml.dumper import SafeDumper

try:
    from collections import OrderedDict as odict # from Python 2.7
except ImportError:
    from .od_backport import OrderedDict as odict


class ODictConstructor(SafeConstructor):

    def construct_mapping(self, node, deep=False):
        # the BaseConstructor.constructmapping is merged for simplicity
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        self.flatten_mapping(node)
        mapping = odict() # odict change
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise ConstructorError("while constructing a mapping", node.start_mark,
                        "found unacceptable key (%s)" % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

    def construct_yaml_map(self, node):
        data = odict() # other odict change (update makes it necessary to add odict twice)
        yield data
        value = self.construct_mapping(node)
        data.update(value)

ODictConstructor.add_constructor(
        u'tag:yaml.org,2002:map',
        ODictConstructor.construct_yaml_map)


class ODictLoader(Reader, Scanner, Parser, Composer, ODictConstructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        ODictConstructor.__init__(self)
        Resolver.__init__(self)


def load(stream):
    return yaml.load(stream, ODictLoader)


def load_all(stream):
    return yaml.load_all(stream, ODictLoader)


class ODictRepresenter(SafeRepresenter):

    def represent_mapping(self, tag, mapping, flow_style=None):
        value = []
        node = MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        if hasattr(mapping, 'items'):
            mapping = mapping.items()
            # mapping.sort() # the only necessary change
        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, ScalarNode) and not node_key.style):
                best_style = False
            if not (isinstance(node_value, ScalarNode) and not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

ODictRepresenter.add_representer(odict,
        ODictRepresenter.represent_dict)


class ODictDumper(Emitter, Serializer, ODictRepresenter, Resolver):

    def __init__(self, stream,
            default_style=None, default_flow_style=None,
            canonical=None, indent=None, width=None,
            allow_unicode=None, line_break=None,
            encoding=None, explicit_start=None, explicit_end=None,
            version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical,
                indent=indent, width=width,
                allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding,
                explicit_start=explicit_start, explicit_end=explicit_end,
                version=version, tags=tags)
        ODictRepresenter.__init__(self, default_style=default_style,
                default_flow_style=default_flow_style)
        Resolver.__init__(self)


def dump(data, stream=None, **kwds):
    kwds.setdefault('default_flow_style', False)
    return yaml.dump_all([data], stream, Dumper=ODictDumper, **kwds)


def dump_all(documents, stream=None, **kwds):
    kwds.setdefault('default_flow_style', False)
    return yaml.dump_all(documents, stream, Dumper=ODictDumper, **kwds)


