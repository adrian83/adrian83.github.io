---
title: "Decorators in Python"
date: 2018-06-03
draft: true
categories:
- python
- decorator
tags:
- python
- decorators
thumbnailImagePosition: left
thumbnailImage: https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nibh augue, suscipit a, scelerisque sed, lacinia in, mi. Cras vel lorem. Etiam pellentesque aliquet tellus. Phasellus pharetra nulla ac diam. Quisque semper justo at risus. Donec venenatis, turpis vel hendrerit interdum, dui ligula ultricies purus, sed posuere libero dui id orci. Nam congue, pede vitae dapibus aliquet, elit magna vulputate arcu, vel tempus metus leo non est. Etiam sit amet lectus quis est congue mollis. Phasellus congue lacus eget neque. Phasellus ornare, ante vitae consectetuer consequat, purus sapien ultricies dolor, et mollis pede metus eget nisi. Praesent sodales velit quis augue. Cras suscipit, urna at aliquam rhoncus, urna quam viverra nisi, in interdum massa nibh nec erat.



{{< codeblock "base.py" "python" "https://github.com/adrian83/playground-python/blob/master/decorators/base.py" "base.py" >}}

import types

info_format = "Executing '{0}' with params: {1} {2}"

def func_invocation_info(call, *args, **kwargs):
    nameable = call if isinstance(call, types.FunctionType) else call.__class__
    argsStr = ", ".join(args)
    kwargsStr = ", ".join(["{0}={1}".format(k, v) for k, v in kwargs.items()])
    return info_format.format(nameable.__name__, argsStr, kwargsStr)

def introduce(first_name, last_name, **info):
    print("First name: {0}".format(first_name))
    print("Last name: {0}".format(last_name))
    for key, value in info.items():
        print("{0}: {1}".format(key, value))

{{< /codeblock >}}
