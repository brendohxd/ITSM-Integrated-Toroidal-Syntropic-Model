"""Validated separable two-time kernels and full-history reconstruction in B1."""
from pathlib import Path
from fractions import Fraction as Q
from concurrent.futures import ProcessPoolExecutor
import argparse,gzip,hashlib,json,sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_certified_numerical_v1 as c
import test_a16_pressure_evolution_v3 as ref
k=c.k;T=Q(1,20);DEG=c.DEGREE
BASE='Analysis/MasterTests/outputs/'
PINS='Theory/Gates/RES-001/RES001_A16_NUMERICAL_KERNEL_V1_INPUTS_2026-11-19.json'
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def encode(o):return (json.dumps(o,sort_keys=True,indent=2)+'\n').encode()
def save(p,o):
 p.write_bytes(encode(o));Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')
def progress(out,mode,message):
 line=f'ell={mode}: {message}'
 print(line,flush=True)
 p=ROOT/'.local/itsm-context'/(out.name+'-progress.log')
 with p.open('a',encoding='utf-8') as f:f.write(line+'\n')
def scaled(q):return k.IV.fraction(Q(q)).hi
def times(a,b):return k.upprod(a,b)
def hscale(a,h):return k.IV(a).scale(h.numerator,h.denominator).hi
def zero_tm():return (k.TM.constant(k.ZERO,DEG),k.TM.constant(k.ZERO,DEG))
def zeros(n,m):return [[zero_tm() for _ in range(m)] for _ in range(n)]
def tmzero(z):return z[0].sup()==0 and z[1].sup()==0
def transpose(mat):return [list(row) for row in zip(*mat)]
def tmnorm(mat):return max((sum(z[0].sup()+z[1].sup() for z in row) for row in mat),default=0)
def multiply(a,b):
 out=zeros(len(a),len(b[0]))
 for i,row in enumerate(a):
  for q,x in enumerate(row):
   if tmzero(x):continue
   for j,y in enumerate(b[q]):
    if not tmzero(y):out[i][j]=c.complex_add(out[i][j],c.complex_mul(x,y))
 return out
def plus(a,b):return [[c.complex_add(x,y) for x,y in zip(row,other)] for row,other in zip(a,b)]
def minus(a,b):return plus(a,[[(-z[0],-z[1]) for z in row] for row in b])
def center(mat):
 out=zeros(len(mat),len(mat[0]));errors=[]
 for i,row in enumerate(mat):
  err=0
  for j,pair in enumerate(row):
   vals=[]
   for model in pair:
    cc=[x.center() for x in model.coeff]
    err+=model.radius+sum((x-y).abs_upper() for x,y in zip(model.coeff,cc));vals.append(k.TM(cc))
   out[i][j]=tuple(vals)
  errors.append(err)
 return out,max(errors,default=0)
def entries_matrix(entries,n,m):
 out=zeros(n,m)
 for i,j,re,im in entries:out[i][j]=(re,im)
 return out
def pack(mat):return [[[[str(q.lo) for q in model.coeff] for model in pair] for pair in row] for row in mat]
def numeric(mat,x=Q(1)):
 return np.array([[complex(float(Q(z[0].at(x.numerator,x.denominator).center().lo,k.SCALE)),float(Q(z[1].at(x.numerator,x.denominator).center().lo,k.SCALE))) for z in row] for row in mat])
def integrate(model,prefix,h):
 """Indefinite integral on a tile; retains degree-25 and all model tails."""
 out=zeros(len(model),1)
 for i,row in enumerate(model):
  pair=[]
  for j,poly in enumerate(row[0]):
   coeff=[prefix[i][j]]+[poly.coeff[n].scale(h.numerator,h.denominator*(n+1)) for n in range(DEG)]
   tail=hscale(poly.radius+poly.coeff[DEG].scale(1,DEG+1).abs_upper(),h)
   pair.append(k.TM(coeff,tail))
  out[i][0]=tuple(pair)
 return out,[(z[0].at(),z[1].at()) for row in out for z in row]
def controls():
 ck=c.common.Checks();c.arithmetic_controls(ck);checks={r['name']:r['passed'] for r in ck.rows}
 # Integration is independently checked on tau^24 plus an absolute remainder.
 poly=k.TM([k.ZERO]*DEG+[k.ONE],k.IV.rational(1,7).hi)
 mat=[[(poly,k.TM.constant(k.ZERO,DEG))]]
 ans,end=integrate(mat,[(k.ZERO,k.ZERO)],Q(1,8))
 checks['integration_retains_highest_coefficient_and_remainder']=end[0][0].contains(Q(1,200)+Q(1,56)) and end[0][0].contains(Q(1,200)-Q(1,56))
 # Noncommuting affine triangular propagator; its inverse is not its transpose.
 t,z=s.symbols('t z',real=True);D=s.zeros(3);D[0,1]=1;D[1,2]=t
 U=s.eye(3);U[0,1]=t-z;U[1,2]=(t*t-z*z)/2;U[0,2]=t**3/6-t*z*z/2+z**3/3
 F=U.subs(z,0);V=F.inv()
 checks['noncommuting_forward_equation']=all(s.cancel(q)==0 for q in s.diff(F,t)-D*F)
 checks['right_inverse_equation']=all(s.cancel(q)==0 for q in s.diff(V,t)+V*D)
 checks['inverse_not_transpose']=V!=F.T
 checks['two_time_orientation']=all(s.cancel(q)==0 for q in F*V.subs(t,z)-U)
 return checks

def run_mode(mode,out_string):
 out=ROOT/out_string;progress(out,mode,'starting validated factors and reference')
 bg=c.old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
 src=read(BASE+'a16_finite_state_history_v3_20261116/formulas.json')
 parse=lambda name:s.Matrix([[s.sympify(q,locals=bg.sy) for q in row] for row in src[name]])
 A,B,Cm,D,Pr=[parse(n) for n in ['retained_generator_A','hidden_to_retained_B','retained_to_hidden_C','hidden_generator_D','pressure_row']]
 Ph=Pr[:,8:];Pr=Pr[:,:8];M=parse('mixed_map')
 data=read(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json')
 mats={name:c.old.parent.import_matrix(obj,bg.sy) for name,obj in data.items()}
 L,F,Bal,Bi=[mats[n] for n in ['full_generator','full_field_reconstruction','balancing_map','balancing_map_inverse']]
 E=s.zeros(20,12);Tc=s.zeros(20,8)
 for off,co in [(0,0),(10,6)]:
  E[off,co]=E[off+2,co]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,co+j]=1
 for off,co in [(0,0),(10,4)]:
  Tc[off,co]=1;Tc[off+2,co]=-1
  for j,i in enumerate([1,4,5],1):Tc[off+i,co+j]=1
 extract=E.row_join(Tc).inv()[:12,:]
 Rmap=(M[:8,:]*extract).applyfunc(s.cancel);Pmap=(parse('pressure_row')*M*extract).applyfunc(s.cancel)
 alpha=F[0,:];proper=lambda row,rate:bg.dt(row)+row*L-rate*alpha
 potential=s.expand(bg.energy-(ud*ud+vd*vd+rd*rd+3*pd*pd)/2-rho)
 canonical=ud*proper(F[13,:],ud)+vd*proper(F[14,:],vd)+rd*proper(F[15,:],rd)-sum((s.diff(potential,q)*F[i,:] for q,i in [(u,13),(v,14),(r,15)]),s.zeros(1,20))
 checks={'canonical_pressure_map':all(s.cancel(x)==0 for x in Pmap-canonical)}
 rz=(Rmap*Bi).applyfunc(s.cancel);pz=(Pmap*Bi).applyfunc(s.cancel);rdz=((bg.dt(Rmap)+Rmap*L)*Bi).applyfunc(s.cancel)
 expressions={'D':D,'A':A,'B':B,'C':Cm,'Ph':Ph,'Pr':Pr,'Rz':rz,'Pz':pz,'Rdz':rdz,'Az':mats['balanced_generator']}
 expressions={n:x.subs(bg.ell,mode) for n,x in expressions.items()}
 bc=read(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
 background=[k.TM([k.IV.fraction(Q(pair[0])*T**j) for j,pair in enumerate(row)]) for row in bc['background_coefficients']]
 un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
 boxes={bg.sy[n]:k.IV(k.IV.fraction(Q(z[0])-Q(1,100)).lo,k.IV.fraction(Q(z[1])+Q(1,100)).hi) for n,z in un['background_boxes'].items()}
 ev=c.evaluators(dict(zip(bg.bg,background)),40);be=c.evaluators(boxes)
 globals_={n:[(i,j,ev(re),ev(im)) for i,j,re,im in c.split_matrix(mat)] for n,mat in expressions.items()}
 norms={n:c.matrix_norm(mat,be) for n,mat in expressions.items() if n!='Az'}
 lips={n:c.matrix_lipschitz(mat,bg.bg,be) for n,mat in expressions.items() if n!='Az'}
 oldcert=read(BASE+'a16_pressure_evolution_v3_20261116/receipt.json');old=next(z for z in oldcert['modes'] if z['ell']==mode)
 parent=next(z for z in read(BASE+'a16_finite_state_history_v3_20261116/receipt.json')['modes'] if z['ell']==mode)
 steps=old['steps'];h=T/steps;eb=scaled(old['background_error_upper']);ez=scaled(old['state_error_upper']);mz=scaled(old['state_amplitude_upper'])
 init_values=[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]
 ip=dict(zip(bg.bg,init_values));iev=c.evaluators({**{q:c.evaluators({})(v) for q,v in ip.items()},bg.ell:k.IV.rational(mode)})
 seed=s.zeros(20,1);seed[16]=1
 zstate=[c.complex_center(row[0]) for row in c.interval_matrix(Bal*seed,iev)]
 initz=[[str(q.lo) for q in pair] for pair in zstate]
 checks['identical_reference_initial_recipe']=initz==old['initial_balanced']
 ident=[[(k.ONE if i==j else k.ZERO,k.ZERO) for j in range(4)] for i in range(20)]
 us=[row[:] for row in ident];vs=[row[:] for row in ident]
 prefix=[(k.ZERO,k.ZERO) for _ in range(4)]
 h0=zeros(4,1);h0[2][0]=(k.TM.constant(k.IV.rational(1,mode),DEG),k.TM.constant(k.ZERO,DEG))
 losses={n:0 for n in ['L','Rh','Lp','A','Pr','R','P','Rd','memP','memRd']}
 sizes={n:0 for n in ['L','Rh','Lp','R','I']}
 du=dv=mu=mv=dz=az=diffp=diffr=0;frames=[];chain=hashlib.sha256();sample={}
 for tile in range(steps):
  local={n:c.restrict_entries(entries,tile,steps) for n,entries in globals_.items()}
  um,us,dd,aa=c.state_polynomial(local['D'],us,h);du=max(du,4*dd);mu=max(mu,4*aa)
  vm,vs,dd,aa=c.state_polynomial([(j,i,-re,-im) for i,j,re,im in local['D']],vs,h);dv=max(dv,4*dd);mv=max(mv,4*aa)
  um=[row[:4] for row in um[:4]];vm=transpose([row[:4] for row in vm[:4]])
  zm,zstate,dd,aa=ref.step(local['Az'],zstate,h);dz=max(dz,dd);az=max(az,aa)
  digest=hashlib.sha256(ref.encode([[[q.lo,q.hi] for q in poly.coeff] for pair in zm for poly in pair])).hexdigest();chain.update(bytes.fromhex(digest))
  obs={}
  for key,source,nrows in [('R','Rz',8),('P','Pz',1),('Rd','Rdz',8)]:
   raw=[[pair] for pair in ref.observe(local[source],zm,nrows)];obs[key],loss=center(raw);losses[key]=max(losses[key],loss)
  matrices={n:entries_matrix(local[n],expressions[n].rows,expressions[n].cols) for n in ['B','C','Ph','A','Pr']}
  factors={}
  for key,raw in [('L',multiply(matrices['B'],um)),('Rh',multiply(vm,matrices['C'])),('Lp',multiply(matrices['Ph'],um)),('A',matrices['A']),('Pr',matrices['Pr'])]:
   factors[key],loss=center(raw);losses[key]=max(losses[key],loss)
   if key in sizes:sizes[key]=max(sizes[key],tmnorm(factors[key]))
  integrand=multiply(factors['Rh'],obs['R']);imodel,prefix=integrate(integrand,prefix,h)
  sizes['I']=max(sizes['I'],tmnorm(imodel));sizes['R']=max(sizes['R'],tmnorm(obs['R']))
  mh=plus(h0,imodel)
  memp,loss=center(plus(multiply(factors['Pr'],obs['R']),multiply(factors['Lp'],mh)));losses['memP']=max(losses['memP'],loss)
  memrd,loss=center(plus(multiply(factors['A'],obs['R']),multiply(factors['L'],mh)));losses['memRd']=max(losses['memRd'],loss)
  diffp=max(diffp,tmnorm(minus(memp,obs['P'])));diffr=max(diffr,tmnorm(minus(memrd,obs['Rd'])))
  frames.append({'tile':tile,'L':pack(factors['L']),'Rh':pack(factors['Rh']),'Lp':pack(factors['Lp']),'R_reference':pack(obs['R']),'P_reference':pack(obs['P']),'P_memory':pack(memp),'R_rate_reference':pack(obs['Rd']),'R_rate_memory':pack(memrd)})
  # Nine independent diagnostic sample times, including t=0.
  if tile==0:sample[0]={'U':numeric(um,Q(0)),'V':numeric(vm,Q(0)),'L':numeric(factors['L'],Q(0)),'Rh':numeric(factors['Rh'],Q(0)),'Lp':numeric(factors['Lp'],Q(0))}
  if (tile+1)*8%steps==0:
   index=(tile+1)*8//steps;sample[index]={'U':numeric(um),'V':numeric(vm),'L':numeric(factors['L']),'Rh':numeric(factors['Rh']),'Lp':numeric(factors['Lp'])}
  if tile==0 or (tile+1)%64==0 or tile+1==steps:progress(out,mode,f'tile {tile+1}/{steps}')
 checks['reference_polynomial_chain']=chain.hexdigest()==old['tile_chain_sha256']
 checks['reference_defect_and_amplitude']=Q(k.upper_fraction(dz))==Q(old['state_defect_upper']) and Q(k.upper_fraction(az))==Q(old['state_amplitude_upper'])
 forcing_u=du+times(times(lips['D'],eb),mu);forcing_v=dv+times(times(lips['D'],eb),mv)
 amp=k.exp_upper(k.IV(norms['D']).scale(T.numerator,T.denominator))
 eu=times(amp,hscale(forcing_u,T));evi=times(amp,hscale(forcing_v,T))
 eL=times(norms['B'],eu)+times(times(lips['B'],eb),mu)+losses['L']
 eRh=times(norms['C'],evi)+times(times(lips['C'],eb),mv)+losses['Rh']
 eLp=times(norms['Ph'],eu)+times(times(lips['Ph'],eb),mu)+losses['Lp']
 eA=times(lips['A'],eb)+losses['A'];ePr=times(lips['Pr'],eb)+losses['Pr']
 errors={}
 for key,source in [('R','Rz'),('P','Pz'),('Rd','Rdz')]:errors[key]=times(norms[source],ez)+times(times(lips[source],eb),mz)+losses[key]
 eK=times(eL,sizes['Rh'])+times(sizes['L'],eRh)+times(eL,eRh)
 eKP=times(eLp,sizes['Rh'])+times(sizes['Lp'],eRh)+times(eLp,eRh)
 eI=hscale(times(eRh,sizes['R'])+times(sizes['Rh'],errors['R'])+times(eRh,errors['R']),T)
 Hprop=scaled(parent['gains']['hidden_propagator_infinity']);hplus=k.IV.rational(1,mode).hi+sizes['I']
 emP=times(norms['Pr'],errors['R'])+times(ePr,sizes['R'])+times(eLp,hplus)+times(times(norms['Ph'],Hprop),eI)+losses['memP']
 emRd=times(norms['A'],errors['R'])+times(eA,sizes['R'])+times(eL,hplus)+times(times(norms['B'],Hprop),eI)+losses['memRd']
 allerrors={'U':eu,'V':evi,'L':eL,'Rh':eRh,'Lp':eLp,'A':eA,'Pr':ePr,'kernel_retained':eK,'kernel_pressure':eKP,'integral_physical':eI,'pressure_memory':emP,'retained_rate_memory':emRd,**{'reference_'+n:q for n,q in errors.items()}}
 for n in ['kernel_retained','kernel_pressure','pressure_memory','retained_rate_memory']:
  checks[n+'_absolute_accuracy']=allerrors[n]<k.IV.rational(1,10**8).lo
 checks['continuous_pressure_reconstruction_agreement']=diffp<k.IV.rational(1,10**8).lo
 checks['continuous_retained_rate_reconstruction_agreement']=diffr<k.IV.rational(1,10**8).lo
 # Independent solve of the actual background and both fundamental equations.
 df=s.lambdify([list(bg.bg)],expressions['D'],'numpy',cse=True);rf=s.lambdify([list(bg.bg)],bg.rates,'numpy',cse=True)
 bfun=s.lambdify([list(bg.bg)],expressions['B'],'numpy',cse=True);cfun=s.lambdify([list(bg.bg)],expressions['C'],'numpy',cse=True);pfun=s.lambdify([list(bg.bg)],expressions['Ph'],'numpy',cse=True)
 def rhs(t,y):
  d=np.asarray(df(y[:11]));un=y[11:27].reshape(4,4);vn=y[27:].reshape(4,4)
  return np.r_[np.asarray(rf(y[:11])).reshape(11),(d@un).reshape(16),(-vn@d).reshape(16)]
 y0=np.r_[np.array([float(z) for z in init_values]),np.eye(4).reshape(16),np.eye(4).reshape(16)].astype(complex)
 sol=solve_ivp(rhs,(0,float(T)),y0,method='DOP853',rtol=2e-12,atol=2e-14,max_step=min(.001,1/mode**2),t_eval=np.linspace(0,float(T),9));assert sol.success
 pairs=[];maximum=invmax=0.
 for i in range(9):
  yi=sol.y[:,i];ui=yi[11:27].reshape(4,4);bi=np.asarray(bfun(yi[:11]));phi=np.asarray(pfun(yi[:11]))
  invmax=max(invmax,float(np.max(np.abs(sample[i]['U']@sample[i]['V']-np.eye(4)))))
  for j in range(i+1):
   yj=sol.y[:,j];vj=yj[27:].reshape(4,4);cj=np.asarray(cfun(yj[:11]))
   kr=sample[i]['L']@sample[j]['Rh'];kp=sample[i]['Lp']@sample[j]['Rh']
   delta=max(float(np.max(np.abs(kr-bi@ui@vj@cj))),float(np.max(np.abs(kp-phi@ui@vj@cj))))
   maximum=max(maximum,delta);pairs.append({'t_index':i,'s_index':j,'kernel_error':delta,'retained_kernel_max_entry':float(np.max(np.abs(kr))),'pressure_kernel_max_entry':float(np.max(np.abs(kp)))})
 checks['independent_DOP853_two_time_control']=maximum<1e-7
 checks['inverse_identity_sample_control']=invmax<1e-10
 folder=out/('ell_'+str(mode));folder.mkdir(exist_ok=False)
 archive={'schema':'a16-separable-kernel-curves-v1','ell':mode,'steps':steps,'T':str(T),'degree':DEG,'dyadic_scale':str(k.SCALE),'frames':frames,'physical_error_bounds':{n:k.upper_fraction(q) for n,q in allerrors.items()}}
 compressed=gzip.compress(json.dumps(archive,sort_keys=True,separators=(',',':')).encode(),compresslevel=6,mtime=0)
 pth=folder/'curves.json.gz';pth.write_bytes(compressed);Path(str(pth)+'.sha256').write_text(hashlib.sha256(compressed).hexdigest()+'  '+pth.name+'\n',encoding='utf-8')
 result={'ell':mode,'checks':checks,'steps':steps,'errors':{n:k.upper_fraction(q) for n,q in allerrors.items()},'norms':{n:k.upper_fraction(q) for n,q in norms.items()},'lipschitz':{n:k.upper_fraction(q) for n,q in lips.items()},'nominal_amplitudes':{n:k.upper_fraction(q) for n,q in sizes.items()},'centering_errors':{n:k.upper_fraction(q) for n,q in losses.items()},'fundamental':{n:k.upper_fraction(q) for n,q in [('U_defect',du),('V_defect',dv),('U_amplitude',mu),('V_amplitude',mv),('absolute_Gronwall_amplification',amp),('background_error',eb),('hidden_propagator_bound',Hprop)]},'reference_state_error':k.upper_fraction(ez),'reference_state_amplitude':k.upper_fraction(mz),'reference_chain':chain.hexdigest(),'difference_majorants':{'pressure':k.upper_fraction(diffp),'retained_rate':k.upper_fraction(diffr)},'independent_solver_kernel_max_error':maximum,'inverse_identity_max_error':invmax,'diagnostic_pairs':pairs,'archive_sha256':hashlib.sha256(compressed).hexdigest(),'archive_bytes':len(compressed)}
 save(folder/'receipt.json',result);progress(out,mode,'complete '+json.dumps({n:float(Q(result['errors'][n])) for n in ['kernel_retained','kernel_pressure','pressure_memory','retained_rate_memory']}))
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=read(PINS);before={p:(sha(p),(ROOT/p).stat().st_mtime_ns) for p in pins};assert all(before[p][0]==h for p,h in pins.items())
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False);checks=controls()
 if not all(checks.values()):
  save(out/'preflight_failure.json',checks);raise RuntimeError('Preflight failures '+str([n for n,v in checks.items() if not v]))
 with ProcessPoolExecutor(max_workers=5) as pool:rows=list(pool.map(run_mode,[4,8,16,32,64],[args.output_dir]*5))
 for row in rows:
  checks.update({str(row['ell'])+'_'+n:v for n,v in row['checks'].items()})
 checks['immutable_source_hashes_and_timestamps']=all((sha(p),(ROOT/p).stat().st_mtime_ns)==before[p] for p in pins)
 receipt={'status':'PASS_VALIDATED_TWO_TIME_KERNEL_AND_HISTORY_RECONSTRUCTION' if all(checks.values()) else 'FAIL_VALIDATED_TWO_TIME_KERNEL_AND_HISTORY_RECONSTRUCTION','checks':checks,'passed':sum(checks.values()),'total':len(checks),'inputs':pins,'modes':rows,'domain':{'t':['0','1/20'],'retarded_triangle':'0<=s<=t<=1/20','ell':[4,8,16,32,64]},'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Uniform piecewise-polynomial two-time kernel accuracy and pressure/rate reconstruction using the certified full retained history. Not independent retained-only Volterra evolution, irreversible memory, a physical window or matching.'}
 save(out/'receipt.json',receipt);print(json.dumps({n:receipt[n] for n in ['status','passed','total','physics_pass']}),flush=True)
 if not all(checks.values()):raise SystemExit(1)
if __name__=='__main__':main()
