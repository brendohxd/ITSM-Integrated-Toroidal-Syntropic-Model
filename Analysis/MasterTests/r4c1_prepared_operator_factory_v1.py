"""Reuse the frozen mixed-operator engine without replaying its full experiment.

Only the immutable calculation's setup prefix is exposed. No source edits,
provider dispatch, runtime configuration or scientific checks are bypassed.
The parent receipt remains the authority for its complete experiment.
"""
from pathlib import Path
import ast,copy,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_mixed_operator_v4.py'
def prepare():
 p=ROOT/SOURCE;want=Path(str(p)+'.sha256').read_text().split()[0].lower()
 assert hashlib.sha256(p.read_bytes()).hexdigest()==want
 spec=importlib.util.spec_from_file_location('prepared_frozen_mixed_engine',p)
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 tree=ast.parse(p.read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
 stop=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='whole' for t in n.targets))
 fn.name='prepared_environment';fn.body=fn.body[:stop]+[ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-mixed-setup-prefix>','exec'),mod.__dict__)
 return mod.prepared_environment()
