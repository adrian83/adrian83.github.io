---
title: "Decorators in Python"
date: 2019-01-12
draft: true
categories:
- python
- decorator
- decorators
tags:
- python
- decorator
- decorators
thumbnailImagePosition: left
thumbnailImage: https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg
---

Decorators are one of my favorite Python features. 
By using them we can alter functions and methods. From decorator we have access to method / function arguments as well as returned value. We don't even have to execute decorated function. 
<!--more-->

Decorators can be implemented in two ways: as a function or as a class. Both types of decorators offer almost the same functionality. 

First let's see code that will be used in all examples:
(1) Function that will return text information about wrapped function (name and given parameters). This function will be used internally by every presented decorator.
(2) Function that will be 'decorated' by every presented decorator.


 "base.py" "python" "https://github.com/adrian83/playground-python/blob/master/decorators/base.py" "base.py" 

import types
import time

info_format = "Executing '{0}' with params: {1} {2}"

# (1)
def func_invocation_info(call, *args, **kwargs):
    nameable = call if isinstance(call, types.FunctionType) else call.__class__
    argsStr = ", ".join(args)
    kwargsStr = ", ".join(["{0}={1}".format(k, v) for k, v in kwargs.items()])
    return info_format.format(nameable.__name__, argsStr, kwargsStr)

# (2)
def introduce(first_name, last_name, **info):
    print("First name: {0}".format(first_name))
    print("Last name: {0}".format(last_name))
    for key, value in info.items():
        print("{0}: {1}".format(key, value))




### Function as a Decorator

Below you can find two different decorators:
(1) Simplest decorator . 
(2) Decorator with parameters.

You can also see example (3) of using many decorators on a single function. Execution ordering is quite intuitive - from top to bottom. What is worth noting is the fact that 'upper' decorator is actualy decorating the other one and not the function.


"decorator_func.py" "python" "https://github.com/adrian83/playground-python/blob/master/decorators/decorator_func.py" "decorator_func.py" 

from base import func_invocation_info, introduce

# (1)
def log(func):
    def wrapper(*args, **kwargs):
        print(func_invocation_info(func, *args, **kwargs))
        return func(*args, **kwargs)
    return wrapper


@log
def introduce_1(first_name, last_name, **info):
    print("PERSONAL DATA")
    introduce(first_name, last_name, **info)
    print("")


introduce_1("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")

# (2)
def log2(level, file_name):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            info = func_invocation_info(func, *args, **kwargs)
            print("[{0}] [{1}] {2}".format(level, file_name, info))
            return func(*args, **kwargs)
        return wrapper2
    return wrapper1


@log2("INFO", "decorators_func.py")
def introduce_2(first_name, last_name, **info):
    print("PERSONAL DATA")
    introduce(first_name, last_name, **info)
    print("")


introduce_2("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")


# (3)
@log2("INFO", "decorators_func.py")
@log
def introduce_3(first_name, last_name, **info):
    print("PERSONAL DATA")
    introduce(first_name, last_name, **info)
    print("")


introduce_3("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")





"output.sh" "bash" 

[adrian@adrian-pc decorators]$ python decorator_func.py 
Executing 'introduce_1' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden

[INFO] [decorators_func.py] Executing 'introduce_2' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden

[INFO] [decorators_func.py] Executing 'wrapper' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
Executing 'introduce_3' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden




### Class as a Decorator


Below you can find two different decorators:
(1) Simplest decorator. 
(2) Decorator with parameters.

You can also see example (3) of using many decorators on a single function. Execution ordering is quite intuitive - from top to bottom. What is worth noting is the fact that 'upper' decorator is actualy decorating the other one and not the function.


"decorator_class.py" "python" "https://github.com/adrian83/playground-python/blob/master/decorators/decorator_class.py" "decorator_class.py" 

from base import func_invocation_info, introduce

# (1)
class Log:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(func_invocation_info(self.func, *args, **kwargs))
        return self.func(*args, **kwargs)


@Log
def introduce_1(first_name, last_name, **info):
    print("PERSONAL DATA")
    introduce(first_name, last_name, **info)
    print("")


introduce_1("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")

# (2)
class Log2:

    def __init__(self, level, file_name):
        self.level = level
        self.file_name = file_name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            info = func_invocation_info(func, *args, **kwargs)
            print("[{0}] [{1}] {2}".format(self.level, self.file_name, info))
            return func(*args, **kwargs)
        return wrapper


@Log2("INFO", "decorators_class.py")
def introduce_2(first_name, last_name, **info):
    print("PERSONAL DATA")
    introduce(first_name, last_name, **info)
    print("")


introduce_2("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")

# (3)
@Log2("INFO", "decorators_class.py")
@Log
def introduce_3(first_name, last_name, **info):
    print("PERSONAL DATA")
    introduce(first_name, last_name, **info)
    print("")


introduce_3("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")




"output.sh" "bash" 

[adrian@adrian-pc decorators]$ python decorator_class.py 
Executing 'introduce_1' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden

[INFO] [decorators_class.py] Executing 'introduce_2' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden

[INFO] [decorators_class.py] Executing 'Log' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
Executing 'introduce_3' with params: William, Shakespeare Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden





## Summary
Decorators are very useful Python feature which is used heavily in almost all Python frameworks as well as in Python standard library (@classmethod, @staticmethod). That's why it is very important to understand how to create and use them.


#### Sources
1. [Python Decorators](https://wiki.python.org/moin/PythonDecorators)