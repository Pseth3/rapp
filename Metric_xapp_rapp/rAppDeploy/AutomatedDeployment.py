from datetime import datetime
import os
import time
import sys

try:
    filepath = sys.argv[1]
except:
    print('You have not specified the persistent path')
    print('Seting meassuremnt file as - "/tmp/rAppMeassurements.txt" ')
    filepath=r'/tmp/rAppMeassurements.txt'

val_dict = {}
val_dict['CPU_main'] = os.cpu_count()
val_dict['RAM_main:'] =(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')//(1024.**3))
# Create a docker image
doc_start = datetime.now()
os.system('eval $(minikube docker-env) && docker build --tag rapp-docker .')
# os.system('docker build --tag rapp-docker')
doc_time = datetime.now()-doc_start
val_dict['ImageCreationTime'] = doc_time.total_seconds()
print('DockerCreateTiem',doc_time.total_seconds())
# Create namespace
os.system('minikube kubectl -- create namespace rapp')
# os.system('kubectl create namespace rapp')



Pod_start_time = datetime.now()
#os.system('sleep 1')
os.system('minikube kubectl -- create -f testrapp.yaml')
Pod_end_time = datetime.now()
Pod_comput_time = Pod_end_time-Pod_start_time
val_dict['PodCreationTime']=Pod_comput_time.total_seconds()
print('PodCreation',float(Pod_comput_time.total_seconds()))
# print(Pod_start_time)
# print(Pod_end_time)

# Get the pod ID
podname = str(os.popen('minikube kubectl -- get pods -o=name | grep rapp | sed "s/^.\{4\}//" ').read())
# print(podname.strip())

# print and parse the logs of the pod
cmd = 'minikube kubectl -- logs  {0} '.format(podname.strip())
# print(cmd)
time.sleep(3)
logs = os.popen(cmd).read()
time.sleep(1)
print(logs)
for l in logs.splitlines():
    if 'CPU' in l or 'RAM' in l or 'Predict_time' in l:
        val_dict[l.split(':')[0].strip()]=l.split(':')[1].strip()
print(val_dict)

# logs = ('kubectl logs  {} -n rapp '.format(podname))



# delete pod
os.system('minikube kubectl -- delete -f testrapp.yaml')

# delete namespace
os.system('minikube kubectl -- delete namespace rapp')
# os.system('kubectl delete namespace rapp')

# Append to file
with open(filepath, "a") as myfile:
    myfile.write(str(val_dict))

print('All done!')

