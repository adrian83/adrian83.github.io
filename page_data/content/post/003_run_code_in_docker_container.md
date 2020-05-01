---
title: Run code in Docker container
date: 2020-04-27
draft: false
categories:
- docker
- python
- tensorflow
tags:
- docker
- python
- tensorflow
---

### Running your code inside of Docker container can save you from installing, sometimes very complex, tree of dependencies on your local computer.


##### Introduction

Following post presents a few steps, that will allow you to run your applications / scripts in an interactive way inside the Docker container.

First let's look at the general command for running Docker containers:  

`docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]`

Using this commmand we can run our first example which in this case is `echo` command:

`docker run alpine echo 'hello world'`

It prints `hello world` somewhere at the end of the logged text.
In similar way we can use other containers to execute our code inside of them.  


##### Problem

Some time ago I was trying to run examples from Tensorflow tutorial. To avoid poluting my operating system, I've prepared virtual environment (with Virtualenv), to which I wanted to download required dependecnies. Unfortunately it turned out, that my python installation is unsupported by Tensorflow. I thought, that upgrading (or downgrading in my case) python is just too much trouble. Fortunately Tensorflow team prepared Docker images, that can be used to run scripts. The image is called `tensorflow/tensorflow`.

<br/>

Let's assume, we have a python script, which uses Tensorflow, that we want to run inside Docker container. We can call it `test_installation.py` and fill it with such content:

```
import tensorflow as tf

tensor1 = tf.convert_to_tensor([[1, 2], [3, 4]], dtype = tf.int32)
tensor2 = tf.convert_to_tensor([[2, 3], [4, 5]], dtype = tf.int32)

result = tf.add(tensor1, tensor2)

print(result)
```

<br/>

Before running following commands please be aware, that it will download Docker image with size around 2,5GB.

```
$ docker system df -v
Images space usage:

REPOSITORY              TAG      IMAGE ID       SIZE      SHARED SIZE   UNIQUE SIZE 
tensorflow/tensorflow   latest   9bf93bf90865   2.469GB   64.19MB       2.405GB  
```

Now we can try to run this script, by executing such command:

`docker run tensorflow/tensorflow ./test_installation.py`

Don't expect too much. It will fail. It's because, the file `test_installation.py` is on our local hard drive, and not inside the docker container.


##### Mount whole directory into Docker container

Easiest way to allow Docker to access our files is to mount directory inside the Docker container. For convinience we can also make it our working directory. We can do that, by adding two options:

- `-v` - mounts specified directory to given path inside docker container  
- `-w` - setting specified directory as a working directory

Now our command looks like this:

`docker run -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py` 

This version should work, but we can make two more improvement.


##### Interactive

Probably in most cases we would like to tell Docker to redirect its terminal content to our terminal. We can achieve this by adding `-it` option (actually those are two options `-i` and `-t`).

Now our command looks like this:

`docker run -it -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py`

We are almost done, but we can add one more improvement.


##### Reusable

If you want to keep your container clean, you can add one more additional option: `--rm`, which will remove file system when the container exits.

Final version of our command looks like this:

`docker run -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py`


##### Result

After running this file I received some amount of logs and result of the executed script somewhere at the bottom of the output.

```
2020-04-27 18:50:49.603913: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libnvinfer.so.6'; dlerror: libnvinfer.so.6: cannot open shared object file: No such file or directory
2020-04-27 18:50:49.604005: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libnvinfer_plugin.so.6'; dlerror: libnvinfer_plugin.so.6: cannot open shared object file: No such file or directory
2020-04-27 18:50:49.604014: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:30] Cannot dlopen some TensorRT libraries. If you would like to use Nvidia GPU with TensorRT, please make sure the missing libraries mentioned above are installed properly.
2020-04-27 18:50:50.016786: W tensorflow/stream_executor/platform/default/dso_loader.cc:55] Could not load dynamic library 'libcuda.so.1'; dlerror: libcuda.so.1: cannot open shared object file: No such file or directory
2020-04-27 18:50:50.016819: E tensorflow/stream_executor/cuda/cuda_driver.cc:351] failed call to cuInit: UNKNOWN ERROR (303)
2020-04-27 18:50:50.016849: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (bd0bde99430b): /proc/driver/nvidia/version does not exist
2020-04-27 18:50:50.017077: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2020-04-27 18:50:50.036082: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 3301490000 Hz
2020-04-27 18:50:50.036482: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x5607a955a160 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
2020-04-27 18:50:50.036501: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): Host, Default Version
tf.Tensor(
[[3 5]
 [7 9]], shape=(2, 2), dtype=int32)
```

##### Different aproach - copy files into Docker container

Sometimes we want to execute code inside long running (with `-d` option) Docker container (ie Cassandra). In such case we need to copy file into the running Docker container and run it.

1. Run docker container in detached mode (which means that it will run until stopped), by executing: `docker run -d -p 9042:9042 --name=cassandra_test cassandra:latest`
2. Copy file, you want to execute: `docker cp cassandra.cql cassandra_test:/schema.cql`
3. Use copied file: `docker exec cassandra_test cqlsh -f /schema.cql`
