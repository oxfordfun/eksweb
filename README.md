# eksweb
A test web deploy to AWS EKS

## Build and run docker image
```shell
docker build -t eksweb .
docker run -d -p 8080:5000 eksweb:latest
```

Then test the app at http://localhost:8080

## Push image to dockerhub

```shell
docker tag eksweb:latest oxfordfun/eksweb:latest
docker push oxfordfun/eksweb:latest


## Deploy to your EKS cluster
kubectl create namespace web-apps
kubectl apply -f deployment.yaml -n web-apps
kubectl get all -n web-apps


## Security setup

### Set up RBAC
```shell
kubectl apply -f rbac-setup.yaml

### Generate certificate
```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=oxfordfun.local" -addext "subjectAltName=DNS:oxfordfun.local"

### Create secret
```shell
kubectl create secret tls web-app-tls --cert=tls.crt --key=tls.key -n web-apps

### Deploy ingress server
```shell
kubectl apply -f ingress.yaml

### Verify 
```shell
kubectl get svc eksweb-service -n web-apps
kubectl get endpoints eksweb-service -n web-apps

### Restart ingress controller
```shell
kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx
