---
title: Kubernates demo on gcp
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



1. Sign in to GCP by executing: `gcloud auth login`

2. Create new project
New project can be created through web console or by executing this command: `gcloud projects create <unique-project-id>`, in my case it will be: `gcloud projects create adrian-gcp-k8s-demo`

3. Make newly created project your main project
Run `gcloud config set project adrian-gcp-k8s-demo`.

4. [Enable billing for newly created project](https://support.google.com/googleapi/answer/6158867?hl=en)

5. Enable required services for this project
Enable Deployment Manager service, by executing this command: `gcloud services enable deploymentmanager.googleapis.com`
Enable Container service, by executing this command: `gcloud services enable container.googleapis.com`

6. Create (or update) project's infrastructure
To create project, execute: gcloud deployment-manager deployments create adrian-gcp-k8s-demo --config 01-infrastructure.yml

If you want to update existing infrastructure, execute: gcloud deployment-manager deployments update adrian-gcp-k8s-demo --config 01-infrastructure.yml

7. Switch from using gloud to kubectl
Get credentials from GCP, so that you can use your local kubectl to manage K8S cluster: `gcloud container clusters get-credentials k8s-demo-cluster --zone <zone-near-you>` in my case it's `gcloud container clusters get-credentials k8s-demo-cluster --zone europe-north1-c`

8. Create deployment (pods)
Execute: `kubectl apply -f 02-echo-deployment.yml`

9. Create service (loadbalancer)
Execute: `kubectl apply -f 03-echo-service.yml`

10. Create ingres
Execute: `kubectl apply -f 04-echo-ingres.yml`

11. Clean up
Remove deployment with Kubernetes cluster, by executing this command: `gcloud deployment-manager deployments delete adrian-gcp-k8s-demo`