import json,urllib.request,time
URL="https://api.swapcard.com/graphql"
VIEW="RXZlbnRWaWV3XzEyNjEzMjA="
Q="""query V($v:ID!,$c:Core_CursorPaginationInput){
 Core_eventPlanningListView(viewId:$v){ plannings(cursor:$c){
  pageInfo{ hasNextPage endCursor }
  nodes{ id title beginsAt(format:ISO8601) endsAt(format:ISO8601) place format type
   htmlDescription
   categories{ name }
   firstSpeakers(size:20){ firstName lastName organization jobTitle }
   exhibitorList{ name }
   fields{
     __typename
     ... on Core_TextField{ definition{ name } value{ text } }
     ... on Core_LongTextField{ definition{ name } value{ longText } }
     ... on Core_SelectField{ definition{ name } value{ text } }
     ... on Core_MultipleSelectField{ definition{ name } values{ text } }
     ... on Core_TreeField{ definition{ name } values{ value } }
   }
  }
 } }
}"""
def call(after):
    c={"first":40}
    if after: c["after"]=after
    body=json.dumps({"query":Q,"variables":{"v":VIEW,"c":c}}).encode()
    req=urllib.request.Request(URL,body,{"content-type":"application/json"})
    return json.load(urllib.request.urlopen(req))
allnodes=[]
after=None
while True:
    r=call(after)
    if "errors" in r:
        print(json.dumps(r["errors"],indent=1)); break
    pl=r["data"]["Core_eventPlanningListView"]["plannings"]
    allnodes.extend(pl["nodes"])
    print("got",len(allnodes))
    if not pl["pageInfo"]["hasNextPage"]: break
    after=pl["pageInfo"]["endCursor"]
    time.sleep(0.2)
json.dump(allnodes,open("all_plannings.json","w"),indent=1,ensure_ascii=False)
print("TOTAL",len(allnodes))
