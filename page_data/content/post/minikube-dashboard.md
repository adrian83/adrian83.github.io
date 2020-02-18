---
title: Running Dashboard in Minikube
date: 2019-12-22
draft: false
categories:
- kubernetes
- k8s
- minikube
- dashboard
tags:
- kubernetes
- k8s
- minikube
- dashboard
---


### To install and access Kubernetes Web UI (called Dashboard), you need to go through few simple steps.


Make sure your Minikube cluster is started by running `k8s-samples`.  
If it is not running start it with `minikube start`.

Create file `dashboard-adminuser.yaml` with content:
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

Create file `dashboard-clusterrolebinding.yaml` with content:
```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

Apply both files by executing:  
`kubectl apply -f dashboard-adminuser.yaml`  
`kubectl apply -f dashboard-clusterrolebinding.yaml`


Install Dashboard:  
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml`

Run kubectl in a reverse proxy mode (it handles locating the apiserver and authenticating):
`kubectl proxy`

Open dashboard:  
`http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/.`

Obtain token by executing:  
`kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')`

Use token contained in response, to sign in.
