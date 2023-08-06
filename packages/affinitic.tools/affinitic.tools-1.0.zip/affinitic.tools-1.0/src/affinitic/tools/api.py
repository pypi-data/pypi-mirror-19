# -*- coding: utf-8 -*-
"""
affinitic.tools
---------------

Created by mpeeters
:copyright: (c) 2016 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import inspect


def declare_api(*elements):
    """Function to declare an api on a module"""
    module_globals = inspect.currentframe().f_back.f_globals
    api_list = []
    for element in elements:
        if inspect.isclass(element) or inspect.isfunction(element):
            api_list.append(element.__name__)
        elif ':' in element:
            api_list.append(_add_class(element, module_globals))
        else:
            api_list.extend(_iterate_api(element, module_globals))
    return tuple(api_list)


def _iterate_api(path, module_globals):
    api_list = []
    element = path.split('.')[-1]
    module = __import__(path, globals(), locals(), [element])
    for cls in module.__all__:
        api_list.append(cls)
        module_globals[cls] = getattr(module, cls)
    return api_list


def _add_class(path, module_globals):
    module_path, element = path.split(':')
    module_name = module_path.split('.')[-1]
    # It is important to import the module and not the class or function
    # directly !
    module = __import__(module_path, globals(), locals(), [module_name])
    module_globals[element] = getattr(module, element)
    return element


def extend_api(api_globals, api):
    """Extend the globals with the given api"""
    extends = []
    for cls in api.__all__:
        api_globals[cls] = getattr(api, cls)
        extends.append(cls)
    api_globals['__all__'] += tuple(extends)
