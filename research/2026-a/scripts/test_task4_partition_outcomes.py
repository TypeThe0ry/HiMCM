import itertools,unittest
from task4_partition_outcomes import partition_union_lower

class PartitionBounds(unittest.TestCase):
    def test_all_three_person_three_school_label_assignments(self):
        checked=0
        for labels in itertools.product(range(3),repeat=9):
            # Each school gives a person at most one label; labels may differ across schools.
            rows=[labels[3*i:3*i+3] for i in range(3)]
            union=sum(any(r) for r in rows)
            all_lower=max(sum(row[s]>0 for row in rows) for s in range(3))
            group_lowers=[max(sum(row[s]==g for row in rows) for s in range(3)) for g in [1,2]]
            excess=sum(max(0,len(set(r)-{0})-1) for r in rows)
            self.assertLessEqual(partition_union_lower(all_lower,group_lowers,excess),union)
            checked+=1
        print('Exhaustive label-change membership checks:',checked)

    def test_stability_is_required_and_budget_restores_validity(self):
        # One student counted under label A at one school and B at another.
        self.assertEqual(partition_union_lower(1,[1,1],0),2)
        self.assertEqual(partition_union_lower(1,[1,1],1),1)
        self.assertEqual(partition_union_lower(655,[92,0,480,25,459,0,0]),1056)
        self.assertEqual(partition_union_lower(655,[92,0,480,25,459,0,0],401),655)
        for invalid in [-1,1.5,float('nan')]:
            with self.assertRaises(ValueError):partition_union_lower(1,[1],invalid)

if __name__=='__main__':unittest.main()
