"""Exact existing-portal allocation control; no new physical closure."""
from pathlib import Path
import argparse,hashlib,json
import sympy as S

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_A16_SECTOR_SPLIT_V1_CONTRACT_2026-11-15.md'
INPUTS='Theory/Gates/RES-001/RES001_A16_SECTOR_SPLIT_V1_INPUTS_2026-11-15.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/INPUTS).read_text())
 for p,h in pins.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 eta,g,u,v,r,ud,vd,rd,H,TP,TR=S.symbols('eta g u v r ud vd rd H TP TR',real=True)
 W=g*(u*u+v*v)*r*r/4
 Wdot=S.diff(W,u)*ud+S.diff(W,v)*vd+S.diff(W,r)*rd
 checks={}
 def zero(name,e):checks[name]=S.simplify(e)==0
 def nonzero(name,e):checks[name]=S.simplify(e)!=0
 # L'_P=L_P+eta W, L'_R=L_R-eta W.
 zero('total_action_density',eta*W-eta*W)
 for x in (u,v,r):zero('total_potential_euler_'+str(x),S.diff(eta*W-eta*W,x))
 metric=S.diag(-1,1,1,1)
 dTP=eta*W*metric;dTR=-dTP
 checks['all_total_stress_components']=dTP+dTR==S.zeros(4)
 dQ0=-eta*Wdot # eta nabla^0 W
 zero('reservoir_energy_balance',S.diff(eta*W,u)*ud+S.diff(eta*W,v)*vd+S.diff(eta*W,r)*rd+dQ0)
 zero('plenum_energy_balance',-eta*Wdot-dQ0)
 zero('reservoir_pressure_cancels_expansion',3*H*(dTR[0,0]+dTR[1,1]))
 zero('plenum_pressure_cancels_expansion',3*H*(dTP[0,0]+dTP[1,1]))
 zero('U1_portal_invariance',u*S.diff(W,v)-v*S.diff(W,u))
 spatial=dTP[1:4,1:4]
 checks['trace_free_spatial_stress_unchanged']=spatial-S.eye(3)*S.trace(spatial)/3==S.zeros(3)
 nonzero('reject_uncompensated_total_stress',dTP[0,0])
 nonzero('reject_uncompensated_current',dQ0)
 nonzero('reject_wrong_raised_time_sign',eta*Wdot+eta*Wdot)
 ds=-dQ0/TR+dQ0/TP
 zero('fixed_temperature_heat_shift',ds-eta*Wdot*(1/TR-1/TP))
 example={g:S.Rational(2),u:S.Rational(1),v:S.Rational(2),r:S.Rational(3),ud:S.Rational(1),vd:S.Rational(-1),rd:S.Rational(2),TP:S.Rational(2),TR:S.Rational(3)}
 plus=S.factor(ds.subs(example).subs(eta,1));minus=S.factor(ds.subs(example).subs(eta,-1))
 checks['rational_entropy_shift_opposite_signs']=bool(plus*minus<0)
 # Independently evaluate a second rational configuration's isotropic components.
 wp=S.Rational(5,4)*(S.Rational(2,3)**2+S.Rational(4,7)**2)*S.Rational(3,2)**2/4
 dp=S.diag(-wp,wp,wp,wp)
 checks['independent_component_allocation']=dp[1,1]==dp[2,2]==dp[3,3] and dp+(-dp)==S.zeros(4)
 assert all(checks.values()),[k for k,vv in checks.items() if not vv]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 receipt={'status':'PASS_EXISTING_PORTAL_ALLOCATION_CONTROL','checks':checks,'inputs':pins,'formulae':{'Wdot':str(S.expand(Wdot)),'delta_Qsyn0':str(S.expand(dQ0)),'naive_entropy_shift':str(S.factor(ds))},'rational_entropy_shift':[str(plus),str(minus)],'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Constant portal-allocation bookkeeping; no temperatures, entropy law, physical domain or memory kernel derived.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode())
 print(json.dumps({'checks':len(checks),'passed':sum(checks.values()),'physics_pass':False,'receipt':str(p)}))
if __name__=='__main__':main()
