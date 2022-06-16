from kubernetes import client
from kubernetes.client import ApiClient
import json
from kubernetes.client.rest import ApiException

def __get_kubernetes_batchv1client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.BatchV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_job(client_output):
        temp_dict={}
        temp_list=[]
        
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        if len(json_data["items"]) != 0:
            for job in json_data["items"]:
                temp_dict={
                    "job": job["metadata"]["name"],
                    "namespace": job["metadata"]["namespace"]
                    #"status": job["status"]["phase"]
                }
                temp_list.append(temp_dict)
        return temp_list

def __format_data_for_create_job(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list


def get_jobs(cluster_details,namespace="default",all_namespaces=True):
        client_api= __get_kubernetes_batchv1client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            job_list =client_api.list_job_for_all_namespaces(watch=False)
            data=__format_data_for_job(job_list)
            print("Jobs under all namespaces: {}".format(data))
            # return data
        else:
            job_list = client_api.list_namespaced_job(namespace)
            data=__format_data_for_job(job_list)
            print("jobs under namespaces {}: {}".format(namespace,data))
            # return data


def create_job_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="pi",
        image="perl",
        command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="job1"),
        spec=spec)

    return job


def create_job(cluster_details,job,namespace):
  
    try:
        client_api= __get_kubernetes_batchv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.create_namespaced_job(
        body=job,
        namespace=namespace)

        data=__format_data_for_create_job(resp)
        print("Job created. status='%s'" % str(data))
    except ApiException as e:
        print("ERROR IN create_job:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_job(e.body)


def delete_job(cluster_details,k8s_object_name=None,namespace="default"):
 
    try:
        client_api= __get_kubernetes_batchv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.delete_namespaced_job(
                name=k8s_object_name,
                namespace="{}".format(namespace),
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=5)
            )

        data=__format_data_for_create_job(resp)
        print("Job deleted. status='%s'" % str(data))
    except ApiException as e:
        print("ERROR IN delete_job:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_job(e.body)


def update_job(cluster_details,job,k8s_object_name=None,namespace="default"):
   
    try:
        client_api= __get_kubernetes_batchv1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        
        job.spec.template.spec.containers[0].image = "perl"
        resp = client_api.patch_namespaced_job(
            name=k8s_object_name,
            namespace="default",
            body=job)

        data=__format_data_for_create_job(resp)
        print("Job updated. status='%s'" % str(data))

    except ApiException as e:
        print("ERROR IN update_job:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_job(e.body)


if __name__ == '__main__':
    cluster_details={
        "bearer_token":"GKE-Bearer-Token",
        "api_server_endpoint":"Ip-k8s-control-plane"
    }
    job = create_job_object()

    # get_jobs(cluster_details)

    create_job(cluster_details,job,"default")

    # update_job(cluster_details,job,k8s_object_name="job1",)


    # delete_job(cluster_details,k8s_object_name="pi",)

