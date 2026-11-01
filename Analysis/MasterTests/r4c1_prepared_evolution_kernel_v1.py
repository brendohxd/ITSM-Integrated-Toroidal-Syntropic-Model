"""Compose the completed local rows; this is not a physical-domain theorem.

Inputs dq,dd,dp contain the THIRTEEN nonauxiliary canonical fields, with
J2 spatial jets (dd is the field derivative, including its own second jet).
psi4 and dpsi4 are explicit fourth derivatives. The caller supplies the
gauge/coordinate-corrected shift jets; this kernel does not determine a
global periodic inverse, charge compatibility or an evolving function space.
Output nonauxiliary field rates have J2 jets. Zdot is VALUE ONLY. Scalar
momentum-rate spatial derivatives are never returned as computed zeros.
"""
from pathlib import Path
import hashlib,importlib.util
import mpmath as mp

def load(name):
 path=Path(__file__).with_name(name+'.py')
 assert hashlib.sha256(path.read_bytes()).hexdigest()==Path(str(path)+'.sha256').read_text().split()[0].lower()
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def apply(ctx,dq,dd,dp,psi4,dpsi4,dS,dSz):
 assert len(dq)==len(dd)==len(dp)==13,'supply nonauxiliary canonical slots only'
 assert len(dS)==len(dSz)==3
 assert psi4 is not None and dpsi4 is not None,'fourth force jets are required'
 J=ctx['J'];hj=ctx['hj'];gradient=ctx['gradient'];L=ctx['L']
 dz=lambda x:J(coefficients=[x.c[1],2*x.c[2],mp.iv.mpf(0)])
 flow=load('r4c1_prepared_canonical_flow_v2');aux=load('r4c1_auxiliary_geometry_rate_v1')
 current=load('r4c1_clock_current_transport_v1');density=load('r4c1_density_time_transport_v1')
 dq=list(dq)+[J(0)];dd=list(dd)+[J(0)];dp=list(dp)+[J(0)]
 first=flow.apply(ctx,dq,dd,dp,dS,dSz)
 ar=aux.apply(ctx,ctx['q'],ctx['d'],psi4,ctx['v'],dq,dd,dpsi4,first['field_rate']+[J(0)])
 dq[13]=ar['delta_Z'];dd[13]=dz(dq[13])
 rate=flow.apply(ctx,dq,dd,dp,dS,dSz);dv=rate['field_rate']+[J(0)];dy=dq+dv+dd+list(dS)+list(dSz)
 pd=[];dpd=[]
 for i in range(14):
  f=gradient(L,i);g=gradient(L,28+i)
  df=sum((hj(L,i,k)*dy[k] for k in range(48)),J(0));dg=sum((hj(L,28+i,k)*dy[k] for k in range(48)),J(0))
  # Internal first coefficients for scalar rows are unused by the density
  # improvement. They are deliberately not exposed in the return value.
  pd.append(J(coefficients=[f.c[0]-g.c[1],f.c[1]-2*g.c[2] if i<9 else mp.iv.mpf(0),mp.iv.mpf(0)]))
  dpd.append(J(coefficients=[df.c[0]-dg.c[1],df.c[1]-2*dg.c[2] if i<9 else mp.iv.mpf(0),mp.iv.mpf(0)]))
 mapped=density.evaluate(ctx,dq,dd,dp,dv,dS,dSz,pd,dpd,ar['Zdot'],ar['delta_Zdot'])
 clock=current.linearized(ctx,ctx['q'],ctx['d'],ctx['v'],ctx['S'],ctx['Sz'],dq,dd,dv,dS,dSz,mapped['density'],mapped['delta_density'])
 return dict(field_rate_nonaux=rate['field_rate'],momentum_rate=rate['momentum_rate'],
  metric_frame_momentum_rate_dz=[t.c[1] for t in dpd[:9]],
  auxiliary=ar['delta_Z'],auxiliary_rate_value=ar['delta_Zdot'],auxiliary_secondary_tangent=rate['auxiliary_secondary_tangent'],
  density=mapped['density'],delta_density=mapped['delta_density'],density_rate=clock['density_rate'],direct_density_rate=mapped['delta_density_rate'],
  background_clock_residual=mapped['density_rate']-(ctx['S'][2]*mapped['density']+clock['background_flux'][2]).c[1],
  delta_clock_residual=mapped['delta_density_rate']-clock['density_rate'],
  auxiliary_background_mismatch=[ar['Z'].c[k]-ctx['q'][13].c[k] for k in range(3)],
  inverse_errors=rate['inverse_errors'],physical_norm='NOT_DERIVED',global_gauge_and_compatible_domain='CALLER_REQUIRED',
  auxiliary_time_spatial_rates='NOT_RETURNED',scalar_momentum_time_spatial_rates='NOT_RETURNED',physical_clearance=False)
