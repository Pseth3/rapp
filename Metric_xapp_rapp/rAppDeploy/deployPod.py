from datetime import datetime
import os
start_time = datetime.now()
#os.system('sleep 1')
os.system('minikube kubectl -- create -f testrapp.yaml')
end_time = datetime.now()
comput_time = end_time-start_time
print('time taken',float(comput_time.total_seconds()))
print(start_time)
print(end_time)
