import pandas as pd
import numpy as np 
import pickle
import random
from datetime import datetime

df = pd.DataFrame(columns=['S.no','Time','S1','S2','S3','FirstResponder','Proportion_S1','Proportion_S2','Proportion_S3'])

# load the model from disk
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

for i in range(5):
    S1 = random.randint(0,300)
    S2 = random.randint(0,300)
    S3 = random.randint(0,300)
    is_present = bool(random.getrandbits(1))
    start_time = datetime.now()

    if not is_present:
        slice_1_prop =int( loaded_model.predict([[S1,S2]])[0]*100)
        slice_2_prop = 100-slice_1_prop
        slice_3_prop = 0
        comput_time = datetime.now()-start_time
        df.loc[len(df)]=[len(df),comput_time.total_seconds(),S1,S2,S3,is_present,slice_1_prop,slice_2_prop,slice_3_prop]
    else:
        slice_3_prop = int( loaded_model.predict([[S3,(S1+S2)]])[0]*100)
        slice_1_prop = int(((100-slice_3_prop)/100) * (int( loaded_model.predict([[S1,S2]])[0]*100)))
        slice_2_prop = int(100-(slice_1_prop+slice_3_prop))
        comput_time = datetime.now()-start_time
        df.loc[len(df)]=[len(df),comput_time.total_seconds(),S1,S2,S3,is_present,slice_1_prop,slice_2_prop,slice_3_prop]

df.to_csv('rAppTimeMetric.csv')
