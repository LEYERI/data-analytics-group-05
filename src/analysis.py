"""Explanatory analysis of equally weighted municipality comparison tariffs."""
from pathlib import Path
import json, hashlib, argparse
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
KEY=['municipality_number_2026','operator_uri']
TYPE='C(municipality_type, Treatment(reference="Urban"))'
FORMULA='total_tariff ~ '+TYPE+' + C(canton_id)'

def manifest_differences(expected, actual):
    """Compare relative input hashes across Windows and POSIX snapshots."""
    def normalize(manifest):
        result = {}
        for key, value in manifest.items():
            key = key.replace(chr(92), '/')
            if key in result and result[key] != value:
                raise ValueError('Conflicting hashes for normalized path: ' + key)
            result[key] = value
        return result
    expected, actual = normalize(expected), normalize(actual)
    if expected.keys() != actual.keys():
        raise ValueError('Input manifest paths differ: ' + str(sorted(expected.keys() ^ actual.keys())))
    return sorted(key for key in expected if expected[key] != actual[key])

def operator_values(t):
    return t[KEY+['total_tariff']].drop_duplicates().groupby(KEY,as_index=False).total_tariff.mean()

def weighted_data(d):
    d=d.copy()
    if d.duplicated(KEY).any(): raise ValueError('Duplicate municipality/operator key')
    if d[KEY+['total_tariff']].isna().any().any() or not np.isfinite(d.total_tariff).all(): raise ValueError('Missing/nonfinite data')
    d['weight']=1/d.groupby('municipality_number_2026').operator_uri.transform('size')
    np.testing.assert_allclose(d.groupby('municipality_number_2026').weight.sum(),1)
    return d

def fit(d,formula=FORMULA):
    d=weighted_data(d)
    base=smf.wls(formula,data=d,weights=d.weight).fit()
    if int(base.nobs)!=len(d): raise ValueError('Silent model row loss')
    if np.linalg.matrix_rank(base.model.exog)!=base.model.exog.shape[1]: raise ValueError('Rank deficient design')
    # Independent weighted least-squares point-estimate verification.
    x=base.model.exog; y=base.model.endog; sw=np.sqrt(d.weight.to_numpy())
    beta=np.linalg.lstsq(x*sw[:,None],y*sw,rcond=None)[0]
    np.testing.assert_allclose(beta,base.params,rtol=1e-8,atol=1e-9)
    groups=np.column_stack([pd.factorize(d.operator_uri)[0],pd.factorize(d.municipality_number_2026)[0]])
    robust=base.get_robustcov_results(cov_type='cluster',groups=groups,use_correction=True,df_correction=True,use_t=True)
    coef=pd.DataFrame({'term':base.model.exog_names,'estimate':robust.params,'se':robust.bse,'p_value':robust.pvalues,'ci_low':robust.conf_int()[:,0],'ci_high':robust.conf_int()[:,1]})
    metrics={'r2_in_sample':float(base.rsquared),'rmse_in_sample':float(np.sqrt(np.average(base.resid**2,weights=d.weight))),'operator_values':len(d),'municipalities':int(d.municipality_number_2026.nunique()),'operators':int(d.operator_uri.nunique())}
    ix=[i for i,n in enumerate(base.model.exog_names) if n.startswith('C(municipality_type')]
    if ix:
        joint=robust.wald_test(np.eye(len(coef))[ix],use_f=True,scalar=True)
        metrics.update(joint_p=float(joint.pvalue),joint_F=float(joint.statistic),joint_df_num=float(joint.df_num),joint_df_denom=float(joint.df_denom))
        coef.loc[ix,'p_holm']=multipletests(coef.loc[ix,'p_value'],method='holm')[1]
    return base,coef,metrics

def main(root,output):
    root=Path(root); output=Path(output); output.mkdir(parents=True,exist_ok=True)
    proc=root/'data/processed'
    tariffs=pd.read_csv(proc/'cleaned_tariffs.csv')
    saved=pd.read_csv(proc/'operator_tariff_values.csv')
    op=operator_values(tariffs)
    pd.testing.assert_frame_equal(op,saved,check_exact=False,atol=1e-10,rtol=1e-10)
    meta=pd.read_csv(proc/'bfs_municipalities_2026.csv').rename(columns={'municipality_number':'municipality_number_2026'})
    d=op.merge(meta,on='municipality_number_2026',validate='many_to_one')
    assert len(d)==len(op)
    d=weighted_data(d)
    m=d.groupby('municipality_number_2026',as_index=False).agg(municipality_tariff=('total_tariff','mean'),n_operators=('operator_uri','size')).merge(meta,on='municipality_number_2026',validate='one_to_one')
    stored=pd.read_csv(proc/'municipality_values.csv').set_index('municipality_number_2026')
    np.testing.assert_allclose(m.municipality_tariff,stored.loc[m.municipality_number_2026].municipality_tariff)
    assert (len(tariffs),len(d),len(m),d.operator_uri.nunique())==(2255,2254,2108,551)
    summaries=m.groupby('municipality_type').municipality_tariff.describe()
    summaries.to_csv(output/'descriptive_summary.csv',encoding='utf8')
    metric=[]
    for name,formula in [('canton','total_tariff ~ C(canton_id)'),('type','total_tariff ~ '+TYPE),('type_canton',FORMULA)]:
        base,coef,me=fit(d,formula);me['model']=name;metric.append(me)
        coef.to_csv(output/('coefficients_'+name+'.csv'),index=False,encoding='utf8')
    pd.DataFrame(metric).to_csv(output/'model_metrics.csv',index=False)
    base,coef,mainmetrics=fit(d)
    diag=d[KEY+['total_tariff','weight']].copy();diag['fitted']=base.fittedvalues;diag['residual']=base.resid
    diag.to_csv(output/'diagnostics.csv',index=False)
    cases={'main':d}
    for label,mid,low,high in [('root',1065,25.153,25.414),('herznach_ueken',4186,24.047,27.892)]:
        for side,value in [('low',low),('high',high)]:
            alt=d.copy();alt.loc[alt.municipality_number_2026==mid,'total_tariff']=value
            cases[label+'_'+side]=alt
        cases['exclude_'+label]=d[d.municipality_number_2026!=mid].copy()
    for oid in ['356','5']:
        keep=(d.municipality_number_2026!=4186) | d.operator_uri.str.endswith('/'+oid)
        cases['herznach_only_operator_'+oid]=d[keep].copy()
    cases['exclude_both']=d[~d.municipality_number_2026.isin([1065,4186])].copy()
    for rootv in [25.153,25.414]:
        for herv in [24.047,27.892]:
            alt=d.copy();alt.loc[alt.municipality_number_2026==1065,'total_tariff']=rootv;alt.loc[alt.municipality_number_2026==4186,'total_tariff']=herv
            cases[f'both_{rootv}_{herv}']=alt
    cases['exclude_moutier']=d[d.municipality_number_2026!=6831].copy()
    for label,fun in [('minimum','min'),('maximum','max')]:
        alt=d.copy();v=tariffs.groupby('municipality_number_2026').total_tariff.agg(fun)
        alt['total_tariff']=alt.municipality_number_2026.map(v)
        cases['municipality_'+label]=alt
    cases['single_operator_only']=d[d.municipality_number_2026.isin(m.loc[m.n_operators==1,'municipality_number_2026'])].copy()
    extremes=diag.assign(absres=diag.residual.abs()).groupby('municipality_number_2026').absres.max().nlargest(10).index
    cases['exclude_10_extreme_residual_municipalities']=d[~d.municipality_number_2026.isin(extremes)].copy()
    for operator in d.operator_uri.value_counts().head(5).index:
        cases['exclude_operator_'+operator.split('/')[-1]]=d[d.operator_uri!=operator].copy()
    rows=[]
    for label,case in cases.items():
        _,c,me=fit(case)
        for row in c[c.term.str.startswith('C(municipality_type')].to_dict('records'):
            rows.append({'scenario':label,**row,**me})
    pd.DataFrame(rows).to_csv(output/'sensitivity.csv',index=False)
    figdir=output/'figures';figdir.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    order=['Urban','Intermediate','Rural']
    fig,ax=plt.subplots(figsize=(8,5));ax.boxplot([m.loc[m.municipality_type==t,'municipality_tariff'] for t in order],labels=order);ax.set_ylabel('Municipality comparison tariff (Rp./kWh, excluding VAT)');fig.tight_layout();fig.savefig(figdir/'01_types.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,6));m.groupby('canton').municipality_tariff.mean().sort_values().plot.barh(ax=ax);ax.set_xlabel('Equal-municipality mean tariff (Rp./kWh)');fig.tight_layout();fig.savefig(figdir/'02_cantons.png',dpi=180);plt.close(fig)
    c=coef[coef.term.str.startswith('C(municipality_type')]
    fig,ax=plt.subplots(figsize=(8,4));ax.errorbar(c.estimate,[1,0],xerr=np.vstack([c.estimate-c.ci_low,c.ci_high-c.estimate]),fmt='o',capsize=4);ax.set_yticks([1,0],['Intermediate vs Urban','Rural vs Urban']);ax.axvline(0,color='grey',linestyle='--');ax.set_xlabel('Adjusted difference, Rp./kWh; 95% marginal interval');fig.tight_layout();fig.savefig(figdir/'03_coefficients.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5));ax.scatter(diag.fitted,diag.residual,s=8,alpha=.4);ax.axhline(0,color='grey');ax.set(xlabel='Fitted tariff',ylabel='Residual (Rp./kWh)');fig.tight_layout();fig.savefig(figdir/'04_residuals.png',dpi=180);plt.close(fig)
    manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['data/raw','data/processed','notebooks'] for p in sorted((root/folder).glob('*')) if p.is_file()}
    report={'counts':{'raw':2268,'historical_ids_harmonized':17,'identical_combinations_consolidated':12,'missing_tariffs_excluded':1,'tariffs':len(tariffs),'operator_values':len(d),'municipalities':len(m),'operators':int(d.operator_uri.nunique()),'multi_operator_municipalities':int((m.n_operators>1).sum()),'uncovered_municipalities':2},'main_model':mainmetrics,'inputs_sha256':manifest,'scenario_count':len(cases),'interpretation':'Explanatory, equal-municipality comparison; in-sample fit, not causal or predictive validation.'}
    (output/'analysis_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report['main_model'],indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));parser.add_argument('--output',default=None);args=parser.parse_args();main(args.root,args.output or str(Path(args.root)/'results/analysis'))
