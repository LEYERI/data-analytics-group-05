import unittest
import pandas as pd
import numpy as np
from src.analysis import operator_values, weighted_data, fit
class AnalysisTests(unittest.TestCase):
 def test_distinct_values_not_historical_row_counts(self):
  d=pd.DataFrame({'municipality_number_2026':[1,1,1,1,2], 'operator_uri':['a','a','a','b','c'], 'total_tariff':[10.,10.,20.,30.,40.]})
  o=operator_values(d)
  self.assertEqual(o.total_tariff.tolist(),[15.,30.,40.])
  w=weighted_data(o)
  np.testing.assert_allclose(w.groupby('municipality_number_2026').weight.sum(),1.)
  self.assertEqual(np.average(w[w.municipality_number_2026==1].total_tariff,weights=w[w.municipality_number_2026==1].weight),22.5)
 def test_reweight_after_removal(self):
  d=pd.DataFrame({'municipality_number_2026':[1,2], 'operator_uri':['a','c'], 'total_tariff':[10.,40.]})
  np.testing.assert_allclose(weighted_data(d).weight,1.)
 def test_duplicate_operator_keys_rejected(self):
  d=pd.DataFrame({'municipality_number_2026':[1,1], 'operator_uri':['a','a'], 'total_tariff':[10.,20.]})
  with self.assertRaises(ValueError): weighted_data(d)
 def test_missing_tariff_rejected(self):
  d=pd.DataFrame({'municipality_number_2026':[1], 'operator_uri':['a'], 'total_tariff':[np.nan]})
  with self.assertRaises(ValueError): weighted_data(d)
 def test_real_fit_equals_equal_municipality_ols(self):
  from pathlib import Path
  import statsmodels.formula.api as smf
  from src.analysis import FORMULA
  root=Path(__file__).resolve().parents[1]
  op=pd.read_csv(root/'data/processed/operator_tariff_values.csv')
  meta=pd.read_csv(root/'data/processed/bfs_municipalities_2026.csv').rename(columns={'municipality_number':'municipality_number_2026'})
  d=op.merge(meta,on='municipality_number_2026',validate='many_to_one')
  b,c,metrics=fit(d)
  m=d.groupby('municipality_number_2026',as_index=False).total_tariff.mean().merge(meta,on='municipality_number_2026')
  independent=smf.ols(FORMULA,data=m).fit()
  np.testing.assert_allclose(b.params,independent.params,rtol=1e-8,atol=1e-9)
  self.assertEqual(metrics['municipalities'],2108)
  self.assertEqual(metrics['operator_values'],2254)
  # Independently construct the two-way cluster sandwich from weighted scores.
  x=b.model.exog;w=weighted_data(d).weight.to_numpy();r=b.resid.to_numpy()
  score=x*(w*r)[:,None];bread=np.linalg.inv(x.T@(w[:,None]*x));n,k=x.shape
  def component(groups):
   sums=pd.DataFrame(score).groupby(np.asarray(groups)).sum().to_numpy();g=len(sums)
   return bread@(sums.T@sums)@bread*(g/(g-1))*((n-1)/(n-k))
  covariance=component(d.operator_uri)+component(d.municipality_number_2026)-component(np.arange(n))
  np.testing.assert_allclose(c.se**2,np.diag(covariance),rtol=1e-7,atol=1e-10)
 def test_two_operator_removal_changes_weights(self):
  d=pd.DataFrame({'municipality_number_2026':[1,1,2], 'operator_uri':['a','b','c'], 'total_tariff':[10.,30.,40.]})
  np.testing.assert_allclose(weighted_data(d).weight,[.5,.5,1.])
  np.testing.assert_allclose(weighted_data(d[d.operator_uri!='b']).weight,[1.,1.])
if __name__=='__main__': unittest.main()
