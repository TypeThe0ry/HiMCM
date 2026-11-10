#!/usr/bin/env python3
import csv, collections, json, pathlib
p=pathlib.Path(__file__).resolve().parent
def load(n):
 with (p/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
s=load('stops.txt'); a=load('areas.txt'); m=load('stop_areas.txt'); sid={r['stop_id'] for r in s}; aid={r['area_id'] for r in a}; bystop=collections.defaultdict(set); byarea=collections.defaultdict(set)
for r in m: bystop[r['stop_id']].add(r['area_id']); byarea[r['area_id']].add(r['stop_id'])
parents=collections.Counter(r['location_type'].strip() for r in s); sp=collections.Counter(r['stop_code'].strip()[:1] for r in s if r['stop_code'].strip());
helsinki={r['stop_id'] for r in s if r['stop_code'].strip().startswith('H')}; relevant={x for x in helsinki if x in bystop}; mixed=sum(bool(v&helsinki) and bool(v-helsinki) for v in byarea.values())
result={'feed_info':load('feed_info.txt'),'stops_rows':len(s),'location_type_counts':parents,'nonblank_parent_station':sum(bool(r['parent_station'].strip()) for r in s),'area_rows':len(a),'distinct_area_ids':len(aid),'stop_area_rows':len(m),'mapped_distinct_stops':len(bystop),'mapped_distinct_areas':len(byarea),'unknown_stop_ids':len(set(bystop)-sid),'unknown_area_ids':len(set(byarea)-aid),'stops_in_multiple_areas':sum(len(x)>1 for x in bystop.values()),'h_prefix_stop_codes':len(helsinki),'h_prefix_stops_with_area':len(relevant),'areas_containing_h_prefix_and_other_stops':mixed,'note':'H prefix is a scope diagnostic, not a municipality polygon or an area count; other codes include missing codes.'}
(p/'inventory_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
