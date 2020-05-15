---
title: Kubernates demo on Google Cloud Platform
date: 2020-04-10
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

### After playing a bit with Minikube I wanted to build something on a real Kubernetes cluster. From few Kubernetes as a Service options I've choosed Google Kubernetes Engine available on Google Cloud Platform. Below you can see how to deploy web application in few simple steps.

The full source code with instructions, how to run and test it, can be found [here](https://github.com/adrian83/gcp-samples/tree/master/001-kubernetes-demo).

Before you start make sure you meet the following requirements:
1. You have [Google Cloud Platform](https://cloud.google.com/) account
2. You have installed [Google Cloud Platform SDK](https://cloud.google.com/sdk)
3. You have installed [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) 


After that we have to do some administation work:
1. Sign in to GCP account by executing: `gcloud auth login`
2. Run `gcloid init`
3. Create new project by executing this command: `gcloud projects create <unique-project-id>`, in my case it will be: `gcloud projects create adrian-gcp-k8s-demo`
4. [Enable billing for newly created project](https://support.google.com/googleapi/answer/6158867?hl=en)
5. Enable required services for this project by executing this commands: `gcloud services enable deploymentmanager.googleapis.com` (for Deployment Manager service) and `gcloud services enable container.googleapis.com` (for Container service)


Now we are ready to deploy sample application. 
We will start from creating an infrastructure. In GCP we can use Deployment Manager to build our infrastructure from code (file called `01-infrastructure.yml`). Actually our infrastructure is only one resource - Kubernetes Cluster. Mine is created in Finland but you should choose zone that is close to your location. Our cluster will contain 2 nodes.

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

Building our infrastructure will require executing such command:  
`gcloud deployment-manager deployments create adrian-gcp-k8s-demo --config 01-infrastructure.yml` 

After some time your Kubernetes cluster should be ready. 
Now we can switch from using gcloud to kubectl. To do this execute this command:  
`gcloud container clusters get-credentials k8s-demo-cluster --zone europe-north1-c`

Lets start with deploying some pods in our cluster. 

`02-echo-deployment.yml`

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

I won't go into details which you can find [here](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/). The most important is that we are deloying two replicas of `docker.io/adrianb83/echo:1.0.3` docker image. You should also 

`03-echo-service.yml`

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



`04-echo-ingres.yml`

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

If you want to clean up you can remove GCP project or Deployment by executing: `gcloud deployment-manager deployments delete adrian-gcp-k8s-demo`