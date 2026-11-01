"""Expose the frozen canonical density setup, without repeating its experiment."""
from pathlib import Path
import ast,copy,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_canonical_density_graph_v2.py'

def prepare():
 p=ROOT/SOURCE;assert hashlib.sha256(p.read_bytes()).hexdigest()==Path(str(p)+'.sha256').read_text().split()[0].lower()
 sp=importlib.util.spec_from_file_location('frozen_canonical_density_setup',p);mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
 tree=ast.parse(p.read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
 stop=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='records' for v in n.targets))
 fn.name='canonical_environment';fn.body=fn.body[:stop]+[ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-canonical-density-setup>','exec'),mod.__dict__)
 return mod.canonical_environment()

def point(zs):
 p=ROOT/SOURCE;assert hashlib.sha256(p.read_bytes()).hexdigest()==Path(str(p)+'.sha256').read_text().split()[0].lower()
 sp=importlib.util.spec_from_file_location('frozen_canonical_point_setup',p);mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
 tree=ast.parse(p.read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
 at=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='zs')
 loop=fn.body[at];stop=next(i for i,n in enumerate(loop.body) if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='probes' for v in n.targets))
 fn.name='point_environment';fn.args.args=[ast.arg(arg='zs')]
 fn.body=fn.body[:at]+loop.body[:stop]+[ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-canonical-point-operators>','exec'),mod.__dict__)
 return mod.point_environment(zs)
