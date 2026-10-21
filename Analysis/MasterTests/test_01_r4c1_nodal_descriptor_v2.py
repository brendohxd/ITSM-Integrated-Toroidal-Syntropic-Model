"""Undivided R4C1 node descriptor and nonuniform unweighted symplectic inverse."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,importlib.util,json,multiprocessing,traceback
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sy
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_planar_reduced_hamiltonian_v1.py'
PSHA='f03a2b9ac794569994be8112b0ba1746b8e596669c2d693c9c7310bd48cab27b'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_NODAL_DESCRIPTOR_V1_CONTRACT_2026-10-19.md'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+chr(10)).encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift before import')
spec=importlib.util.spec_from_file_location('frozen_planar_reduction',ROOT/PARENT)
planar=importlib.util.module_from_spec(spec);spec.loader.exec_module(planar)
canonical,base,v4=planar.canonical,planar.base,planar.v4
tensor_h=canonical.tensor_h
HM=canonical.HM
reg=planar.parent.reg
PINS=dict(planar.PINS)
PINS.update({
 'Analysis/MasterTests/test_01_r4c1_nodal_descriptor_v1.py':'86b1c665d2130fd48fb75fbb6b5aa4fe5ee7518dbd2a1a5b3e7c34646573343f',
 'Theory/Gates/RES-001/RES001_R4C1_NODAL_DESCRIPTOR_V2_BINDING_ADDENDUM_2026-10-19.md':'8ad10bc9ef42496713d66d82b625922249327c0563cee1f2ab4dbf3cc92b6b83',
 'Analysis/MasterTests/outputs/r4c1_nodal_descriptor_attempt_01/summary.json':'4a534ce4d1245820a5796a887e1a65d2744a2d8d7d4bdfda861233aa1c3cf61f',
 'Analysis/MasterTests/outputs/r4c1_nodal_descriptor_attempt_01/formulas.json':'280ee1834ef44e3428990563baa98951a2c43a147b5464dc2b04c8b66fafcfd2',
 'Analysis/MasterTests/outputs/r4c1_nodal_descriptor_attempt_01/independent.json':'3d4da9e9865424209dd616053deba58a8ea0dd0e10ad3542612f940e06196074',
 PARENT:PSHA,CONTRACT:'1cd091d3f41e51e5face8bead912c765124cc54a8eb75f37968c18ae6bdb7e2b',
 'Theory/Gates/RES-001/RES001_R4C1_PLANAR_REDUCED_HAMILTONIAN_V1_REPORT_2026-10-19.md':
 '175c41f50b18bb32c6b1b38edb255e61bcd656643f226c8e49171545c051c673',
 'Theory/Gates/RES-001/RES001_R4C1_REGULATOR_NODE_V1_REPORT_2026-10-17.md':
 'b47dcf5e7fc340a015f2e7cdf273157bc6e2e1ba311bbc543a5f66596dbc83d2'})
_PROGRESS=None
def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+chr(10))
def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,digest in pins.items():
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest or side.read_text().split()[0].lower()!=digest:
            raise ValueError('source/sidecar drift '+name)
        for q in (p,side):
            raw=q.read_bytes();meta[q.relative_to(ROOT).as_posix()]=dict(
                sha256=SHA(raw),bytes=len(raw),mtime_ns=q.stat().st_mtime_ns)
    return pins,meta

def partial_blocks(q,hi,grad,DV,p,par,R3,clock_s):
    """Undivided scalar-rate partial Legendre transform in the exact psi=tau gauge."""
    if np.max(abs(grad[:,12,:]))>1e-12:raise ValueError("not in force-clock spatial gauge")
    grad=grad.copy();grad[:,12,:]=0
    psihat=np.broadcast_to(clock_s,(len(q),))
    if np.any(np.real(psihat)<=0):raise ValueError("nonpositive force clock")
    h=tensor_h(q);V=q[:,6:9];vl=np.einsum('nij,nj->ni',h,V)
    v2=np.einsum('ni,ni->n',vl,V);gam=np.sqrt(1+v2);volume=np.sqrt(np.linalg.det(h))
    n=np.column_stack((gam,V));G=np.zeros((len(q),4,4),dtype=q.dtype);Gi=G.copy()
    G[:,0,0]=Gi[:,0,0]=-1;G[:,1:,1:]=h;Gi[:,1:,1:]=hi
    basis=np.zeros((len(q),9,4,4),dtype=q.dtype);E=np.zeros((6,3,3))
    for a,(i,j) in enumerate(HM):E[a,i,j]=E[a,j,i]=1
    mix=np.einsum('nij,ajk->naik',hi,E)
    b0=np.einsum('naij,nj->nai',mix,V)
    basis[:,:6,0,0]=np.einsum('ni,nai->na',vl,b0)/gam[:,None]
    basis[:,:6,0,1:]=b0
    basis[:,:6,1:,0]=np.einsum('aij,nj->nai',E,V)
    basis[:,:6,1:,1:]=gam[:,None,None,None]*mix.swapaxes(2,3)
    for j in range(3):basis[:,6+j,0,0]=vl[:,j]/gam;basis[:,6+j,0,j+1]=1
    bg=np.zeros((len(q),4,4),dtype=q.dtype)
    bg[:,1:,0]=np.einsum('nj,nij->ni',vl,DV)/gam[:,None];bg[:,1:,1:]=DV
    acc=np.einsum('ni,naij->naj',n,basis);accbg=np.einsum('ni,nij->nj',n,bg)
    def bilinear(A,B):
        a=np.einsum('ni,naij->naj',n,A);b=np.einsum('ni,naij->naj',n,B)
        return -par['MU2']*(par['c1']*np.einsum('nij,nkl,naik,nbjl->nab',Gi,G,A,B)
            +par['c2']*np.einsum('na,nb->nab',np.trace(A,axis1=2,axis2=3),np.trace(B,axis1=2,axis2=3))
            +par['c3']*np.einsum('naij,nbji->nab',A,B)
            -par['c4']*np.einsum('nai,nij,nbj->nab',a,G,b))
    R=np.zeros((len(q),12,12),dtype=q.dtype);R[:,:9,:9]=bilinear(basis,basis)
    tm=np.trace(mix,axis1=2,axis2=3)
    R[:,:6,:6]+=par['MP2']*(np.einsum('naij,nbji->nab',mix,mix)-np.einsum('na,nb->nab',tm,tm))
    current=np.column_stack((q[:,10],-q[:,9],np.zeros(len(q))))
    R[:,9:,9:]=np.eye(3)-par['zeta']*v2[:,None,None]*np.einsum('ni,nj->nij',current,current)
    dq=grad[:,12,:];dz=grad[:,13,:];Vq=np.einsum('ni,ni->n',V,dq)
    pcov=np.column_stack((psihat,dq))
    ell=np.zeros((len(q),12),dtype=np.result_type(q,p,psihat))
    ell[:,:9]=bilinear(basis,bg[:,None,:,:])[:,:,0]-par['b']*q[:,13,None]*np.einsum('nai,ni->na',acc,pcov)
    J=q[:,10,None]*grad[:,9,:]-q[:,9,None]*grad[:,10,:]
    VJ=np.einsum('ni,ni->n',V,J)
    ell[:,9:]=-par['zeta']*gam[:,None]*VJ[:,None]*current
    canonical_grad=sum(np.einsum('ni,nij,nj->n',grad[:,k,:],hi,grad[:,k,:]) for k in (9,10,11))
    ss=q[:,9]**2+q[:,10]**2
    potential=par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)+par['mr2']*q[:,11]**2/2+par['lambda_r']*q[:,11]**4/4+par['g_r']*ss*q[:,11]**2/4+par['rho_Lambda']
    Q=gam*psihat+Vq;Y=v2*psihat**2
    framebg=bilinear(bg[:,None,:,:],bg[:,None,:,:])[:,0,0]/2
    f=(par['MP2']*R3/2+framebg-canonical_grad/2-potential
        -par['zeta']*(np.einsum('ni,nij,nj->n',J,hi,J)+VJ**2)/2
        +par['K_Q']*Q**2/2-par['A']*Y**1.5+par['b']*q[:,13]**2/2
        -par['b']*(np.einsum('ni,nij,nj->n',dz,hi,dq)+np.einsum('ni,ni->n',V,dz)*Q)
        -par['b']*q[:,13]*np.einsum('ni,ni->n',accbg,pcov))
    P=np.column_stack((2*p[:,:6],p[:,6:12]))/volume[:,None]
    y=np.linalg.solve(R,(P-ell)[...,None])[...,0]
    energy=volume*(np.einsum('ni,ni->n',P-ell,y)/2-f)
    C=np.exp(par['beta']*q[:,12]);dT=grad[:,14,:]
    dust=p[:,14]*np.sqrt(C*C+np.einsum('ni,nij,nj->n',dT,hi,dT))
    flux=gam*np.einsum('ni,ni->n',hi[:,2,:],p[:,6:9])
    return energy+dust,flux,dict(R=R,ell=ell,y=y,psi_hat=psihat,Y=Y,volume=volume,gamma=gam,f=f,g=volume*par['b']*v2)


def exact(ch):
    q,p,s,Z,b,N,pz,ppsi,zh,zd,E,D,J=sy.symbols('q p s Z b N pZ ppsi Zhat Zdot E Edust J',real=True)
    gg=sy.Function('g')(q)
    before=p+ppsi+pz*zd-N*(E+ppsi*s+(pz+gg*s)*zh+D+J)
    ch.zero('clock_varied_before_elimination',sy.diff(before,ppsi)-(1-N*s))
    ch.zero('undivided_multiplier_row',sy.diff(before,zh)+N*(pz+gg*s))
    after=before.subs({N:1/s,pz:-gg*s})
    ch.zero('exact_nodal_action_pullback',after-(p-gg*s*zd-(E+D+J)/s))
    ch.zero('multiplier_constraint_solved_without_g_inverse',sy.diff(pz+gg*s,pz)-1)
    coords=(q,p,s,Z);theta=sy.Matrix([p,0,0,-gg*s])
    Om=sy.Matrix(4,4,lambda i,j:sy.diff(theta[j],coords[i])-sy.diff(theta[i],coords[j]))
    closure=[sy.diff(Om[i,j],coords[k])+sy.diff(Om[j,k],coords[i])+sy.diff(Om[k,i],coords[j])
             for i in range(4) for j in range(i+1,4) for k in range(j+1,4)]
    ch.zero('closed_two_form_including_crosses',closure)
    ch.zero('scalar_rate_regulator_two_form_entry',Om[2,3]+gg)
    ch.zero('coordinate_regulator_cross_retained',Om[0,3]+s*sy.diff(gg,q))
    ch.add('dropping_coordinate_cross_breaks_closure',sy.diff(Om[2,3],q)!=0)
    K,v,ss=sy.symbols('K volume positive_s',positive=True)
    Er=sy.Symbol('Eother',real=True)
    H=(Er+D+J-v*K*ss**2/2)/ss
    ch.zero('node_scalar_rate_row_is_energy_compatibility',
            sy.diff(H,ss)+(Er+D+J+v*K*ss**2/2)/ss**2)
    # Full metric-volume and frame response of g=b*sqrt(h)*V.h.V.
    hs=sy.symbols('hxx hxy hxz hyy hyz hzz',real=True)
    hm=sy.Matrix([[hs[0],hs[1],hs[2]],[hs[1],hs[3],hs[4]],[hs[2],hs[4],hs[5]]])
    dhs=sy.symbols('dhxx dhxy dhxz dhyy dhyz dhzz',real=True)
    dh=sy.Matrix([[dhs[0],dhs[1],dhs[2]],[dhs[1],dhs[3],dhs[4]],[dhs[2],dhs[4],dhs[5]]])
    V=sy.Matrix(sy.symbols('Vx Vy Vz'));dV=sy.Matrix(sy.symbols('dVx dVy dVz'))
    cc=(V.T*hm*V)[0]
    dc=sum(sy.diff(cc,a)*da for a,da in zip(hs,dhs))+sum(sy.diff(cc,a)*da for a,da in zip(V,dV))
    ch.zero('all_metric_frame_variations_of_c',dc-(V.T*dh*V)[0]-2*(dV.T*hm*V)[0])
    det=hm.det();ddet=sum(sy.diff(det,a)*da for a,da in zip(hs,dhs))
    ch.zero('metric_volume_variation',ddet-sy.trace(hm.adjugate()*dh))
    ch.zero('g_and_first_variation_vanish_at_alignment',[cc.subs(dict.fromkeys(V,0)),dc.subs(dict.fromkeys(V,0))])
    x,t,sl,rate,dx,dy,dz,dv,ds=sy.symbols('x t slope rate dVx dVy dVz dvolume ds',real=True)
    cpert=(t*dx)**2+(sl*x+t*dy)**2+(t*dz)**2
    ppert=-b*(1+t*dv)*cpert*(rate+t*ds)
    dp=sy.diff(ppert,t).subs(t,0)
    ch.zero('moving_node_delta_pZ_value',dp.subs(x,0))
    ch.zero('moving_node_delta_pZ_normal_jet',sy.diff(dp,x).subs(x,0)+2*b*rate*sl*dy)
    ddp=sy.diff(ppert.subs(t,0),x,2).subs(x,0)
    ch.zero('moving_node_coordinate_correction',sy.diff(dp,x).subs(x,0)-dy/sl*ddp)
    ch.add('fixed_old_node_derivative_would_reject_motion',sy.diff(dp,x).subs(x,0)!=0)
    ch.zero('transverse_node_lifting_not_discarded',
            sy.expand(cpert.subs(x,-t*dy/sl))-t*t*(dx*dx+dz*dz))
    u=sy.Symbol('u',real=True)
    I0=sy.integrate((1-u*u)**6,(u,-1,1));I4=sy.integrate(u**4*(1-u*u)**6,(u,-1,1))
    ch.zero('normalized_bump_integral',I0-sy.Rational(2048,3003))
    ch.zero('bump_fourth_moment',I4/I0-sy.Rational(1,85))
    return dict(
        action='Theta_other-g*s*dZ-Hpsi(s)*dtau; g=b*volume*V.h.V, pZ=-g*s',
        elimination='vary ppsi,N,pZ,Zhat first; N=1/s and pZ=-g*s eliminate multiplier pair without dividing g',
        partial_Hamiltonian='Hpsi(s)=<(E0(s)+Edust+div F)/s>; same full spatial/global reduction with pZ=-g*s',
        two_form='dTheta_other-g*ds wedge dZ-s*dg wedge dZ',
        metric_frame_variation='dg=b*volume*[c*tr(h^-1 dh)/2+V^T dh V+2*dV^T*h*V]',
        descriptor_rows='-g*Zdot-H_s=0; d_tau(g*s)-H_Z=0; other canonical momenta include -s*g_q*Zdot',
        linearized_descriptor='Omega_ij*d_tau(deltaX^j)+[(d_k Omega_ij)*Xdot_bg^j-Hessian(Hpsi)_ik]*deltaX^k=0',
        background_drift_required=True,
        aligned_rows='H_s=-(Eother+Edust+divF+volume*K_Q*s^2/2)/s^2=0; Ppsi=K_Q*s; original Z row chi=Z+s*divV=0',
        tangent_domain='delta pZ(node)=0; delta pZprime(node)=-2*b*p*wprime*deltaVy; dz_node=-deltaVy/wprime',
        node_lifting='Transverse deltaV can lift rather than move the alignment surface; no imposed persistence or mode removal',
        inverse_bound='unit L2 delta_s bump: ||Omega delta_s||<=b*e^2*k^2*epsilon^2/sqrt(85), tends to zero',
        conclusion='No uniform bounded inverse on this unrestricted unweighted L2 tangent space. Not a Cauchy/physical ghost or all-formulation no-go.',
        remaining='Actual mixed-order/weighted domain, full coupled functional Hessian/background drift, spectrum and physical window remain open')
def local_control(ch,par,point,eta,orientation,angle):
    mp.mp.dps=100;rat=sy.Rational(eta);et=mp.mpf(rat.p)/rat.q;e=mp.mpf(1)/500;k=mp.mpf(40);rate=et/5
    a=mp.mpf(angle);w=orientation*e*mp.sin(a);wp=orientation*e*k*mp.cos(a)
    H,U,Ud=[mp.mpf(point[n]) for n in ('H','U','Ud')]
    Rc=mp.sqrt(et);D=Rc/(1-par['zeta']*Rc**2*e**2/2)
    yy=[H,H/13,H/17,H*mp.mpf('1.01'),-wp/23,H*mp.mpf('.99'),et/37,-H*w,-et/41,0,D,Rc/4]
    config=dict(h=mp.eye(3),hi=mp.eye(3),V=mp.matrix([0,w,0]),gamma=mp.sqrt(1+w*w),
        DV=mp.matrix([[0,0,0],[0,0,0],[0,wp,0]]),u=Rc,v=mp.mpf(0),r=Rc,psi=mp.mpf(0),Z=U*w*w,
        R3=et/19,epsilon=mp.mpf(1),proper={'T':mp.mpf(1)},
        spatial={n:mp.matrix([0,0,2*U*w*wp if n=='Z' else 0]) for n in ('u','v','r','psi','Z','T')})
    y=mp.matrix(yy);zh=Ud*w*w;body=lambda y,s,z:canonical.mp_body(config,par,y,s,z,include_dust=False)
    PY=[]
    for j in range(12):
        def fy(t):
            vy=mp.matrix(y);vy[j]=t
            return body(vy,rate,0)
        PY.append(mp.diff(fy,y[j]))
    PY=mp.matrix(PY)
    psi0=mp.diff(lambda s:body(y,s,0),rate);Ppsi=mp.diff(lambda s:body(y,s,zh),rate)
    PZ=mp.diff(lambda z:body(y,rate,z),zh)
    E0=(PY.T*y)[0]-body(y,rate,0)
    J=et/97;rho=-(E0+Ppsi*rate+J);g=par['b']*w*w
    Hs=-psi0/rate-(E0+rho+J)/rate**2
    tag=f'{orientation}_{angle}_'
    ch.small(tag+'original_undivided_momentum',abs(PZ+g*rate),'1e-45')
    ch.small(tag+'original_scalar_rate_descriptor_row',abs(Hs+g*zh/rate),'1e-45')
    ch.add(tag+'positive_local_dust_control',rho>0,base.SHOW(rho))
    if not w:
        ch.small(tag+'aligned_scalar_momentum',abs(Ppsi-par['K_Q']*rate),'1e-45')
        # E0 already contains -K_Q*s^2/2; Eother=E0+K_Q*s^2/2.
        ch.small(tag+'aligned_energy_compatibility',abs(E0+rho+J+par['K_Q']*rate**2),'1e-45')
    # Independent original-density polarization, all temporal complement entries at nodes.
    R0=None;polerr=mp.mpf(0)
    if not w:
        z=mp.zeros(12,1);basis=[mp.matrix([int(i==j) for i in range(12)]) for j in range(12)]
        f0=body(z,rate,0);ff=[body(v,rate,0) for v in basis]
        R0=mp.matrix([[body(basis[i]+basis[j],rate,0)-ff[i]-ff[j]+f0 for j in range(12)] for i in range(12)])
    q=np.zeros((1,15));q[0,[0,3,5]]=1;q[0,7]=float(w)
    q[0,9]=q[0,11]=float(Rc);q[0,13]=float(U*w*w)
    grad=np.zeros((1,15,3));grad[0,13,2]=float(2*U*w*wp)
    DV=np.zeros((1,3,3));DV[0,2,1]=float(wp)
    p=np.zeros_like(q);pn={name:float(v) for name,v in par.items()}
    args=(q,np.eye(3)[None,:,:],grad,DV,p,pn,np.array([float(et/19)]))
    _,_,co=partial_blocks(*args,float(rate))
    yn=np.array([float(v) for v in yy]);npPY=co['R'][0]@yn+co['ell'][0]
    npPY0=np.array([float(v) for v in PY])
    p[0,:6]=npPY[:6]/2;p[0,6:12]=npPY[6:]
    p[0,13]=float(-g*rate);p[0,14]=float(rho)
    E,flux,out=partial_blocks(*args,float(rate))
    # E includes independently eliminated dust; compare E0 separately.
    err=max(abs(npPY-npPY0)/(1+abs(npPY)+abs(npPY0)))
    err=max(err,abs(E[0]-float(E0+rho))/(1+abs(E[0])+abs(float(E0+rho))))
    if R0 is not None:
        target=np.array([[float(R0[i,j]) for j in range(12)] for i in range(12)])
        polerr=float(np.max(abs(co['R'][0]-target)/(1+abs(co['R'][0])+abs(target))))
        err=max(err,polerr)
    ch.small(tag+'original_density_partial_Legendre_control',mp.mpf(float(err)),'1e-8')
    step=1e-20
    Ev,_,_=partial_blocks(*args,complex(float(rate),step))
    deriv=np.imag((Ev[0]+float(J))/complex(float(rate),step))/step
    row_error=abs(float(rate)**2*(deriv-float(Hs)))/(1+abs(float(E0))+float(rho)+abs(float(J)))
    ch.small(tag+'undivided_clock_row_binary64',mp.mpf(float(row_error)),'1e-8')
    # Metric/frame cross in dg, including the volume determinant.
    dh=mp.matrix([[mp.mpf(1)/13,mp.mpf(1)/17,mp.mpf(1)/19],
                  [mp.mpf(1)/17,-mp.mpf(1)/23,mp.mpf(1)/29],
                  [mp.mpf(1)/19,mp.mpf(1)/29,mp.mpf(1)/31]])
    dv=mp.matrix([mp.mpf(1)/37,mp.mpf(1)/41,-mp.mpf(1)/43]);V=config['V']
    gg=lambda t:par['b']*mp.sqrt(mp.det(mp.eye(3)+t*dh))*((V+t*dv).T*(mp.eye(3)+t*dh)*(V+t*dv))[0]
    want=par['b']*(w*w*sum(dh[i,i] for i in range(3))/2+(V.T*dh*V)[0]+2*(dv.T*V)[0])
    ch.small(tag+'original_metric_frame_dg',abs(mp.diff(gg,0)-want),'1e-45')
    if w:
        ch.add(tag+'omitted_metric_frame_cross_rejected',want!=0)
    return dict(orientation=orientation,normal_angle=angle,E0=base.SHOW(E0),local_dust=base.SHOW(rho),
        scalar_rate_row=base.SHOW(Hs),binary64_undivided_row_error=repr(float(row_error)),
        original_density_error=repr(float(err)),nodal_polarization_error=str(polerr))
def case_job(task):
    index,family,eta,point=task;mp.mp.dps=100;ch=base.Checks()
    par=canonical.parameters(family,eta,'mp');records=[]
    try:
        for sign in (-1,1):
            for angle in ('0','1e-2','-1e-2','1e-6','-1e-6'):
                records.append(local_control(ch,par,point,eta,sign,angle))
        I0=mp.mpf(2048)/3003;e=mp.mpf(1)/500;k=mp.mpf(40);C=par['b']*e*e*k*k
        probes=[]
        for angle in ('1e-2','1e-3'):
            eps=mp.mpf(angle)/k
            val=mp.sqrt(mp.quad(lambda u:(par['b']*e*e*mp.sin(k*eps*u)**2)**2*(1-u*u)**6,[-1,0,1])/I0)
            bound=C*eps**2/mp.sqrt(85)
            ch.add('normalized_bump_bound_'+angle,val<=bound,base.SHOW(val/bound),'<=1')
            probes.append(dict(epsilon=base.SHOW(eps),image_norm=base.SHOW(val),explicit_bound=base.SHOW(bound)))
        ch.add('strict_bound_shrinks_with_support',mp.mpf(probes[1]['explicit_bound'])<mp.mpf(probes[0]['explicit_bound']))
        # Check the guard at an actual node, never call the divided inverse there.
        rat=sy.Rational(eta)
        q=np.zeros((1,15));q[0,[0,3,5]]=1;q[0,9]=q[0,11]=float(mp.sqrt(mp.mpf(rat.p)/rat.q))
        rejected=False
        try:partial_blocks(q,np.eye(3)[None,:,:],np.zeros((1,15,3)),np.zeros((1,3,3)),
                           np.zeros((1,15)),{n:float(v) for n,v in par.items()},np.zeros(1),0)
        except ValueError as exc:rejected='nonpositive force clock' in str(exc)
        ch.add('zero_clock_rejected_without_g_inverse',rejected)
        extra=dict(inverse_bound_coefficient=base.SHOW(C/mp.sqrt(85)),bump_probes=probes)
    except Exception:
        ch.add('unexpected_case_exception',False,traceback.format_exc());extra={}
    return index,dict(family=family,eta=eta,controls=records,**extra,
        meaning='Original-density node/regular controls and explicit norm obstruction, not an adopted background or computed spectrum.'),ch.rows
def calculate(workers):
    pins,before=sources();ch=base.Checks();form=exact(ch)
    if not all(r['passed'] for r in ch.rows):raise ValueError('exact descriptor failure '+repr([r for r in ch.rows if not r['passed']]))
    points=reg.READ(reg.JOINT+'independent.json')
    tasks=[(i,a['family'],a['eta'],a) for i,a in enumerate(points)]
    if len(tasks)!=9:raise ValueError('case count')
    out={};progress('nodal_descriptor_cases',cases=9,workers=min(workers,9))
    if workers==1:
        for t in tasks:
            r=case_job(t);out[r[0]]=r;progress('descriptor_case_complete',index=r[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,9),mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(case_job,t):t[0] for t in tasks}
            for f in as_completed(jobs):
                r=f.result()
                if r[0]!=jobs[f] or r[0] in out:raise ValueError('case identity')
                out[r[0]]=r;progress('descriptor_case_complete',index=r[0])
    records=[]
    for i in range(9):
        _,record,rows=out[i];records.append(record)
        planar.parent.joint.merge_checks(ch,rows,record['family']+'_'+record['eta']+'_')
    _,after=sources();ch.add('original_source_sidecar_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_UNDIVIDED_DESCRIPTOR_ONLY' if passed==len(ch.rows) else 'FAIL_OR_UNRESOLVED_DESCRIPTOR',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='UNDIVIDED_NODAL_ACTION_SUPPLIED_UNWEIGHTED_UNIFORM_INVERSE_REJECTED_PHYSICAL_DOMAIN_OPEN',
        uniform_unweighted_inverse=False,physical_mode_spectrum_computed=False,physical_frequency_window_established=False,
        full_initial_admission=False,state_adopted_or_evolved=False,action_no_go=False,stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    return {'summary.json':summary,'formulas.json':form,'independent.json':records}
def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--replay')
    p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose output or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside scientific output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    meta=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:meta(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(v4.selected_workers(a.workers));payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+chr(10)).encode()
    if a.replay:
        if set(before)!=set(payload):raise ValueError('replay set changed')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or meta(f)!=before[name]:raise ValueError('replay bytes/metadata drift '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f:f.write(raw)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1
if __name__=='__main__':raise SystemExit(main())
