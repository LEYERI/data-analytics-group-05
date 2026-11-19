"""Read-only comparison to a separately archived reference project."""
from pathlib import Path
import sys,argparse,json,hashlib
import pandas as pd,numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from src.analysis import fit
parser=argparse.ArgumentParser();parser.add_argument('--reference',required=True);args=parser.parse_args();old=Path(args.reference)
d=pd.read_csv(old/'data/processed/tariffs_joined.csv').rename(columns={'bfs_id':'municipality_number_2026','operator':'operator_uri','total':'total_tariff'})
d['municipality_type']=d.type_code.map({1:'Urban',2:'Intermediate',3:'Rural'})
b,c,me=fit(d)
oldmetrics=pd.read_csv(old/'results/model_metrics.csv').iloc[2]
oldcoef=pd.read_csv(old/'results/coefficients_typ.csv')
oldjoint=json.loads((old/'results/joint_test.json').read_text(encoding='utf8'))
selected=c[c.term.str.startswith('C(municipality_type')]
np.testing.assert_allclose(selected.estimate,oldcoef.estimate_rp_kwh,rtol=1e-8,atol=1e-9)
np.testing.assert_allclose(selected[['se','p_value','ci_low','ci_high']],oldcoef[['se','p_value','ci_low','ci_high']],rtol=1e-8,atol=1e-9)
np.testing.assert_allclose([me['joint_p'],me['r2_in_sample'],me['rmse_in_sample']],[oldjoint['p_value'],oldmetrics.weighted_r2_in_sample,oldmetrics.weighted_rmse_rp_kwh_in_sample],rtol=1e-8,atol=1e-9)
new=pd.read_csv(root/'results/analysis/coefficients_type_canton.csv');new=new[new.term.str.startswith('C(municipality_type')]
newmet=json.loads((root/'results/analysis/analysis_report.json').read_text())['main_model']
rows=[]
for label,ov,nv in [('municipalities',2105,2108),('operator_values',2250,2254),('operators',549,551),('joint_p',me['joint_p'],newmet['joint_p']),('r2_in_sample',me['r2_in_sample'],newmet['r2_in_sample']),('rmse_in_sample',me['rmse_in_sample'],newmet['rmse_in_sample'])]: rows.append({'measure':label,'old':ov,'new':nv,'difference':nv-ov})
for label,(_,o),(_,n) in zip(['Intermediate','Rural'],selected.iterrows(),new.iterrows()):
 for field in ['estimate','ci_low','ci_high','p_value']:
  rows.append({'measure':label+'_'+field,'old':o[field],'new':n[field],'difference':n[field]-o[field]})
pd.DataFrame(rows).to_csv(root/'results/analysis/reference_comparison.csv',index=False)
report={'old_results_independently_reproduced':True,'old_reference_files_sha256':{f:hashlib.sha256((old/f).read_bytes()).hexdigest() for f in ['data/processed/tariffs_joined.csv','results/model_metrics.csv','results/coefficients_typ.csv','results/joint_test.json']},'note':'Reference comparison is separate from the self-contained current pipeline; requires the archived reference project.'}
(root/'results/analysis/reference_comparison.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(pd.DataFrame(rows).to_string(index=False))
