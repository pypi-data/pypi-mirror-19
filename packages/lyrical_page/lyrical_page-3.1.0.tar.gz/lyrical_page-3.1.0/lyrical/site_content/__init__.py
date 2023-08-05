__version__ = '3.1.0'

import django
 
_libs = {}
_libs_lookup = {}
 
def template_tag_library_lookup(func_name):
    """ Find the name of the template tag library containing the given
    function name. """
    if not _libs_lookup:
        for name, lib in _libs.items():
            for v in lib.tags.keys():
                _libs_lookup[v] = name
    return _libs_lookup.get(func_name, None)
 
def register_template_tag_library(name):
    """ Register the given template tag library for automatic loading. """
    found_lib_name = None
    
    if django.VERSION < (1, 9):
        from django.template.base import get_library, InvalidTemplateLibrary
        try:
            found_lib_name = get_library(libname)
        except InvalidTemplateLibrary:
            found_lib_name = None
    else:
        #import importlib
        from django.template.backends.django import get_installed_libraries
        from django.template.library import InvalidTemplateLibrary
        try:
            lib = get_installed_libraries()[libname]
            #lib = importlib.import_module(lib).register
            #return lib
            found_lib_name = lib
        except (InvalidTemplateLibrary, KeyError):
            #return None
            pass
        
    #_libs[name] = get_library(name)
    _libs[name] = found_lib_name
