---
title: Python decorators
date: 2020-04-10
draft: true
categories:
- python
- decorators
tags:
- python
- decorators
---

### Python decorators






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