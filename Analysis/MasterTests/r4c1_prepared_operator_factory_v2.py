"""Frozen mixed-engine setup with an explicit higher spatial Taylor order.

Order-two callers must supply their own certified highest shift jet: the
old order-one uncertainty constructor is deliberately not exposed there.
"""
from pathlib import Path
import ast,copy,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_mixed_operator_v4.py'
def prepare(order=1):
 assert order in (1,2)
 p=ROOT/SOURCE;want=Path(str(p)+'.sha256').read_text().split()[0].lower();assert hashlib.sha256(p.read_bytes()).hexdigest()==want
 spec=importlib.util.spec_from_file_location('prepared_frozen_higher_engine',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 tree=ast.parse(p.read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
 stop=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='whole' for t in n.targets));fn.name='prepared_environment';fn.body=fn.body[:stop]
 assignments=[n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(v,ast.Attribute) and isinstance(v.value,ast.Name) and v.value.id=='j' and v.attr=='ORDER' for v in n.targets)]
 assert len(assignments)==1 and isinstance(assignments[0].value,ast.Constant) and assignments[0].value.value==1
 assignments[0].value=ast.Constant(order)
 fn.body.append(ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[])))
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-mixed-higher-setup>','exec'),mod.__dict__)
 env=mod.prepared_environment()
 if order!=1:
  del env['state'];del env['second_at']
 return env
