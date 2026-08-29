import json,urllib.request,time
URL="https://api.swapcard.com/graphql"
EID="RXZlbnRfNDM1MDQyOA=="
nodes=json.load(open("all_plannings.json"))
ids=[n["id"] for n in nodes]
def chunk(l,s):
    for i in range(0,len(l),s): yield l[i:i+s]
res={}
BATCH=20
for bi,group in enumerate(chunk(ids,BATCH)):
    parts=[]
    for j,pid in enumerate(group):
        parts.append(f'a{j}: Core_listSpeakersByPlanning(planningId:"{pid}", eventId:"{EID}", cursor:{{first:100}}){{ nodes{{ firstName lastName jobTitle organization type{{ value }} }} }}')
    q="query{ "+" ".join(parts)+" }"
    body=json.dumps({"query":q}).encode()
    req=urllib.request.Request(URL,body,{"content-type":"application/json"})
    r=json.load(urllib.request.urlopen(req))
    if "errors" in r: print("ERR",json.dumps(r["errors"])[:300])
    d=r.get("data",{}) or {}
    for j,pid in enumerate(group):
        v=d.get(f"a{j}")
        res[pid]=v["nodes"] if v else []
    print("batch",bi,"done",len(res))
    time.sleep(0.2)
json.dump(res,open("speakers.json","w"),indent=1,ensure_ascii=False)
print("total planningswith speakers:",sum(1 for v in res.values() if v))
