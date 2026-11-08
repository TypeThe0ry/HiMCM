"""Synthetic mathematical tests; no test judgment is empirical evidence."""
import unittest
from itertools import product
import numpy as np
from task4_ahp_mc_baseline import ahp_weights, score_many, rank_metrics, interval_metrics
from task4_interval_decision import interval_decision
from task4_v5_model import score


class ModelTests(unittest.TestCase):
    def document(self, matrix):
        return dict(source='Synthetic mathematical test', respondents='None: test fixture',
            elicitation_date='Not elicited', judgment_method='Synthetic unit test',
            indicators=['a','b','c'], matrix=matrix)

    def test_ahp_known_eigenvector(self):
        w = np.array([.5,.3,.2])
        got, report = ahp_weights(self.document((w[:,None]/w).tolist()), ['a','b','c'])
        np.testing.assert_allclose(got,w,atol=1e-12)
        self.assertLess(report['CR'],1e-12)

    def test_ahp_rejects_missing_provenance_reciprocity_and_inconsistency(self):
        doc = self.document(np.ones((3,3)).tolist())
        doc['source']=''
        with self.assertRaises(ValueError): ahp_weights(doc,['a','b','c'])
        doc=self.document([[1,2,1],[1,1,1],[1,1,1]])
        with self.assertRaises(ValueError): ahp_weights(doc,['a','b','c'])
        doc=self.document([[1,9,1/9],[1/9,1,9],[9,1/9,1]])
        with self.assertRaises(ValueError): ahp_weights(doc,['a','b','c'])

    def test_scores_preserve_existing_metric_and_monotonicity(self):
        rng=np.random.default_rng(12)
        lo=rng.random((5,3));hi=lo+(1-lo)*rng.random((5,3))
        w=rng.dirichlet([1,2,3],size=8)
        got=score_many(lo,w)
        for i in range(8): np.testing.assert_allclose(got[i],score(lo,w[i]),atol=1e-12)
        self.assertTrue(np.all(got<=score_many(hi,w)))
        np.testing.assert_allclose(score_many(np.array([[0,0,0],[1,1,1]]),w), np.tile([0,100],(8,1)))

    def test_ties_split_at_first_and_third(self):
        ranks,first,third=rank_metrics([[4,4,2,2]])
        np.testing.assert_allclose(ranks,[[1.5,1.5,3.5,3.5]])
        np.testing.assert_allclose(first,[[.5,.5,0,0]])
        np.testing.assert_allclose(third,[[1,1,.5,.5]])
        ranks,first,third=rank_metrics([[2,2,4,4]],descending=False)
        np.testing.assert_allclose(first,[[.5,.5,0,0]])
        np.testing.assert_allclose(third,[[1,1,.5,.5]])

    def test_interval_metrics_against_existing_and_corner_enumeration(self):
        lo=np.array([[.2,.4,.4],[.5,.5,.5]])
        hi=np.array([[.3,.7,.8],[.5,.5,.5]])
        regret,possible,necessary,best,worst=interval_metrics(lo,hi)
        for r in range(2):
            dec=interval_decision(lo[r],hi[r])
            for value,key in [(regret,'max_regret'),(possible,'possible_champion'),
                (necessary,'necessary_champion'),(best,'best_rank'),(worst,'worst_rank')]:
                np.testing.assert_allclose(value[r],dec[key])
            corner_ranks=[]
            for bits in product([0,1],repeat=3):
                x=np.where(bits,hi[r],lo[r])
                corner_ranks.append([1+np.sum(x>v+1e-12) for v in x])
            np.testing.assert_array_equal(best[r],np.min(corner_ranks,axis=0))
            np.testing.assert_array_equal(worst[r],np.max(corner_ranks,axis=0))

if __name__=='__main__': unittest.main()
