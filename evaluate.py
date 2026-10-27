import json,time,statistics,re
from archive import Archive,ROOT,REVISION
CASES=[
('What rang after the bell rope was cut?','bell'),
('Why was the amber lantern kept burning?','light'),
('What did Mara write to her brother?','letter'),
('When did the final passenger service leave?','train'),
('Why were there no wheel marks in the snow?','tracks'),
('Could the heating system make knocking sounds?','pipe'),
('Was the light powered by electricity?','battery'),
('What did the siblings repair in the old photo?','portrait'),
('What food did the kiosk buy?','bread'),
('What grew outside the waiting room?','garden'),
('Why did the timepiece stop?','clock'),
('Who found a fresh letter many years later?','visitor'),
('How much is bitcoin today?',None),
('Write a Kubernetes deployment manifest',None),
('Can you prescribe antibiotics?',None),
]
a=Archive();rows=[]
for q,expected in CASES:
 t=time.perf_counter();r=a.search(q);ms=(time.perf_counter()-t)*1000
 ids=[h['id'] for h in r['hits']]
 rows.append(dict(query=q,expected=expected,actual=ids,correct=(not ids if expected is None else expected in ids),top1=(ids[0] if ids else None),ms=round(ms,2)))
tokens=lambda s:set(re.findall(r'[a-z]+',s.lower()))
baseline=[]
for q,e in CASES[:12]:
 qt=tokens(q);ranked=sorted(a.records,key=lambda r:-len(qt & tokens(r['title']+' '+r['text']))/max(1,len(qt | tokens(r['title']+' '+r['text']))))
 baseline.append(ranked[0]['id']==e)
r=dict(model_revision=REVISION,fixture='15 author-written diagnostic queries, not independent or human-user evaluation',cases=rows,correct=sum(x['correct'] for x in rows),total=len(rows),in_scope_top1=sum(x['top1']==x['expected'] for x in rows[:12]),in_scope_total=12,jaccard_in_scope_top1=sum(baseline),warm_median_ms=round(statistics.median(x['ms'] for x in rows[1:]),2),source_count=len(a.records),notes='Timings exclude model loading. Threshold is uncalibrated. No visitor chills or memory outcomes measured.')
(ROOT/'docs/evaluation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
