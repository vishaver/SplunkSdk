import splunklib.client as client
import sys
from time import sleep
import splunklib.results as results
import pandas as pd
from collections import OrderedDict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
sns.set(rc={'figure.figsize':(11, 4)})


HOST = "splunkit.corp.xyz.com"
PORT = "9443"
USERNAME =  "************"
PASSWORD = "*********"
OWNER="user"
APP="YourAppInSplunk"

# Create a Service instance and log in
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD,
    owner=OWNER,
    app=APP)

query = {"cache":["search source=/apps/python3/hitachi/1m/cache_cliper1_stg  earliest=-2h latest=now| timechart span=2m latest(CACHE_MEMORY_USAGE_RATE) as CACHE_MEMORY_USAGE_RATE latest(CACHE_WRITE_PENDING_RATE) as CACHE_WRITE_PENDING_RATE by CLPR_NUMBER","CACHE_WRITE_PENDING_RATE","CACHE_MEMORY_USAGE_RATE","Scatter"],"cache1":["search source=/apps/python3/hitachi/1m/cache_cliper1_sfer  earliest=-2h latest=now| timechart span=2m latest(CACHE_MEMORY_USAGE_RATE) as CACHE_MEMORY_USAGE_RATE latest(CACHE_WRITE_PENDING_RATE) as CACHE_WRITE_PENDING_RATE by CLPR_NUMBER","CACHE_WRITE_PENDING_RATE","CACHE_MEMORY_USAGE_RATE","Scatter"]}
#searchquery_normal = "search source=/apps/python3/hitachi/1m/cache_cliper1_indhds08  earliest=-2h latest=now| timechart span=2m latest(CACHE_MEMORY_USAGE_RATE) as CACHE_MEMORY_USAGE_RATE latest(CACHE_WRITE_PENDING_RATE) as CACHE_WRITE_PENDING_RATE by CLPR_NUMBER"
kwargs_normalsearch = {"exec_mode": "normal"}

            
def runQurey(keys,*queryname):
    print("runQuery function called")
    job = service.jobs.create(queryname[0],**kwargs_normalsearch)
    while True:
        if job.is_done() == True:
            print("running job")
            break
    output=results.ResultsReader(job.results(count=0))
    job.cancel()
    print("calling dataframe function now")
    myDataframe(output,keys,*queryname)

def myDataframe(output,keys,*queryname):
    l = []
    for j in output:
        l.append(j)       
    df = pd.DataFrame(l)
    df._time = pd.to_datetime(df._time)
    jk1 = df.dropna().set_index('_time').astype(float).rename(columns={"CACHE_MEMORY_USAGE_RATE: 0":"CACHE_MEMORY_USAGE_RATE", "CACHE_WRITE_PENDING_RATE: 0":"CACHE_WRITE_PENDING_RATE"})
    myGraph(jk1,keys,*queryname)
    
def myGraph(jk1,keys,*queryname):
    print("In myGraph")
    fig = go.Figure()
    if queryname[3] == "Scatter":
        t=[queryname[1],queryname[2]]
        print(t)
        jk1[t].plot(marker='o', linestyle='-')
        plt.savefig(keys)
    elif queryname[3] == "Table":
        print("Table graph will print")    
def myQuery(**kwargs):
    for keys,values in kwargs.items():
        runQurey(keys,*values)
        sleep(10)
myQuery(**query)
