import json,re,html,collections
nodes=json.load(open("all_plannings.json"))
spk=json.load(open("speakers.json"))
def strip(h):
    if not h: return ""
    t=re.sub(r"<br\s*/?>","\n",h)
    t=re.sub(r"</p>","\n\n",t)
    t=re.sub(r"<[^>]+>","",t)
    t=html.unescape(t)
    return re.sub(r"\n{3,}","\n\n",t).strip()
out=[]
for n in nodes:
    b=n["beginsAt"]; e=n["endsAt"]
    sp=[]
    for s in spk.get(n["id"],[]):
        nm=" ".join(x for x in [s.get("firstName"),s.get("lastName")] if x).strip()
        sp.append({"name":nm,"jobTitle":s.get("jobTitle") or "","organization":s.get("organization") or "","role":(s.get("type") or {}).get("value") or ""})
    out.append({
        "id":n["id"],
        "title":n["title"],
        "description":strip(n["htmlDescription"]),
        "date":b[:10],
        "startTime":b[11:16],
        "endTime":e[11:16],
        "beginsAt":b,"endsAt":e,
        "location":n["place"],
        "type":n["type"],
        "format":n["format"],
        "speakers":sp,
        "registeredAttendees":((n.get("withEvent") or {}).get("attendeeProfiles") or {}).get("totalCount",0),
    })
out.sort(key=lambda x:(x["beginsAt"],x["location"] or "",x["title"]))
json.dump(out,open("dmexco-2026-conference-agenda.json","w"),indent=2,ensure_ascii=False)
print("wrote",len(out))
print("by date:",collections.Counter(x["date"] for x in out))
print("by location:",collections.Counter(x["location"] for x in out))
