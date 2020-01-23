---
title: Running Tensorflow in Docker
date: 2020-01-21
draft: false
categories:
- tensorflow
- docker
tags:
- tensorflow
- docker
---


### If for some reasons you don't want to run Tensorflow scripts locally you can easily do this inside of Docker container.

Curently Tensorflow can be run only on Python 3.4–3.7. Upgrading or downgrading python can lead to different types of problems. Fortunatelly we can run Tensorflow scripts on Docker containers.

<br/>

First we need to create file `test_installation.py` with content which will be used to test the installation:
```
import tensorflow as tf

tensor1 = tf.convert_to_tensor([[1, 2], [3, 4]], dtype = tf.int32)
tensor2 = tf.convert_to_tensor([[2, 3], [4, 5]], dtype = tf.int32)

result = tf.add(tensor1, tensor2)

print(result)
```
<br/>

Before running this code please be aware that this will download Docker image with size around 2,5GB
```
$ docker system df -v
Images space usage:

REPOSITORY                TAG                   IMAGE ID            CREATED             SIZE                SHARED SIZE         UNIQUE SIZE         CONTAINERS
tensorflow/tensorflow     latest                9bf93bf90865        10 days ago         2.469GB             64.19MB             2.405GB      
```
<br/>

Now we can just run the script by executing this command:  
`docker run -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow python ./test_installation.py`

<br/>

Let's look closer at the generic form of the command  
`$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]`

1. Options
    - `-it` - starts container in interactive mode (actually connection of `-i` and `-t`)
    - `-rm` - clean up the container and remove the file system
    - `-v` - mounts current directory to `/tmp` directory inside docker container
    - `-w` - setting working directory to `/tmp`
2. Image - latest version of Tensorflow - `tensorflow/tensorflow`
3. Command and arguments `python ./test_installation.py`

<br/>

As a result you should see some amount of logs and result of the executed script somewhere at the bottom of the output.
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

