from requests import request
from datetime import datetime as dt
from multiprocessing import Process
from multiprocessing import Manager
import os
# import pandas as pd

def runIperf3(throughput):
    logs = os.popen('iperf3 -c  127.0.0.1 -p 5023 -i 1 -t 5 -b'+str(throughput)+'M '+'-T $(date "+%H:%M:%S ") ' ).read()
    data_dict[str(throughput)]=logs
    data_dict['PID']=os.getppid()



if __name__ =='__main__':
    t = 15
    manager= Manager()
    data_dict = manager.dict()
    
    # p1 = Process(target=o1Call, args=(t,))  
    p2 = Process(target=runIperf3, args=(t,))
    # p1.start()
    p2.start()
    p2.join()
    p2.close()
    print(data_dict['PID'])
    # os.system('kill -9 '+str(data_dict['PID']))
    # df.iloc[len(df),:]=
    print(data_dict[str(t)])
    # print([dt.now(),t,data_dict[t]])