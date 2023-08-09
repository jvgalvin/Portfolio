# Sentiment Classifier on Azure Kubernetes Service

This FastAPI application has the following endpoints:
1. "/predict" - uses a fine-tuned DistilBERT model to classify sentiment. This endpoint expects a list of strings (see below for ann example) and returns a list of predictions. Each request to this endpoint is cached in Redis.
2. "/docs" - serves interactive FastAPI documentation and is browsable while the application is running 
3. "/openapi.json" - returns a json object with information from the application's .openapi() method (i.e., version of the API, etc.).
4. "/health" - returns "healthy" when reachable

### Model
The [DistilBERT model](https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2) took 5 minutes to transfer learn on the glue dataset on 2x A4000 GPUs with a 256 batch size, taking 15 GB of memory on each GPU. Given the inefficiency associated with pulling the model (256MB) directly from HuggingFace, it is pulled down locally as part of the build process (model files are excluded from this repo given their size).

### Deploy Locally
To make changes or develop the application locally, use minikube. Follow the below commands from within the mlapi directory.

    minikube start --kubernetes-version=v1.25.4
    eval $(minikube docker-env)
    kubectl config use-context minikube

    docker build -t project .
    kubectl apply -f ../.k8s/bases/namespace.yaml
    kubectl kustomize ../.k8s/dev
    kubectl apply -k ../.k8s/dev
    kubectl port-forward service/project -n jgalvin 8000:8000

Use the following command to hit the /predict endpoint of the application, which should be running on localhost:8000.

    curl -X POST -H "Content-Type: application/json" localhost:8000/predict -d '{"text": ["This is fun", "the movie was awful"]}'


### Deploy to AKS
To deploy the application within Kubernetes on Azure, run the following commands from within the mlapi directory.

    # Switch context and login (requires credentials)
    kubectl config use-context w255-aks
    az acr login --name w255mids

    # Build, tag, and push image
    docker build --platform linux/amd64 -t project:some_tag .
    docker tag project:some_tag w255mids.azurecr.io/jgalvin/project:some_tag
    docker push w255mids.azurecr.io/jgalvin/project:some_tag
    docker pull w255mids.azurecr.io/jgalvin/project:some_tag

    # Deploy to AKS
    kubectl apply -f ../.k8s/bases/namespace.yaml
    kubectl kustomize ../.k8s/prod
    kubectl apply -k ../.k8s/prod

Alternatively, you could use the build-push.sh script. To do so, follow these steps.

    # Switch context and login (requires credentials)
    kubectl config use-context w255-aks

    # Automatically builds, tags, and pushes image with latest git hash
    sh build-push.sh

    # Deploy to AKS
    kubectl apply -f ./.k8s/bases/namespace.yaml
    kubectl kustomize ./.k8s/prod
    kubectl apply -k ./.k8s/prod

Use the following command to hit the /predict endpoint of the application, which is running in AKS.

    curl -X POST -H "Content-Type: application/json" "https://jgalvin.mids255.com/predict" -d '{"text": ["This is fun", "the movie was awful"]}'
    
Note: The API will not accept a blank request (i.e., you must pass something, even if it is a blank string).

### Performance

Select load testing was performed against the /predict endpoint in AKS using K6. Traffic was ramped up from 1 to 10 users over the first 30 seconds, sustained at 10 users for 7 minutes, and then ramped down to 0 users over the last 30 seconds. Testing was done with a cache hit rate of 0.95 over a gigabit fiber wifi connection. Data from the test was logged in Prometheus and analyzed within Grafana. Select screenshots of the Istio service and workload dashboards are included below.

![Istio Service](https://github.com/UCB-W255/summer23-jvgalvin/blob/main/final_project/assets/service.png)

![Istio Workload](https://github.com/UCB-W255/summer23-jvgalvin/blob/main/final_project/assets/workload.png)
