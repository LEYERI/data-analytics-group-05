"""Reproduce all notebooks in a temporary copy, leaving source data untouched."""
from pathlib import Path
import sys, tempfile, shutil, json, hashlib, sqlite3, subprocess
from contextlib import closing
import pandas as pd, numpy as np, nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from src.analysis import manifest_differences
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original={p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts}
report={'notebooks':[],'environment':sys.version,'csv_checks':0}
with tempfile.TemporaryDirectory(prefix='group05_reproduction_') as tmp:
    work=Path(tmp)/'project';shutil.copytree(root,work,ignore=shutil.ignore_patterns('.git','__pycache__'))
    # Remove only derived artifacts inside the verified temporary workspace.
    for relative in ['data/processed','results','data/electricity_tariffs.sqlite']:
        target=(work/relative).resolve()
        assert target.is_relative_to(work.resolve())
        if target.is_dir(): shutil.rmtree(target)
        elif target.exists(): target.unlink()
    ks=Path(tmp)/'kernels/verify';ks.mkdir(parents=True)
    (ks/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Verified environment','language':'python'}))
    for path in sorted((work/'notebooks').glob('*.ipynb')):
        nb=nbformat.read(path,as_version=4)
        nb.cells.insert(0,nbformat.v4.new_code_cell("import requests\ndef blocked(*a,**k): raise RuntimeError('Network disabled during reproduction')\nrequests.sessions.Session.request=blocked"))
        km=KernelManager(kernel_name='verify',kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(ks.parent)]))
        try: NotebookClient(nb,km=km,timeout=180,resources={'metadata':{'path':str(work/'notebooks')}}).execute()
        finally:
            if km.has_kernel: km.shutdown_kernel(now=True)
        report['notebooks'].append({'name':path.name,'code_cells':sum(c.cell_type=='code' for c in nb.cells)-1,'status':'PASS'})
        print('PASS',path.name,flush=True)
    for folder in ['data/processed','results/sql','results/analysis']:
        expected={f.name for f in (root/folder).glob('*.csv') if not f.name.startswith('reference_comparison')}
        actual={f.name for f in (work/folder).glob('*.csv')}
        assert expected==actual, (folder,expected,actual)
        for f in sorted((root/folder).glob('*.csv')):
            if f.name.startswith('reference_comparison'): continue
            pd.testing.assert_frame_equal(pd.read_csv(f),pd.read_csv(work/folder/f.name),check_exact=False,rtol=1e-9,atol=1e-9)
            report['csv_checks']+=1
    with closing(sqlite3.connect(root/'data/electricity_tariffs.sqlite')) as a,closing(sqlite3.connect(work/'data/electricity_tariffs.sqlite')) as b:
        assert b.execute('pragma integrity_check').fetchone()[0]=='ok'
        for (t,) in a.execute("select name from sqlite_master where type='table'"):
            pd.testing.assert_frame_equal(pd.read_sql_query('select * from '+t,a),pd.read_sql_query('select * from '+t,b))
        report['sql_checks']={f.name:len(pd.read_sql_query(f.read_text(encoding='utf8'),b)) for f in sorted((root/'sql').glob('*.sql'))}
    # Compare computed summary, excluding notebook file hashes (new notebook is executed in memory).
    a=json.loads((root/'results/analysis/analysis_report.json').read_text());b=json.loads((work/'results/analysis/analysis_report.json').read_text())
    report['regenerated_byte_differences']=manifest_differences(a['inputs_sha256'], b['inputs_sha256'])
    assert not any(key.startswith(('data/raw/','notebooks/')) for key in report['regenerated_byte_differences'])
    assert a['counts']==b['counts'] and a['scenario_count']==b['scenario_count']
    for key,value in a['main_model'].items(): np.testing.assert_allclose(value,b['main_model'][key],rtol=1e-9,atol=1e-9)
    report['analysis_report_reproduced']=True
    report['derived_outputs_removed_before_execution']=True
    expected_figures={f.name for f in (root/'results/analysis/figures').glob('*.png')}
    assert expected_figures=={f.name for f in (work/'results/analysis/figures').glob('*.png')}
    report['figures_reproduced']=len(expected_figures)
assert all(sha(root/f)==h for f,h in original.items())
report['source_files_unchanged']=True
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root,check=True)
report['unit_tests']='PASS'
(root/'results/analysis/reproduction.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
