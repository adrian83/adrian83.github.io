---
title: Decorators in Python
date: 2020-04-10
draft: true
categories:
- python
- decorators
tags:
- python
- decorators
---

### Decorators in Python are very powerful and elegant way to wrap functions and classes, modify it's arguments, returned value or block wrapped function from invocation.

In this post we will see how to create decorators implemented as functions as well as classes. We will see that also decorators can have parameters and we will see results of using multiple decorators on single function.


Before we go to decorators let's see code that will be used in every example.
First function will be used in every decorator presented below and it will print name of decorated function / class and it's arguments.
Second one is a function on which we will test every created decorator.

```
import types
import time

info_format = "Executing '{0}' with *args: {1} and **kwargs: {2}"

def func_invocation_info(call, *args, **kwargs):
    name = (call if isinstance(call, types.FunctionType) else call.__class__).__name__
    argsStr = ", ".join(args)
    kwargsStr = ", ".join(["{0}={1}".format(k, v) for k, v in kwargs.items()])
    return info_format.format(name, argsStr, kwargsStr)


def introduce(first_name, last_name, **info):
    print("PERSONAL DATA:")
    print("First name: {0}".format(first_name))
    print("Last name: {0}".format(last_name))
    for key, value in info.items():
        print("{0}: {1}".format(key, value))
    print("")
```

#### Python decorators implemented as functions


##### Decorator without it's own parameters
```
def log(func):
    def wrapper(*args, **kwargs):
        print(func_invocation_info(func, *args, **kwargs))
        return func(*args, **kwargs)
    return wrapper


@log
def introduce_ex1(first_name, last_name, **info):
    introduce(first_name, last_name, **info)


introduce_ex1("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")
```

Output:
```
Executing 'introduce_ex1' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA:
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden
```

The code above can be also written as:
```
introduce_ex1 = log(introduce_ex1)
introduce_ex1("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")
```

The `log` function (our decorator) accepts function and returns function (`wrapper`) which is ready for accepting arguments.
Invocation of that wrapped function first prints info about wrapped function, and then executes it. 



##### Decorator with it's own parameters
```
def log2(level, file_name):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            info = func_invocation_info(func, *args, **kwargs)
            print("[{0}] [{1}] {2}".format(level, file_name, info))
            return func(*args, **kwargs)
        return wrapper2
    return wrapper1


@log2("INFO", "decorator_func.py")
def introduce_ex2(first_name, last_name, **info):
    introduce(first_name, last_name, **info)


introduce_ex2("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")
```

Output:
```
[INFO] [decorator_func.py] Executing 'introduce_ex2' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA:
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden
```

##### Multiple decorators on single function / method
```
@log2("INFO", "decorator_func.py")
@log
def introduce_ex3(first_name, last_name, **info):
    introduce(first_name, last_name, **info)
```

Output:
```
[INFO] [decorator_func.py] Executing 'wrapper' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
Executing 'introduce_ex3' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA:
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden
```


#### Python decorators implemented as classes


##### Decorator without it's own parameters
```
class Log:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(func_invocation_info(self.func, *args, **kwargs))
        return self.func(*args, **kwargs)


@Log
def introduce_1(first_name, last_name, **info):
    introduce(first_name, last_name, **info)


introduce_1("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")
```

Output:
```
Executing 'introduce_ex1' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA:
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden
```


##### Decorator with it's own parameters
```
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


@Log2("INFO", "decorator_class.py")
def introduce_ex2(first_name, last_name, **info):
    introduce(first_name, last_name, **info)


introduce_ex2("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")
```

Output:
```
[INFO] [decorator_class.py] Executing 'introduce_ex2' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA:
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden
```


##### Multiple decorators on single function / method
```
@Log2("INFO", "decorator_class.py")
@Log
def introduce_ex3(first_name, last_name, **info):
    introduce(first_name, last_name, **info)


introduce_ex3("William", "Shakespeare", Father="John Shakespeare",
            Mother="Mary Arden")
```

Output:
```
[INFO] [decorator_class.py] Executing 'Log' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
Executing 'introduce_ex3' with *args: William, Shakespeare and **kwargs: Father=John Shakespeare, Mother=Mary Arden
PERSONAL DATA:
First name: William
Last name: Shakespeare
Father: John Shakespeare
Mother: Mary Arden
```