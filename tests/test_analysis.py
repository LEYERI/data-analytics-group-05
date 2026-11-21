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
class ManifestPathTests(unittest.TestCase):
 def test_windows_and_posix_manifest_keys_match(self):
  from src.analysis import manifest_differences
  self.assertEqual(manifest_differences({r'data\raw\input.csv':'abc'}, {'data/raw/input.csv':'abc'}), [])
  self.assertEqual(manifest_differences({'data/raw/input.csv':'abc'}, {r'data\raw\input.csv':'abc'}), [])
 def test_changed_hash_returns_posix_key(self):
  from src.analysis import manifest_differences
  self.assertEqual(manifest_differences({r'data\raw\input.csv':'abc'}, {'data/raw/input.csv':'def'}), ['data/raw/input.csv'])
 def test_missing_manifest_key_is_not_ignored(self):
  from src.analysis import manifest_differences
  with self.assertRaises(ValueError): manifest_differences({'data/raw/a.csv':'abc'}, {})
 def test_conflicting_normalized_keys_rejected(self):
  from src.analysis import manifest_differences
  with self.assertRaises(ValueError): manifest_differences({r'data\raw\a.csv':'abc','data/raw/a.csv':'def'}, {'data/raw/a.csv':'abc'})
class LineEndingHashTests(unittest.TestCase):
 def test_lf_crlf_text_equal(self):
  from src.analysis import content_sha256
  self.assertEqual(content_sha256('input.csv',b'a,b\n1,2\n'),content_sha256('input.csv',b'a,b\r\n1,2\r\n'))
 def test_real_text_change_detected(self):
  from src.analysis import content_sha256
  self.assertNotEqual(content_sha256('input.json',b'{"x":1}\n'),content_sha256('input.json',b'{"x":2}\r\n'))
 def test_binary_hashes_remain_exact(self):
  import hashlib
  from src.analysis import content_sha256
  for ext in ['.sqlite','.db','.pdf','.pptx','.png','.jpg','.bin']:
   with self.subTest(ext=ext):
    b=b'binary\r\ncontent\x00'
    self.assertEqual(content_sha256('file'+ext,b),hashlib.sha256(b).hexdigest())
    self.assertNotEqual(content_sha256('file'+ext,b),content_sha256('file'+ext,b.replace(b'\r\n',b'\n')))
 def test_other_whitespace_not_normalized(self):
  from src.analysis import content_sha256
  self.assertNotEqual(content_sha256('input.csv',b'a, b\n'),content_sha256('input.csv',b'a,b\n'))
  self.assertNotEqual(content_sha256('input.csv',b'a,b'),content_sha256('input.csv',b'a,b\n'))
 def test_standalone_carriage_return_not_normalized(self):
  from src.analysis import content_sha256
  self.assertNotEqual(content_sha256('input.csv',b'a\rb'),content_sha256('input.csv',b'a\nb'))
if __name__=='__main__': unittest.main()
