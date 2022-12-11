from requests import request
from datetime import datetime as dt
from multiprocessing import Process
import os
import pandas as pd
from multiprocessing import Manager

'''
    This function is responsible to send 
    Throughput requirements to the rAPP
'''
def o1Call(slice_1):
    slice ={'slice_1':slice_1,
            'slice_2':0,
            'slice_3':0,
            'first_responder':'NO'}
    slice=str(slice)
    res = request("POST","http://38.68.234.107:41000/slices",data=slice)


'''
    This fuction triggers the IPERF3 command
    Make sure the machine has IPERF3 installed and run script
    as sudo - change the delay in the iperf command
'''
def runIperf3(throughput,data_dict):
    logs = os.popen('iperf3 -c  127.0.0.1 -p 5023 -i 1 -t 5 -b'+str(throughput)+'M '+'-T $(date "+%H:%M:%S ") ' ).read()
    data_dict[str(throughput)]=logs
    data_dict['PID']=os.getppid()



'''
    This is where the main function starts
    It uses multiprocesses to start the 
    IPERF and o1 interface together
'''
if __name__ == '__main__':
    slice_throughput = [3,4,7]
    df = pd.DataFrame(columns=['start_time','Throughput','logs'])

    for t in slice_throughput:
        manager= Manager()
        data_dict = manager.dict()
        p1 = Process(target=o1Call, args=(t,))  
        p2 = Process(target=runIperf3, args=(t,data_dict,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        p1.close()
        p2.close()
        # os.system('kill -9 '+str(data_dict['PID']))
        df.loc[len(df)]=[str(dt.now()),t,data_dict[str(t)]]
    
    # with open('output.csv','a') as f:
    #     f.write(str(df) +str('\n'))

    df.to_csv('UE_metic.csv',mode='a',header = False)
