---
title: Kubernates demo on Google Cloud Platform
date: 2020-05-25
draft: true
categories:
- google cloud platform
- gcp
- kubernetes
- k8s
- kubectl
- docker
tags:
- google cloud platform
- gcp
- kubernetes
- k8s
- kubectl
- docker
---

### After playing a bit with Minikube I wanted to build something on a real Kubernetes cluster. From few Kubernetes as a Service options I've chosen Google Kubernetes Engine available on Google Cloud Platform. Below you can see how to deploy web application in few simple steps.

The full source code with instructions, how to run and test it, can be found [here](https://github.com/adrian83/gcp-samples/tree/master/001-kubernetes-demo).

#### Prerequisites

Before you start make sure, you meet the following requirements:
1. You have [Google Cloud Platform](https://cloud.google.com/) account
2. You have installed [Google Cloud Platform SDK](https://cloud.google.com/sdk)
3. You have installed [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) 

Below you can find list of properties, I used in this application. Adjust them to your needs and use them consistently in the following commands and configuration files. 
1. Project id: `adrian-gcp-k8s-demo` 
2. Region: `europe-north1`
3. Zone: `europe-north1-c` 
4. Cluster name: `k8s-demo-cluster`


#### Admin work

After that we have to do some administration work:
1. Sign in to GCP account, by executing: `gcloud auth login`
2. Create new project, by executing: `gcloud projects create adrian-gcp-k8s-demo`
3. Set few `gcloud` properties: 
  - `gcloud config set project adrian-gcp-k8s-demo`
  - `gcloud config set region europe-north1`
  - `gcloud config set zone europe-north1-c`
4. [Enable billing for newly created project](https://support.google.com/googleapi/answer/6158867?hl=en)
5. Enable required services for this project:
  - `gcloud services enable deploymentmanager.googleapis.com` (for Deployment Manager service) 
  - `gcloud services enable container.googleapis.com` (for Container service)


#### Infrastructure

Now we are ready to deploy sample application. 
We will start from defining our infrastructure. In GCP we can use Deployment Manager to build our infrastructure from code. Actually our infrastructure is only one resource - Kubernetes Cluster. Mine is created in Finland, but you should choose region, that is close to your location. Our cluster will contain 2 nodes.

```
resources:

- name: k8s-demo-cluster
  type: container.v1.cluster
  properties:
    zone: europe-north1-c      # Finland
    cluster:
      description: "k8s-demo cluster"
      initialNodeCount: 2
```

Let's place this code in file called `01-infrastructure.yml` and build it, by executing such command:  
`gcloud deployment-manager deployments create adrian-gcp-k8s-demo --config 01-infrastructure.yml` 

Our Kubernetes Cluster runs on Google Cloud Platform, but since now we can forget for a while about GSP and concentrate on K8S cluster. Tool that is used to manage K8S clusters is called `kubectl` and since now we will use it. 

Let's authenticate kubectl to manage our K8S cluster on GCP, by executing:  
`gcloud container clusters get-credentials k8s-demo-cluster --zone europe-north1-c`

Now every `kubectl` command will hit our cluster.

#### Deployment (Pods)

Let's start from deploying sample application in form of a pod(s). To do this, let's create file `02-echo-deployment.yml` with following content:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo-deployment
  labels:
    app: echo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: echo
  template:
    metadata:
      labels:
        app: echo
    spec:
      containers:
      - name: echo
        image: docker.io/adrianb83/echo:1.0.3
        ports:
        - containerPort: 8080
          protocol: TCP
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "64Mi"
            cpu: "250m"
```

I won't go into details about `Deployment` type which you can find [here](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/). The most important is, that we're deploying two replicas of `docker.io/adrianb83/echo:1.0.3` docker image. This image starts http server and returns data contained with request, such as headers, host name and body. We need to remember, that all deployed images should return status `OK` (200) under its root path.

To deploy pods, please run: `kubectl apply -f 02-echo-deployment.yml`

#### Service

If we have running pods, we need a way to expose them as a network service. To do this, we need to deploy `Service`.

Let's create file `03-echo-service.yml` with following content:

```
apiVersion: v1
kind: Service
metadata:
  name: echo
  namespace: default
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 8080
  type: NodePort
  selector:
    app: echo
```

Again, if you need details about Kubernetes Services, take a look [here](https://kubernetes.io/docs/concepts/services-networking/service/). The most important is that this Service will reroute traffic from port 80 to port 8080 on target pods and that it will use Pods that match give selector (so Pods defined above).

To deploy Service, please run: `kubectl apply -f 03-echo-service.yml`

#### Ingress

Now we should have running Service, but it is available only from our cluster. To make it visible from the internet, we need an Ingress.

Let's create file `04-echo-ingres.yml` with following content:

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: echo-ingress
spec:
  backend:
    serviceName: echo
    servicePort: 80
```

Again, if you need details about Kubernetes Ingress, take a look [here](https://kubernetes.io/docs/concepts/services-networking/ingress/). The most important is, that this ingress reroutes traffic to our service (defined above) on port 80 so exactly, as we wanted.

To deploy ingress, please run: `kubectl apply -f 04-echo-ingres.yml`

#### Testing

If you find newly created Ingress and it's IP address, you can past it into your browser and make few requests. Response will contain field `host` which should have one of two values corresponding to our replicas.

#### Cleaning

If you want to clean up, you can remove GCP project or Deployment, by executing: `gcloud deployment-manager deployments delete adrian-gcp-k8s-demo`