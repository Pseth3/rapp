import iperf3
import pandas as pd
import os
from subprocess import Popen
from multiprocessing import Process
from requests import request

# Read manual Data
throughput_df = pd.read_csv(os.path.join(os.getcwd(),"throughput.csv"),header=0)

# Initiate the 2 UE clients
client1 = iperf3.Client()
client1.duration = 35
client1.server_hostname = '38.68.232.201' #'172.16.0.2'
client1.port = 5022
client1.protocol = 'tcp' # 'udp'

client2 = iperf3.Client()
client2.duration = 35
client2.server_hostname = '38.68.232.77' #'172.16.0.3'
client2.port = 5022
client2.protocol = 'tcp' # 'udp'

def ping(client):
    print("starting process")
    client.run()

def o1Call(slice_1,slice_2,slice_3):
    # O1 implemetation
    var = os.getenv('IS_PRESENT')
    data = {'slice_1':throughput_df.loc[i,'slice_1'],
            'slice_2':throughput_df.loc[i,'slice_2'],
            'slice_3':throughput_df.loc[i,'slice_3'],
            'first_responder':var}
    res = request("POST","http://38.68.234.107/slices",data = data)


if __name__=="__main__":

    print('Connecting to {0}:{1} and {2}:{3}'.format(client1.server_hostname, client1.port,client2.server_hostname, client2.port))
    while True:
        for i in range(len(throughput_df)):
            print("New throughput",throughput_df.loc[i,'slice_1'],throughput_df.loc[i,'slice_2'])
            client1.blksize = throughput_df.loc[i,'slice_1']
            client2.blksize = throughput_df.loc[i,'slice_2']

            p1 = Process(target=ping,args=(client1,))
            p2 = Process(target=ping,args=(client2,))
            p3 = Process(target=o1Call,args=(throughput_df.loc[i,'slice_1'],throughput_df.loc[i,'slice_2'],throughput_df.loc[i,'slice_3'],))
            # p2 = Process(target=client2.run())
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()