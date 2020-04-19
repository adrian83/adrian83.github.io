---
title: Run code in Docker container
date: 2020-01-21
draft: true
categories:
- docker
- python
- tensorflow
tags:
- docker
- python
- tensorflow
---

### Running your code inside of Docker container can save you from installing, sometimes very complex tree of dependencies on your local computer.


##### Basics

If you ever saw the Docker tutorial you've probably also seen something like this:

`docker run alpine echo 'hello world'`

It prints 'hello world' somewhere at the end of the logged text.
In similar way we can use other containers to execute code inside of them.  

First let's look at the general command for running Docker containers:  

`$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]`

Following post presents few steps that will allow you to run your applications / scripts in an interactive way inside of the docker container.

##### Example

Some time ago I was trying to run examples from Tensorflow tutorial. I've prepared virtual environment (with Virtualenv) but when downloading required dependecnies it occured that my python installation is unsopported by Tensorflow. I thought that upgrading (or downgrading in my case) python is just too much trouble. Fortunately Tensorflow team prepared Docker images that can be used to run scripts. The image is called `tensorflow/tensorflow`.

<br/>

Testing Tensorflow installation can be anything that is using Tensorflow. In my case it file called `test_installation.py` with such content:

```
import tensorflow as tf

tensor1 = tf.convert_to_tensor([[1, 2], [3, 4]], dtype = tf.int32)
tensor2 = tf.convert_to_tensor([[2, 3], [4, 5]], dtype = tf.int32)

result = tf.add(tensor1, tensor2)

print(result)
```

<br/>

Before running this following commands please be aware that it will download Docker image with size around 2,5GB
```
$ docker system df -v
Images space usage:

REPOSITORY              TAG      IMAGE ID       SIZE      SHARED SIZE   UNIQUE SIZE 
tensorflow/tensorflow   latest   9bf93bf90865   2.469GB   64.19MB       2.405GB  
```

Now we can try to run this script by executing such command:

`docker run tensorflow/tensorflow ./test_installation.py`

It failed. I know. It's because the file `test_installation.py` is on our local hard drive and not inside of the docker container.

##### Copy files into Docker container

The easiest possible fix to this problem is to copy file into the Docker container and run it.

1. Run docker container in detached mode (option `-d`), which means that it will run until stopped, by executing: `docker run -d --name=tensorflow tensorflow/tensorflow`
2. Copy script: `docker cp ./test_installation.py tensorflow:/test.py`
3. Run it: `docker exec tensorflow python /test.py`

##### Mount whole directory into Docker container

Sometimes instead of copying file(s) it's much easier to mount directory with the script inside the Docker container. For convinience we can also make this directory working directory. We can do that by adding two options:

- `-v` - mounts specified directory to given path inside docker container  
- `-w` - setting specified directory as a working directory

Now our command looks like this:

`docker run -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py` 

This version should work, but we can make two more improvement.

##### Interactive

Probably in most cases we would like to tell Docker to redirect its terminal content to our terminal. We can achieve this by adding `-it` option (actually those are two options `-i` and `-t`).

Now our command looks like this:

`docker run -it -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py`

All nice but we can add one more improvement


##### Reusable

If you want to keep your container clean you can add one more additional option: `--rm`, which will remove file system when the container exits.

Final version of our command looks like this:

`docker run -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py`


##### Result

After runing this file I received some amount of logs and result of the executed script somewhere at the bottom of the output.

```
$ docker run -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py
2020-01-22 15:07:37.952597: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libnvinfer.so.6'; dlerror: libnvinfer.so.6: cannot open shared object file: No such file or directory
2020-01-22 15:07:37.952723: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libnvinfer_plugin.so.6'; dlerror: libnvinfer_plugin.so.6: cannot open shared object file: No such file or directory
2020-01-22 15:07:37.952754: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:30] Cannot dlopen some TensorRT libraries. If you would like to use Nvidia GPU with TensorRT, please make sure the missing libraries mentioned above are installed properly.
2020-01-22 15:07:38.597934: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libcuda.so.1'; dlerror: libcuda.so.1: cannot open shared object file: No such file or directory
2020-01-22 15:07:38.597989: E tensorflow/stream_executor/cuda/cuda_driver.cc:351] failed call to cuInit: UNKNOWN ERROR (303)
2020-01-22 15:07:38.598025: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (f9debc474004): /proc/driver/nvidia/version does not exist
2020-01-22 15:07:38.598841: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2020-01-22 15:07:38.605445: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2698015000 Hz
2020-01-22 15:07:38.606165: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x56379a961040 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
2020-01-22 15:07:38.606238: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): Host, Default Version
tf.Tensor(
[[3 5]
 [7 9]], shape=(2, 2), dtype=int32)
```

