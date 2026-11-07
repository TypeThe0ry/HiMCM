import unittest
import pandas as pd
from extract_chains import reconstruct


def trip(dep,arr,purpose,origin=0,destination=0,place=1,tour=1):
    dh,dm=dep;ah,am=arr
    return dict(TRP_DEP_HR=dh,TRP_DEP_MIN=dm,TRP_ARR_HR=ah,TRP_ARR_MIN=am,TRPDUR=(ah*60+am-dh*60-dm)%1440,DTPURP=purpose,ORIG_HOME=origin,DEST_HOME=destination,PLANO=place,TOUR_ID=tour)

class Chains(unittest.TestCase):
    def test_midnight_and_skipped_place_numbers(self):
        frame=pd.DataFrame([trip((23,50),(0,0),5,origin=1),trip((0,10),(0,30),12,place=4)])
        r=reconstruct(frame);self.assertEqual(r['status'],'reconstructed');self.assertTrue(r['transport_stops_only'])
        self.assertEqual((r['elapsed_minutes'],r['moving_minutes'],r['stop_minutes']),(40,30,10))

    def test_last_actual_home_departure(self):
        frame=pd.DataFrame([trip((6,0),(6,10),5,origin=1),trip((6,20),(6,30),3,destination=1,place=2),trip((7,0),(7,10),6,origin=1,place=3),trip((7,15),(7,30),12,place=4)])
        self.assertEqual(reconstruct(frame)['elapsed_minutes'],30)
        frame.loc[2,'ORIG_HOME']=0
        self.assertEqual(reconstruct(frame)['status'],'unresolved_home_return')

    def test_long_work_episode_is_not_commute_admitted(self):
        r=reconstruct(pd.DataFrame([trip((7,0),(8,0),9,origin=1),trip((16,0),(17,0),12,place=2)]))
        self.assertEqual(r['elapsed_minutes'],600);self.assertEqual(r['moving_minutes'],120);self.assertFalse(r['transport_stops_only'])

    def test_overlap_bad_duration_and_missing_home(self):
        frame=pd.DataFrame([trip((7,0),(7,10),5,origin=1),trip((7,5),(7,30),12,place=2)])
        self.assertEqual(reconstruct(frame)['status'],'overlapping_segments')
        frame.loc[1,'TRP_DEP_MIN']=15;frame.loc[1,'TRPDUR']=15
        frame.loc[0,'TRPDUR']=12;self.assertEqual(reconstruct(frame)['status'],'invalid_segment_duration')
        frame.loc[0,'TRPDUR']=10;frame.loc[0,'ORIG_HOME']=0;frame.loc[0,'DTPURP']=3
        self.assertEqual(reconstruct(frame)['status'],'no_observed_home_departure')

if __name__=='__main__':unittest.main()
