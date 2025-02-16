from celery import Celery

cl_app = Celery(
    'jobsearchit',
    broker='redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060',
    backend='redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060'
)


