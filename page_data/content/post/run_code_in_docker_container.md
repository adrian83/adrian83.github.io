---
title: Run code in Docker container
date: 2020-01-21
draft: true
categories:
- tensorflow
- docker
- python
tags:
- tensorflow
- docker
- python
---

Some time ago I was trying to run examples from Tensorflow tutorial. I've prepared virtual environment (with Virtualenv) but when downloading required dependecnies it occured that verion of python installed on my computer is unsopported by Tensorflow. I thought that updating python is too much. Fortunately Tensorflow team prepared Docker images that can be used to run scripts. 


First let's look at the generic form of the command for running Docker containers:  
`$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]`

Runnign simple script that will test if Tensorflow is installed properly would require executing this command:  
`docker run -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py`

Let's explain what each element of this command means:  <br/>

1. Options:
    - `-it` - starts container in interactive mode (actually connection of `-i` and `-t`), in simple worlds it means that information from executed script will be printed on your terminal  
    - `-rm` - cleans up the container and remove the file system   
    - `-v` - mounts current directory to `/tmp` directory inside docker container  
    - `-w` - setting working directory to `/tmp`  
2. Image:  
    -  `tensorflow/tensorflow` - latest version of Tensorflow image
3. Command and arguments:
    - `python ./test_installation.py`

<br/>

Before running this code please be aware that this will download Docker image with size around 2,5GB
```
$ docker system df -v
Images space usage:

REPOSITORY              TAG      IMAGE ID       SIZE      SHARED SIZE   UNIQUE SIZE 
tensorflow/tensorflow   latest   9bf93bf90865   2.469GB   64.19MB       2.405GB  
```

<br/>

Testing Tensorflow installation (content of `test_installation.py`) can be anything that is using Tensorflow. In my case it is something like this:
```
import tensorflow as tf

tensor1 = tf.convert_to_tensor([[1, 2], [3, 4]], dtype = tf.int32)
tensor2 = tf.convert_to_tensor([[2, 3], [4, 5]], dtype = tf.int32)

result = tf.add(tensor1, tensor2)

print(result)
```

<br/>

As a result I received some amount of logs and result of the executed script somewhere at the bottom of the output.
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

