# README #

Documentation to successfully setup Minikube for local development

### Installation ###

* Ensure you have successfully installed [Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
* Ensure you have a successfully installed version of [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-with-homebrew-on-macos)

### How do I get set up? ###
* Download and Install [Minikube](https://kubernetes.io/docs/getting-started-guides/minikube/) on your host machine
* Download and Install [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) on your host machine
* Download and Install [Docker](https://docs.docker.com/docker-for-mac/install/) on your host machine
* Download and Install the Virtualbox driver if it's not already on your host machine
* From a terminal window run: ```pip install -r requirements.txt```   
* From a terminal window run: ```python3 bootstrap.py -f minikube-inputs.yaml```   
     - Feel free to edit the ```minikube-inputs.yaml``` file to meet your local environment's needs

### Supported YAML inputs ###
* cpu parameter - number of vCPUs
* memory parameter - amount of RAM in MBs
* action - either 'start' or 'stop'
* delete_instance - boolean
* debug - boolean

### Example minikube-inputs.yaml ###
```---
cpu: 4
memory: 8196
action: start
delete_instance: True
debug: False
``` 
