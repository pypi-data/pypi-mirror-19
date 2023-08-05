======================
Django Settings Helper
======================

Django Settings Helper helps you get environment variables. It is created for settings of Django framework based projects,
however it can be used generally, without Django.


Simple Usage
------------

get_env
~~~~~~~
get_env gets environment variables by keys, and cast into types other than string, such as integer, or boolean::

    foo = get_env('foo')  # read 'foo'. When not found, None is returned

    # read 'bar'. When not found, 'ImproperlyConfigured' exception is raised.
    # if you're using django, django.core.exceptions.ImproperlyConfigured is raised.
    bar = get_env('bar', strict=True)

    # read 'baz'. If goes strict when DEBUG is False.
    baz = get_env('baz', strict=(not DEBUG), default='baz')

    # read DEBUG. When not found, True is returned.
    # environment variable is casted into True, or False if
    # the value is one of these: True, False, Yes, No, On, Off, 1, 0 (case-insensitive)
    bool_val = get_env('DEBUG', strict=False, default=True, type_cast=bool)

    # type_cast parameter not only supports primitive types such as int, bool, and float
    # but also more complex types like dict, list, and 'json'.
    list_cast = get_env('LIST_CAST', type_cast=list)
    dict_cast = get_env('DICT_CAST', type_cast=dict)
    json_load = get_env('JSON_LOAD', type_cast='json')

env_from_file
~~~~~~~~~~~~~
env_from_file() reads environment variables from path.
Variables should be declared with 'export' keyword, e.g.) export FOO=BAR


import_all
~~~~~~~~~~
import_all imports other packages' variables::

    # file: x.y.z_pkg.py
    def test():
        print('hello!')

    FOO = 'foo'
    BAR = 'bar'
    # end of x.y.z_pkg.py

    # file: foo.py
    import_all('x.y.z_pkg', globals())

    # all variables, functions in 'x.y.z_pkg' are imported into this package.
    test()
    print(FOO)
