import itertools,json,unittest
from extract_commute import P,bounds,optional_membership,reconstructed_ems

class MembershipTests(unittest.TestCase):
    def test_year_specific_attendance(self):
        r=dict(ASISTEN='1',NIVACAD='04',ESCOLARI='01')
        self.assertTrue(reconstructed_ems(r))
        self.assertFalse(reconstructed_ems(dict(r,ASISTEN='5')))
        self.assertFalse(reconstructed_ems(dict(r,NIVACAD='99')))
        self.assertFalse(reconstructed_ems(dict(r,ESCOLARI='03')))
    def test_optional_students_not_forced(self):
        l,h=optional_membership({'1':1,'6':0,'9':0,'2':0,'3':0,'4':0,'5':0},{'5':100})
        self.assertLess(l,.01);self.assertEqual(h,1)
    def test_real_group_subsets(self):
        source=json.loads((P/'commute_summary.json').read_text())
        for r in source['scopes'].values():
            counts=r['weighted_time_bins'];pool=r['optional_stage_time_bins'];n=sum(counts.values());lo,hi=bounds(counts);keys=list(pool);lows=[];highs=[]
            for take in itertools.product([0,1],repeat=len(keys)):
                a,b,den=n*lo,n*hi,n
                for code,z in zip(keys,take):
                    if z:
                        one={str(k):int(str(k)==code) for k in [1,2,3,4,5,6,9]};u,v=bounds(one)
                        a+=pool[code]*u;b+=pool[code]*v;den+=pool[code]
                lows.append(a/den);highs.append(b/den)
            actual=optional_membership(counts,pool)
            self.assertAlmostEqual(actual[0],min(lows),places=12)
            self.assertAlmostEqual(actual[1],max(highs),places=12)
if __name__=='__main__':unittest.main()
