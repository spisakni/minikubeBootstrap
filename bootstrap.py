#!/usr/bin/env python
__author__ = 'Nick Spisak'

import subprocess, time, argparse, yaml, os, sys
from Logger import configure_console_logger

# Create the logger config
logger = configure_console_logger(name='default')


def cmdOut(cmd):
    """Utility function for running terminal commands."""
    return subprocess.check_output(cmd, shell=True).strip()


def poll(search_string, init_interval, interval, count=None):
    """Utility function to poll status"""

    print("Starting the poller to monitor the status of the pods...")
    time.sleep(init_interval)
    creating = search_string
    counter = 0

    if count == None:
        count = 5

    while counter < count:

        while creating.find(search_string) != -1:
            creating = cmdOut("kubectl get pods -n spinnaker").decode()
            os.system("clear")
            print(creating)
            print("\nPolling the status of the pods ...")
            time.sleep(interval)

        counter += 1

    print("The poller input condition has been met...")


def is_running():
    """Check if minikube is running"""

    try:
        output = subprocess.check_output(["minikube", "status"]).decode('utf-8')
        if "Running" in output:
            return True
        else:
            return False

    except Exception as e:
        logger.error('Received the following error while checking if minikube was running: {0}'.format(e))
        return False


def start_minikube(cpu, memory):
    """Start minikube."""

    try:
        logger.info('Starting Minikube with {0} CPUs and {1} MB Memory in virtualbox...'.format(cpu, memory))
        subprocess.check_call(["minikube", "start", "--cpus", str(cpu), "--memory", str(memory)])
        logger.info('Minikube Started!')
    except Exception as e:
        logger.error('Received the following error while starting minikube: {0}'.format(e))
        return e


def stop_minikube():
    """Stop minikube."""

    try:
        logger.info('Stopping Minikube in virtualbox...')
        subprocess.check_call(["minikube", "stop"])
        logger.info('Minikube Stopped!')
    except Exception as e:
        logger.error('Received the following error while stopping minikube: {0}'.format(e))
        return e


def delete_minikube():
    """Stop any running instances"""

    try:
        stop_minikube()
        logger.info('Deleting Minikube in virtualbox...')
        subprocess.check_call(["minikube", "delete"])
    except Exception as e:
        logger.error('Received the following error while deleting minikube: {0}'.format(e))
        return e


def create_kube_config():
    ip = os.popen('minikube ip').read().strip()

    certificate_authority = os.popen("openssl base64 -in ~/.minikube/ca.crt | tr -d \'\n\'").read().strip()
    client_certificate = os.popen("openssl base64 -in ~/.minikube/client.crt | tr -d \'\n\'").read().strip()
    client_key = os.popen("openssl base64 -in ~/.minikube/client.key | tr -d \'\n\'").read().strip()

    kubeConfig = """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: """ + certificate_authority + """
    server: https://""" + ip + """:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate-data: """ + client_certificate + """
    client-key-data: """ + client_key + """
"""
    try:
        logger.info('Creating the .kube config file...')
        with open("config", "w") as text_file:
            text_file.write(kubeConfig)

        logger.info('Overwriting the existing kube config file with the new one...')
        os.popen('mv config ~/.kube/config').read().strip()

        logger.info('Copying the necessary keys to the /opt/secure/ directory on your host machine...')
        os.popen('cp ~/.minikube/ca.crt /opt/secure/ca.crt')
        os.popen('cp ~/.minikube/client.crt /opt/secure/client.crt')
        os.popen('cp ~/.minikube/client.key /opt/secure/client.key')
    except Exception as e:
        logger.error('Received the following error while building the kube config file: {0}'.format(e))
        return e

    time.sleep(1)


# ----------------- MAIN ------------------- #
# Logic to instantiate the main() function and run as a script
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Bootstrap a minikube environment for local development.")
    parser.add_argument('-f', action="store", help='Absolute path to the input YAML file.', required=True)
    args = parser.parse_args()

    try:
        with open(args.f) as file:
            user_input = yaml.safe_load(file)
    except Exception as e:
        print("Experienced the following error while attempting to the read the input YAML file: {0}".format(e))
        sys.exit(1)

    if not 'cpu' in user_input:
        print("The \"cpu\" parameter is a required parameter in the input YAML file! Exiting...")
        sys.exit(1)
    if not 'memory' in user_input:
        print('The \"memory\" parameter is a required parameter in the input YAML file! Exiting...')
        sys.exit(1)

    try:
        running = is_running()
        if 'delete_instance' in user_input:
            if user_input['delete_instance'] == True:
                delete_minikube()
        if 'action' in user_input:
            if user_input['action'].lower() == 'start':
                if running == False:
                    start_minikube(cpu=user_input['cpu'], memory=user_input['memory'])
                    create_kube_config()
                elif running == True:
                    stop_minikube()
                    start_minikube(cpu=user_input['cpu'], memory=user_input['memory'])
                    create_kube_config()
            if user_input['action'].lower() == 'stop':
                if running == True:
                    stop_minikube()
    except Exception as e:
        print("Experienced the folllowing error: {0}".format(e))
        sys.exit(1)
