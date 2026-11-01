"""Expose immutable local density operators without rerunning global bounds.

The parent experiment remains the authority for its complete checks.
This helper neither edits it nor replaces its recorded results.
"""
from pathlib import Path
import ast,copy,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_clock_density_v3.py'
def prepare():
 p=ROOT/SOURCE;assert hashlib.sha256(p.read_bytes()).hexdigest()==Path(str(p)+'.sha256').read_text().split()[0].lower()
 spec=importlib.util.spec_from_file_location('frozen_local_clock_density',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 tree=ast.parse(p.read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
 body=fn.body
 stop=next(i for i,n in enumerate(body) if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='whole' for v in n.targets))
 clock=next(i for i,n in enumerate(body) if i>stop and isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='tree' for v in n.targets))
 tensor=next(i for i,n in enumerate(body) if isinstance(n,ast.FunctionDef) and n.name=='tensor')
 defs=[copy.deepcopy(n) for n in body if isinstance(n,ast.FunctionDef) and n.name in ('tensor','lie','generators','balance')]
 assert len(defs)==4
 fn.name='local_environment';fn.body=body[:stop]+body[clock:tensor]+defs+[ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-clock-density-local-operators>','exec'),mod.__dict__)
 return mod.local_environment()
