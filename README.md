# eksweb
A test web deploy to AWS EKS

## Build and run docker image
```
docker build -t eksweb .
docker run -d -p 8080:5000 eksweb:latest
```

Then test the app at http://localhost:8080

## Push image to dockerhub

```
docker tag eksweb:latest oxfordfun/eksweb:latest
docker push oxfordfun/eksweb:latest


## Deploy to your EKS cluster
kubectl create namespace web-apps
kubectl apply -f deployment.yaml -n web-apps
kubectl get all -n web-apps
        