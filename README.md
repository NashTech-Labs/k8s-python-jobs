# jobs
#### Python client for the kubernetes API

we can use the client module to interact with the resources. 

`CreateResources:` kubectl get commands are used to create job using yaml file in a cluster for eg:

To create the namespaces in the cluster, we fire following kubectl command:

```kubectl apply -f job.yaml``` 

List the jobs in default namespace

`kubectl get jobs`

But In Python, we instantiate BatchV1Api class from client module:

`client_api = client.BatchV1Api()`

Here I've created the client with it's respective class BatchV1Api
and storing in a var named as client_api. so furture we can use it.

`KubeConfig:` to pass the on local cluster e.g minikube we use bellowcommand: 

`config. load_kube_config()`

#### Authenticating to the Kubernetes API server

But what if you want to list all the automated cronjobs of a GKE Cluster, you must need to authenticate the configuration

`configuration.api_key = {"authorization": "Bearer" + bearer_token}` 

I've used Bearer Token which enable requests to authenticate using an access key.

#### Create the job:

Call the funcation  create_job(cluster_details,job,"default")

And replace default with any name of the namespace you want to create.

And run following command:

`python3 job.py`

#### get the list of jobs:

call the funcation  get_jobs(cluster_details)

`python3 job.py`

### update the job:

call the funcation update_job(cluster_details,job,k8s_object_name="job1",)

And replace "job1 with any name of the job you want to update.

`python3 job.py`

#### delete the job:

call the funcation delete_job(cluster_details,k8s_object_name="pi",)

And replace "pi" with any name of the namespace you want to delete.

`python3 job.py`
