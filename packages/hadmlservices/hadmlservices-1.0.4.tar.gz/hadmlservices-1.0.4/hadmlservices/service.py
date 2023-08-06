import os
import sys
import urllib
from subprocess import call
import time
from hadmlservices import model_runtime

AWS_REGION = "us-east-1"

def update(key, message):
    print message
    model_runtime.update_job(key, message)


def user_data(root_dir,
              input_s3,
              output_s3,
              model_params):

    update("job_state", "creating input and output dirs")
    for x in [root_dir + "/input", root_dir + '/output']:
        if not os.path.exists(x):
            os.mkdir(x, 0777)
        os.chmod(x, 0777)    

    update("job_state", "downloading log agent")
    agent = root_dir + '/awslogs-agent-setup.py'
    url = ("https://s3.amazonaws.com/aws-cloudwatch/" +
           "downloads/latest/awslogs-agent-setup.py")
    f = urllib.URLopener()
    f.retrieve(url, agent)

    update("job_state", "launching log agent")
    os.chmod(agent, 0700)
    path = os.path.dirname (os.path.abspath (__file__))
    call([agent, "-n", "-r", AWS_REGION, "-c", path + "/awslogs.conf"])

    update("job_state", "copying input data")
    update("started", time.strftime('%Y-%m-%d %H:%M:%S'))
    call(["aws", "s3", "sync", input_s3, root_dir + "/input"])

    update("job_state", "executing run_script")
    call([root_dir + "/run_script",
         root_dir + "/input",
         root_dir + "/output",
         model_params])

    update("job_state", "copying output data")
    call(["aws", "s3", "sync", root_dir + "/output", output_s3])

    update("job_state", "finished")
    update("finished", time.strftime('%Y-%m-%d %H:%M:%S'))
    '''
    time.sleep(10)
    # get instance id from aws
    url = "http://169.254.169.254/latest/meta-data/instance-id"
    instance_id = urllib.urlopen(url).read()
    call(["aws",
          "ec2",
          "terminate-instances",
           "--instance-ids", instance_id, 
           "--region", AWS_REGION])
    '''
