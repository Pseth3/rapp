import os
from requests import request
import json
import sys
from time import sleep
# New script
SLEEPINT=5
GLOBAL_POLICY=1
SLICE1 = 0
SLICE2 = 0



print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))


NEXRAN_XAPP=os.popen("sudo kubectl get svc -n ricxapp --field-selector metadata.name=service-ricxapp-nexran-rmr -o jsonpath='{.items[0].spec.clusterIP}'").read()
KONG_PROXY=os.popen("sudo kubectl get svc -n ricplt -l app.kubernetes.io/name=kong -o jsonpath='{.items[0].spec.clusterIP}'").read()

SETUP_URL = "http://{}:8000/v1/nodebs".format(NEXRAN_XAPP)
print(NEXRAN_XAPP,KONG_PROXY,SETUP_URL)
SETUP_EXISTS= request ("GET",SETUP_URL,headers = {'Accept': 'application/json'},data= {})
nodebs=json.loads(SETUP_EXISTS.text)
print(nodebs)

if len(nodebs['nodebs'])==0:
    print("currently no nodebs exist")
else:
    print("the following nodebs exist")
    for i in range(len(nodebs)):
        print(nodebs['nodebs'][i]['name'])

sleep(SLEEPINT)


def enbA():
    # curl -i -X POST -H "Content-type: application/json" -d '{"type":"eNB","id":411,"mcc":"101","mnc":"010"}' http://${NEXRAN_XAPP}:8000/v1/nodebs
    res = request("POST","http://{}:8000/v1/nodebs".format(NEXRAN_XAPP),data='{"type":"eNB","id":411,"mcc":"101","mnc":"01"}')
    print("enb added")
    sleep(SLEEPINT)



def enbD(name:str):
    pass

def slice1A(share=64):
    # curl -i -X POST -H "Content-type: application/json" -d '{"name":"fast","allocation_policy":{"type":"proportional","share":1024}}' http://${NEXRAN_XAPP}:8000/v1/slices ; echo ; echo
    print('Creating Slice1')
    sleep(SLEEPINT)
    res = request("POST","http://{}:8000/v1/slices".format(NEXRAN_XAPP),data='{"name":"slice1","allocation_policy":{"type":"proportional","share":50}}')

    print("binding slice1 to enb")
    # curl -i -X POST http://${NEXRAN_XAPP}:8000/v1/nodebs/enB_macro_101_010_0019b0/slices/slow 
    res = request("POST","http://{}:8000/v1/nodebs/enB_macro_101_001_0019b0/slices/slice1".format(NEXRAN_XAPP))
    sleep(SLEEPINT)

def slice2A(share=1024):
    print("Creating slice2")
    res = request("POST","http://{}:8000/v1/slices".format(NEXRAN_XAPP),data='{"name":"slice2","allocation_policy":{"type":"proportional","share":50}}')
    sleep(SLEEPINT)

    print("binding slice2 to enb")
    res = request("POST","http://{}:8000/v1/nodebs/enB_macro_101_001_0019b0/slices/slice2".format(NEXRAN_XAPP))
    sleep(SLEEPINT)

def sliceDslow():
    pass

def sliveDfast():
    pass

def ueA1():
    # curl -i -X POST -H "Content-type: application/json" -d '{"imsi":"101010123456789"}' http://${NEXRAN_XAPP}:8000/v1/ues
    print("Creating UE 101010123456789")
    res = request("POST","http://{}:8000/v1/ues".format(NEXRAN_XAPP), data = '{"imsi":"101010123456789"}')
    sleep(SLEEPINT)
    print("binding ue 101010123456789 to slice1")
    # curl -i -X POST http://${NEXRAN_XAPP}:8000/v1/slices/fast/ues/101010123456789
    res = request("POST","http://{}:8000/v1/slices/slice1/ues/101010123456789".format(NEXRAN_XAPP))
    sleep(SLEEPINT)

def ueA2():
    # curl -i -X POST -H "Content-type: application/json" -d '{"imsi":"101010123456787"}' http://${NEXRAN_XAPP}:8000/v1/ues
    print("Creating UE 101010123456787")
    res = request("POST","http://{}:8000/v1/ues".format(NEXRAN_XAPP), data = '{"imsi":"101010123456787"}')
    sleep(SLEEPINT)
    print("binding ue 101010123456787 to slice2")
    # curl -i -X POST http://${NEXRAN_XAPP}:8000/v1/slices/slice1/ues/101010123456789
    res = request("POST","http://{}:8000/v1/slices/slice2/ues/101010123456787".format(NEXRAN_XAPP))
    sleep(SLEEPINT)

def ueD1():
    pass

def ueD2():
    pass

def switchSlice(S1,S2):
    # curl -X PUT   http://${NEXRAN_XAPP}:8000/v1/slices/slow  -H 'accept: */*'  -H 'Content-Type: application/json'  -d '{"allocation_policy": {"type": "proportional","share": 64}}'
    data = '{"allocation_policy": {"type": "proportional","share":'+str(S1)+'}}'
    res = request("PUT","http://{}:8000/v1/slices/slice1".format(NEXRAN_XAPP),data=data)
    sleep(SLEEPINT)

    # curl -X PUT   http://${NEXRAN_XAPP}:8000/v1/slices/fast  -H 'accept: */*'  -H 'Content-Type: application/json'  -d '{"allocation_policy": {"type": "proportional","share": 1024}}'
    data = '{"allocation_policy": {"type": "proportional","share":'+str(S2)+'}}'
    res = request("PUT","http://{}:8000/v1/slices/slice2".format(NEXRAN_XAPP),data=data)
    sleep(SLEEPINT)




if __name__=="__main__":

    while True:
        try:
            session= request("GET","http://{}:32080/a1mediator/a1-p/policytypes/22000/policies".format(KONG_PROXY)).text
            temp=json.loads(session)[0]
            break
        except:
            pass

    while True:

        try:
            RESP = request("GET","http://{}:32080/a1mediator/a1-p/policytypes/22000/policies/{}".format(KONG_PROXY,temp))
            POL=json.loads(RESP.text)['policy_conf']
            S1=json.loads(RESP.text)['slice_1']
            S2=json.loads(RESP.text)['slice_2']
           #  GLOBAL_POLICY = 0
           #  enbA()
           # slice2A()
           #  slice1A()
           #  ueA1()
           #  ueA2()

        except:
            sleep(2)
            continue

        if S1 != SLICE1 or  S2!=SLICE2:
            print("New proportions",S1,S2)
            SLICE1 = S1
            SLICE2 = S2
            switchSlice(S1,S2)
            print("Slice Changed")


        if POL == '0' and GLOBAL_POLICY != 0:
            GLOBAL_POLICY = 0
            enbA()
            slice2A()
            slice1A()
            ueA1()
            ueA2()