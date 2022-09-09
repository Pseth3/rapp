import pandas as pd
import os

df = pd.DataFrame(data = {"slice_1":[425,910,500,10],
                    "slice_2":[900,220,600,80],
                    "slice_3":[332,880,100,300],
                    })

df.to_csv(os.path.join(os.getcwd(),"throughput.csv"),index=False)
df1 = pd.read_csv(os.path.join(os.getcwd(),"throughput.csv"),header=0)
print(df1)