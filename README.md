# eksweb
A test web deploy to AWS EKS

## Run locally
```shell
git clone https://github.com/oxfordfun/eksweb.git
cd eksweb
python3 -m venv env
source env/bin/activate
pip3 install -r requirement.txt
FLASK_PORT=8080 FLASK_DEBUG=False python3 app.py
```
Then test the app at http://localhost:8080

## Build and run docker image
```shell
docker build -t eksweb .
docker run -d -p 8080:5000 -e FLASK_PORT=5000 -e FLASK_DEBUG=False eksweb:latest
```

Then test the app at http://localhost:8080

## Push image to dockerhub

```shell
docker tag eksweb:latest oxfordfun/eksweb:latest
docker push oxfordfun/eksweb:latest
```

## Deploy to your EKS cluster
```shell
kubectl create namespace web-apps
kubectl apply -f deployment.yaml -n web-apps
kubectl get all -n web-apps
```

## Security setup

### Set up RBAC
```shell
kubectl apply -f rbac-setup.yaml
```

### Generate certificate
```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=oxfordfun.kube" -addext "subjectAltName=DNS:oxfordfun.kube"
```
### Create secret
```shell
kubectl create secret tls web-app-tls --cert=tls.crt --key=tls.key -n web-apps
```
### Deploy ingress server
```shell
kubectl apply -f ingress.yaml
```
### Verify 
```shell
kubectl get svc eksweb-service -n web-apps
kubectl get endpoints eksweb-service -n web-apps
```
### Restart ingress controller
```shell
kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx
```