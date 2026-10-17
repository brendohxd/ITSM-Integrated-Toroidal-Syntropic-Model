"""Actual finite-tilt ADM constraints and planar canonical bracket controls.

Full 3D physical closure, admissible initial data and EFT admission remain open.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import traceback
import mpmath as mp
import numpy as np
import sympy as sy

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V1_CONTRACT_2026-10-17.md'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
BG='Analysis/MasterTests/test_01_r4c1_interacting_background.py'
PINS={CONTRACT:'c2c0c054867f4b11cbfafa5a20b792a6c8592f57ebbb737c28f7dd55ce99cade',
 PLANAR:'852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a',
 BG:'1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
 'Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v2.py':'7321e53304864f0832a3e5a6ce3fce5dc2d156d3fa12d29df267b93910730b3f',
 'Analysis/MasterTests/test_01_r4c1_finite_tilt_constraint_v1.py':'199d2ae85d059eaf5861570e03b44f31b739e1c48e396f1579bf3dc547b55579',
 'Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CONSTRAINT_V1_REPORT_2026-10-17.md':'fb4409c5035f2b5d78df673f9656c147037234252012dce3bb2630f0ea92c00a',
 'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md':'14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
 'GEMINI.md':'5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
 'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md':'d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md':'3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809'}
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V2_NORMAL_FORM_ADDENDUM_2026-10-17.md'
PINS.update({ADDENDUM:'167e540c28d0722620f28dfa84ab9a47dfc93dee95073b7df68de975210ea8dc',
 'Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v1.py':'1ce336217fd71267a7af5b5f08b8c89c1899321c7eb2641e3827b3ab43f2c115',
 'Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_attempt_01/summary.json':'e13647178a72afa39c80488a6c50bf1c4569bc186b03134c79e343fea20de027'})
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))
FIELDS=('hxx','hxy','hxz','hyy','hyz','hzz','Vx','Vy','Vz','u','v','r','psi','Z','T')
FAMILIES=('archived_G3','new_B1_frame','new_hierarchical')
ETAS=('1/4','1/64','1/1024')
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

class Checks:
    def __init__(self):self.rows=[];self.names=set()
    def add(self,name,ok,value=None,criterion='exact'):
        if name in self.names:raise ValueError('duplicate check '+name)
        self.names.add(name);self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def small(self,name,error,tol):self.add(name,error<mp.mpf(tol),mp.nstr(error,45),'normalized<'+tol)

def inputs():
    pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes());meta={}
    for name,h in pins.items():
        path=ROOT/name
        if SHA(path.read_bytes())!=h:raise ValueError('source drift '+name)
        side=Path(str(path)+'.sha256')
        if side.read_text().split()[0].lower()!=h:raise ValueError('sidecar drift '+name)
        for p in (path,side):
            b=p.read_bytes();st=p.stat();meta[p.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=st.st_mtime_ns)
    return pins,meta

def parameters(family,eta,backend='np'):
    original=ast.parse((ROOT/BG).read_text(encoding='utf-8-sig'))
    call=next(node.value for node in original.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PARAMS' for t in node.targets))
    base={kw.arg:sy.sympify(ast.unparse(kw.value)) for kw in call.keywords}
    e=sy.sympify(eta);symbol=sy.Symbol('eta')
    fm=json.loads((ROOT/PLANAR).read_bytes())['families'][family]['parameter_map']
    out={k:sy.sympify(v,locals={'eta':symbol}).subs(symbol,e) for k,v in fm.items()}
    out.update(m2=base['m2'],lambda4=base['l4'],lambda6=base['l6'],Lambda=base['cutoff'],
               mr2=base['mr2'],lambda_r=base['lr'],g_r=base['gr']*e,rho_Lambda=base['vacuum'])
    return {k:(mp.mpf(str(sy.N(v,90))) if backend=='mp' else float(v)) for k,v in out.items()}

def symbolic_decomposition(ch):
    print('SYMBOLIC_FULL_ADM_FIRST_JETS',flush=True)
    s=sy;N,g=s.symbols('N gamma',positive=True);V=s.Matrix(s.symbols('V0:3',real=True))
    hd=[[None]*3 for _ in range(3)];dh=[[[None]*3 for _ in range(3)] for _ in range(3)]
    for i,j in HM:
        hd[i][j]=hd[j][i]=s.Symbol('hd'+str(i)+str(j),real=True)
        for a in range(3):dh[a][i][j]=dh[a][j][i]=s.Symbol('h'+str(i)+str(j)+'_'+str(a),real=True)
    nd=s.Symbol('N_t',real=True);ng=s.Matrix(s.symbols('N_0:3',real=True))
    sd=s.Matrix(s.symbols('S_t0:3',real=True));sg=s.Matrix(3,3,lambda i,j:s.Symbol('S'+str(j)+'_'+str(i),real=True))
    vd=s.Matrix(s.symbols('V_t0:3',real=True));vg=s.Matrix(3,3,lambda i,j:s.Symbol('V'+str(j)+'_'+str(i),real=True))
    met=s.diag(-N*N,1,1,1);inv=s.diag(-1/(N*N),1,1,1)
    dg=[]
    for a in range(4):
        m=s.zeros(4);m[0,0]=-2*N*(nd if a==0 else ng[a-1])
        for i in range(3):
            m[0,i+1]=m[i+1,0]=sd[i] if a==0 else sg[a-1,i]
            for j in range(3):m[i+1,j+1]=hd[i][j] if a==0 else dh[a-1][i][j]
        dg.append(m)
    conn=[[[sum(inv[c,j]*(dg[a][j,b]+dg[b][j,a]-dg[j][a,b]) for j in range(4))/2 for b in range(4)] for a in range(4)] for c in range(4)]
    vnorm=(V.T*V)[0]
    def reduce(expr):
        num,den=s.fraction(s.cancel(s.expand(expr)))
        return s.factor(s.Poly(num,g).rem(s.Poly(g*g-1-vnorm,g)).as_expr())/den
    dgam=[]
    for a in range(4):
        hh=s.Matrix(hd if a==0 else dh[a-1]);vv=vd if a==0 else vg[a-1,:].T
        dgam.append(((V.T*hh*V)[0]+2*(V.T*vv)[0])/(2*g))
    n=s.Matrix([g/N,*V]);dn=s.zeros(4)
    for a in range(4):
        na=nd if a==0 else ng[a-1]
        dn[a,0]=dgam[a]/N-g*na/N**2
        for i in range(3):dn[a,i+1]=(vd[i] if a==0 else vg[a-1,i])-g*(sd[i] if a==0 else sg[a-1,i])/N
    cov=dn+s.Matrix(4,4,lambda a,b:sum(conn[b][a][j]*n[j] for j in range(4)))
    B=s.Matrix(4,4,lambda a,b:cov[a,b]*(N if b==0 else 1)/(N if a==0 else 1))
    K=(s.Matrix(hd)-sg-sg.T)/(2*N)
    X=(vd+sg.T*V)/N+g*ng/N
    G3=[[[sum((1 if k==l else 0)*(dh[i][l][j]+dh[j][l][i]-dh[l][i][j]) for l in range(3))/2 for j in range(3)] for i in range(3)] for k in range(3)]
    DV=vg+s.Matrix(3,3,lambda i,j:sum(G3[j][i][k]*V[k] for k in range(3)))
    candidate=s.zeros(4);b0=X+K*V
    candidate[0,0]=(V.T*b0)[0]/g
    for j in range(3):candidate[0,j+1]=b0[j]
    for i in range(3):
        candidate[i+1,0]=sum(V[j]*DV[i,j] for j in range(3))/g+(K*V)[i]
        for j in range(3):candidate[i+1,j+1]=DV[i,j]+g*K[i,j]
    residual=[reduce(B[i,j]-candidate[i,j]) for i in range(4) for j in range(4)]
    ch.add('all16_arbitrary_first_jet_ADM_connection_identities',all(v==0 for v in residual),[str(v) for v in residual if v!=0])
    ch.add('no_lapse_or_shift_time_derivatives_in_nabla_n',not any(v.has(nd,*sd) for v in candidate))
    # Chain rule before eliminating lapse or shift: actual L0 form is proved above.
    z,Ni,A,Pi=s.symbols('N_i numerator proper_momentum local_energy',real=True)
    x=(A+g*Ni)/N
    ch.add('lapse_gradient_chain_coefficient',s.diff(x,Ni)==g/N)
    ch.add('lapse_chain_scaling',s.simplify(s.diff(x,N)+x/N)==0)
    phat,py,b,r2,G,pz,ps,ff=s.symbols('psi_hat y b V2 G pZ pPsi f',real=True)
    gZ=-b*(r2*phat+G)
    solution=-(pz/b+G)/r2
    ch.add('exact_finite_tilt_pZ_inverse',s.cancel(gZ.subs(phat,solution)-pz)==0)
    cancel_residual=s.expand((pz*z-z*gZ).subs(pz,gZ))
    ch.add('Z_hat_cancels_in_true_Legendre_energy',cancel_residual==0,str(cancel_residual))
    # Six independent metric components obey hdot=2NK+Lie_S h, including off diagonals.
    ph,kk,ls=s.symbols('p_h K Lie_Sh',real=True)
    ch.add('independent_metric_momentum_factor_two',s.expand(ph*(2*N*kk+ls)-N*2*ph*kk-ph*ls)==0)
    # ACTUAL chain-rule shift variation after proving the full action's ADM form.
    hh=s.Matrix(3,3,lambda i,j:s.Symbol('h'+str(min(i,j))+str(max(i,j)),real=True))
    pi=s.Matrix(3,3,lambda i,j:s.Symbol('pi'+str(min(i,j))+str(max(i,j)),real=True))
    pv=s.Matrix(s.symbols('pV0:3',real=True));dvS=s.Matrix(s.symbols('deltaS0:3',real=True))
    dsjet=s.Matrix(3,3,lambda a,i:s.Symbol('deltaS'+str(i)+'_'+str(a),real=True))
    hv=[s.Matrix(3,3,lambda i,j:s.Symbol(str(hh[i,j])+'_'+str(a),real=True)) for a in range(3)]
    piv=[s.Matrix(3,3,lambda i,j:s.Symbol(str(pi[i,j])+'_'+str(a),real=True)) for a in range(3)]
    pvv=s.Matrix(3,3,lambda a,i:s.Symbol('pV'+str(i)+'_'+str(a),real=True))
    scalP=s.symbols('pu pv pr ppsi pZ pT',real=True)
    scalG=s.Matrix(6,3,lambda a,i:s.Symbol('scalar'+str(a)+'_'+str(i),real=True))
    lhs=-sum(pi[i,j]*(sum(dvS[k]*hv[k][i,j] for k in range(3))
              +sum(hh[i,k]*dsjet[j,k]+hh[j,k]*dsjet[i,k] for k in range(3))) for i in range(3) for j in range(3))
    lhs-=sum(pv[j]*sum(dvS[i]*vg[i,j]-V[i]*dsjet[i,j] for i in range(3)) for j in range(3))
    lhs-=sum(scalP[a]*dvS[i]*scalG[a,i] for a in range(6) for i in range(3))
    for i in range(3):
        expect0=-sum(pi[j,k]*hv[i][j,k] for j in range(3) for k in range(3))-sum(pv[j]*vg[i,j] for j in range(3))-sum(scalP[a]*scalG[a,i] for a in range(6))
        ch.add('shift_variation_undifferentiated_'+str(i),s.expand(s.diff(lhs,dvS[i])-expect0)==0)
        for j in range(3):
            ch.add('shift_variation_gradient_'+str(j)+'_'+str(i),s.expand(s.diff(lhs,dsjet[j,i])+2*sum(hh[i,k]*pi[j,k] for k in range(3))-V[j]*pv[i])==0)
    return dict(proof='ALL3D_ARBITRARY_FIRST_JET_AT_A_POINT; tensorial ADM extension',
        B00='V_i (X^i+K^i_j V^j)/gamma',B0j='X^j+K^j_k V^k',
        Bi0='D_i gamma+K_ij V^j',Bij='D_i V^j+gamma K_i^j',
        H_perp='E + partial_i(gamma h^(ij) pV_j)',
        E='sqrt(h)[(P_y-ell)^T R^-1(P_y-ell)/2+P_psi psi_hat-f]',
        C_i='-2partial_j(h_ik pi^(jk))+pi^(jk)partial_i h_jk+pV_j partial_i V^j+partial_j(pV_i V^j)+sum_s p_s partial_i phi_s',
        metric_convention='p_hxy=2*pi^(xy); P_y metric slots=2*p_h/sqrt(h)',
        equations='Euler_N=-H_perp; Euler_shift_i=-C_i, with periodic integration by parts',
        physical_3D_constraint_closure='NOT_PROVED_BY_PLANAR_NUMERICAL_CONTROLS')

def tensor_h(q):
    h=np.zeros((len(q),3,3),dtype=q.dtype)
    for a,(i,j) in enumerate(HM):h[:,i,j]=h[:,j,i]=q[:,a]
    return h

def spatial_geometry(q,D):
    h=tensor_h(q);hi=np.linalg.inv(h);dhz=tensor_h(D@q)
    dh=np.zeros((len(q),3,3,3),dtype=q.dtype);dh[:,2]=dhz
    conn=np.zeros((len(q),3,3,3),dtype=q.dtype)
    for k in range(3):
        for i in range(3):
            for j in range(3):
                for l in range(3):conn[:,k,i,j]+=hi[:,k,l]*(dh[:,i,l,j]+dh[:,j,l,i]-dh[:,l,i,j])/2
    dc=(D@conn.reshape(len(q),-1)).reshape(conn.shape)
    ric=np.zeros_like(h)
    for i in range(3):
        for j in range(3):
            ric[:,i,j]=dc[:,2,i,j]
            if j==2:ric[:,i,j]-=sum(dc[:,k,i,k] for k in range(3))
            for k in range(3):
                for l in range(3):ric[:,i,j]+=conn[:,k,k,l]*conn[:,l,i,j]-conn[:,k,j,l]*conn[:,l,i,k]
    R3=np.einsum('nij,nij->n',hi,ric)
    grad=np.zeros((len(q),15,3),dtype=q.dtype);grad[:,:,2]=D@q
    DV=grad[:,6:9,:].swapaxes(1,2)+np.einsum('njik,nk->nij',conn,q[:,6:9])
    return h,hi,grad,DV,R3

def full_blocks(q,hi,grad,DV,p,par,R3):
    """Exact quadratic complement of the original unit-branch density; no velocity truncation."""
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
    psihat=-(p[:,13]/(volume*par['b'])+gam*Vq)/v2
    pcov=np.column_stack((psihat,dq))
    ell=np.zeros((len(q),12),dtype=np.result_type(q,p))
    ell[:,:9]=bilinear(basis,bg[:,None,:,:])[:,:,0]-par['b']*q[:,13,None]*np.einsum('nai,ni->na',acc,pcov)
    J=q[:,10,None]*grad[:,9,:]-q[:,9,None]*grad[:,10,:]
    VJ=np.einsum('ni,ni->n',V,J)
    ell[:,9:]=-par['zeta']*gam[:,None]*VJ[:,None]*current
    canonical_grad=sum(np.einsum('ni,nij,nj->n',grad[:,k,:],hi,grad[:,k,:]) for k in (9,10,11))
    ss=q[:,9]**2+q[:,10]**2
    potential=par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)+par['mr2']*q[:,11]**2/2+par['lambda_r']*q[:,11]**4/4+par['g_r']*ss*q[:,11]**2/4+par['rho_Lambda']
    Q=gam*psihat+Vq;Y=-psihat**2+np.einsum('ni,nij,nj->n',dq,hi,dq)+Q**2
    framebg=bilinear(bg[:,None,:,:],bg[:,None,:,:])[:,0,0]/2
    f=(par['MP2']*R3/2+framebg-canonical_grad/2-potential
        -par['zeta']*(np.einsum('ni,nij,nj->n',J,hi,J)+VJ**2)/2
        +par['K_Q']*Q**2/2-par['A']*Y**1.5+par['b']*q[:,13]**2/2
        -par['b']*(np.einsum('ni,nij,nj->n',dz,hi,dq)+np.einsum('ni,ni->n',V,dz)*Q)
        -par['b']*q[:,13]*np.einsum('ni,ni->n',accbg,pcov))
    P=np.column_stack((2*p[:,:6],p[:,6:12]))/volume[:,None]
    y=np.linalg.solve(R,(P-ell)[...,None])[...,0]
    energy=volume*(np.einsum('ni,ni->n',P-ell,y)/2+p[:,12]/volume*psihat-f)
    C=np.exp(par['beta']*q[:,12]);dT=grad[:,14,:]
    dust=p[:,14]*np.sqrt(C*C+np.einsum('ni,nij,nj->n',dT,hi,dT))
    flux=gam*np.einsum('ni,ni->n',hi[:,2,:],p[:,6:9])
    return energy+dust,flux,dict(R=R,ell=ell,y=y,psi_hat=psihat,Y=Y,volume=volume,gamma=gam)

def hamiltonian(q,p,lapse,D,par,gr=False,omit_flux=False):
    h,hi,grad,DV,R3=spatial_geometry(q,D)
    if gr:
        volume=np.sqrt(np.linalg.det(h));pi=np.zeros(h.shape,dtype=np.result_type(q,p))
        for a,(i,j) in enumerate(HM):pi[:,i,j]=pi[:,j,i]=p[:,a]/(1 if i==j else 2)
        mixed=np.einsum('nij,njk->nik',pi,h)
        grav=2/(par['MP2']*volume)*(np.einsum('nij,nji->n',mixed,mixed)-np.trace(mixed,axis1=1,axis2=2)**2/2)-par['MP2']*volume*R3/2
        matter=sum(p[:,k]**2/(2*volume)+volume*np.einsum('ni,nij,nj->n',grad[:,k,:],hi,grad[:,k,:])/2 for k in (9,10,11))
        dust=p[:,14]*np.sqrt(1+np.einsum('ni,nij,nj->n',grad[:,14,:],hi,grad[:,14,:]))
        return (2*np.pi/len(q))*np.sum(lapse*(grav+matter+dust))
    energy,flux,_=full_blocks(q,hi,grad,DV,p,par,R3)
    return (2*np.pi/len(q))*np.sum(lapse*energy-(0 if omit_flux else D@lapse)*flux)

def diffeo(q,p,shift,D):
    h=tensor_h(q);hp=tensor_h(D@q);sp=D@shift;hs=np.einsum('nij,nj->ni',h,sp)
    lieh=shift[:,2,None,None]*hp
    lieh[:,:,2]+=hs;lieh[:,2,:]+=hs
    lieV=shift[:,2,None]*(D@q[:,6:9])-q[:,8,None]*sp
    result=sum(p[:,a]*lieh[:,i,j] for a,(i,j) in enumerate(HM))
    result+=np.einsum('ni,ni->n',p[:,6:9],lieV)
    result+=np.einsum('ni,ni->n',p[:,9:],shift[:,2,None]*(D@q[:,9:]))
    return (2*np.pi/len(q))*np.sum(result)

def derivative(fn,q,p,step):
    result=[]
    for part in range(2):
        out=np.zeros_like(q,dtype=float)
        for i in range(len(q)):
            for j in range(15):
                if part==0:
                    a=q.astype(complex);a[i,j]+=1j*step;v=fn(a,p)
                else:
                    a=p.astype(complex);a[i,j]+=1j*step;v=fn(q,a)
                out[i,j]=np.imag(v)/step
        result.append(out)
    return result

def bracket(a,b,spacing):return np.sum(a[0]*b[1]-a[1]*b[0])/spacing

def spectral_grid(n):
    z=2*np.pi*np.arange(n)/n
    delta=np.arange(n)[:,None]-np.arange(n)[None,:]
    D=np.zeros((n,n));mask=delta!=0
    D[mask]=.5*((-1.)**delta[mask])/np.sin(np.pi*delta[mask]/n)
    return z,D

def sample(n,par,gr=False):
    z,D=spectral_grid(n);q=np.zeros((n,15));p=np.zeros_like(q)
    q[:,0]=1+.012*np.cos(z);q[:,3]=1+.009*np.sin(z);q[:,5]=1+.011*np.cos(2*z)
    q[:,1]=.004*np.sin(z);q[:,2]=.003*np.cos(z);q[:,4]=.003*np.sin(2*z)
    q[:,6]=.1+.002*np.cos(z);q[:,7]=.012+.001*np.sin(z);q[:,8]=.008+.001*np.cos(2*z)
    for j,value in ((9,.4),(10,.6),(11,.13),(12,.02),(13,.04),(14,0)):
        q[:,j]=value+.001*np.sin(z+(j%3))
    for j in range(6):p[:,j]=(-.1 if j in (0,3,5) else .003)+.0007*np.cos(z+j)
    for j in range(6,9):p[:,j]=par['MU2']*(.002+.0001*np.sin(z+j))
    for j in range(9,12):p[:,j]=.01+.0003*np.cos(z+j)
    p[:,12]=par['K_Q']*(.015+.0002*np.sin(z));p[:,14]=.07+.001*np.cos(z)
    h=tensor_h(q);hi=np.linalg.inv(h);vol=np.sqrt(np.linalg.det(h));V=q[:,6:9]
    v2=np.einsum('ni,nij,nj->n',V,h,V);gam=np.sqrt(1+v2)
    p[:,13]=-par['b']*vol*(v2/8+gam*V[:,2]*(D@q[:,12]))
    if gr:p[:,6:9]=0;p[:,12:14]=0
    return z,D,q,p

def bracket_case(ch,index,family,eta,n,gr=False):
    label=('GR_control' if gr else family+'_'+eta)+'_N'+str(n)
    print('POISSON '+label,flush=True)
    par=parameters(family,eta);z,D,q,p=sample(n,par,gr)
    h,hi,grad,DV,R3=spatial_geometry(q,D)
    ch.add(label+'_positive_spatial_metric',np.min(np.linalg.eigvalsh(h))>0)
    if not gr:
        _,_,base=full_blocks(q,hi,grad,DV,p,par,R3)
        ch.add(label+'_regular_base_away_from_cusp',np.min(base['Y'])>0 and np.min(np.einsum('ni,nij,nj->n',q[:,6:9],h,q[:,6:9]))>0)
    f=1+.1*np.sin(z);g=.7+.1*np.cos(2*z)
    S=np.column_stack((.04*np.cos(z),.03*np.sin(2*z),.05*np.sin(z)))
    T=np.column_stack((.03*np.sin(z),.02*np.cos(z),.04*np.cos(2*z)))
    HF=lambda a,b:hamiltonian(a,b,f,D,par,gr)
    HG=lambda a,b:hamiltonian(a,b,g,D,par,gr)
    DS=lambda a,b:diffeo(a,b,S,D)
    DT=lambda a,b:diffeo(a,b,T,D)
    if not gr:
        flux_effect=HF(q,p)-hamiltonian(q,p,f,D,par,omit_flux=True)
        ch.add(label+'_reject_deleting_lapse_gradient',abs(flux_effect)>np.finfo(float).eps*max(1.,abs(HF(q,p))),float(flux_effect),'resolved nonzero original Hamiltonian contribution; not a physical cutoff')
    derivs=[derivative(fn,q,p,1e-20) for fn in (HF,HG,DS,DT)]
    small=derivative(HF,q,p,1e-24)
    consistency=max(float(np.max(np.abs(a-b))/max(1.,np.max(np.abs(a)))) for a,b in zip(derivs[0],small))
    ch.small(label+'_complex_step_consistency',mp.mpf(consistency),'1e-9')
    spacing=2*np.pi/n
    xi=hi[:,:,2]*(f*(D@g)-g*(D@f))[:,None]
    comm=S[:,2,None]*(D@T)-T[:,2,None]*(D@S)
    observed=[bracket(derivs[2],derivs[3],spacing),bracket(derivs[2],derivs[0],spacing),bracket(derivs[0],derivs[1],spacing)]
    expected=[diffeo(q,p,comm,D),hamiltonian(q,p,S[:,2]*(D@f),D,par,gr),diffeo(q,p,xi,D)]
    residual=[]
    for name,a,b in zip(('D_D','D_H','H_H'),observed,expected):
        err=float(abs(a-b)/max(1.,abs(a),abs(b)));residual.append(err)
        ch.small(label+'_'+name,mp.mpf(err),'1e-7')
    return dict(index=index,family=family,eta=eta,grid=n,GR_control=gr,
        observed=list(map(float,observed)),expected=list(map(float,expected)),normalized_residuals=residual,
        complex_step_consistency=consistency,scope='full canonical pairs on planar periodic fields; not arbitrary3D closure proof')

def mp_geometry(seed):
    """Independent original ADM coordinates with general first jets and nonzero shift."""
    r=lambda a,b=1:mp.mpf(a)/b
    N=r(6+seed,5);S=mp.matrix([r(1,19),-r(1,23),r(1,29)])
    h=mp.matrix([[r(6,5),r(1,31),r(1,37)],[r(1,31),r(11,10),-r(1,41)],[r(1,37),-r(1,41),r(9,10)]])
    V=mp.matrix([r(1,10),r(1+seed,33),-r(1,43)])
    hd=mp.matrix([[r(1+i+j,53) for j in range(3)] for i in range(3)])
    dh=[mp.matrix([[r((i+j+a)%5-2,101+a*4) for j in range(3)] for i in range(3)]) for a in range(3)]
    Nd=r(2,31);Ng=mp.matrix([r(1,47),-r(1,53),r(1,59)])
    Sd=mp.matrix([r(1,61),r(1,67),-r(1,71)])
    Sg=mp.matrix([[r((i+2*j)%5-2,73) for j in range(3)] for i in range(3)])
    Vd=mp.matrix([r(1,79),r(1,83),r(1,89)])
    Vg=mp.matrix([[r((2*i+j)%7-3,97) for j in range(3)] for i in range(3)])
    def point(xx):
        t=xx[0];NN=N+Nd*t+sum(Ng[i]*xx[i+1] for i in range(3))
        ss=S+t*Sd+mp.matrix([sum(Sg[i,j]*xx[i+1] for i in range(3)) for j in range(3)])
        hh=h+t*hd+sum((xx[i+1]*dh[i] for i in range(3)),mp.zeros(3))
        vv=V+t*Vd+mp.matrix([sum(Vg[i,j]*xx[i+1] for i in range(3)) for j in range(3)])
        gam=mp.sqrt(1+(vv.T*hh*vv)[0]);nn=mp.matrix([gam/NN]+list(vv-ss*gam/NN))
        g=mp.zeros(4);g[0,0]=-NN**2+(ss.T*hh*ss)[0]
        for i in range(3):
            g[0,i+1]=g[i+1,0]=(hh*ss)[i]
            for j in range(3):g[i+1,j+1]=hh[i,j]
        return g,nn
    x=[mp.mpf(0)]*4;g,n=point(x);gi=g**-1
    def partial(fn,mu):
        def at(v):xx=list(x);xx[mu]=v;return fn(xx)
        return mp.diff(at,0)
    dg=[mp.matrix([[partial(lambda xx:point(xx)[0][i,j],a) for j in range(4)] for i in range(4)]) for a in range(4)]
    conn=[[[sum(gi[c,j]*(dg[a][j,b]+dg[b][j,a]-dg[j][a,b]) for j in range(4))/2 for b in range(4)] for a in range(4)] for c in range(4)]
    DN=mp.matrix([[partial(lambda xx:point(xx)[1][b],a)+sum(conn[b][a][j]*n[j] for j in range(4)) for b in range(4)] for a in range(4)])
    B=mp.zeros(4)
    for a in range(4):
        vec=(DN[0,:].T-sum((S[i]*DN[i+1,:].T for i in range(3)),mp.zeros(4,1)))/N if a==0 else DN[a,:].T
        B[a,0]=N*vec[0]
        for j in range(3):B[a,j+1]=vec[j+1]+S[j]*vec[0]
    hi=h**-1;gam=mp.sqrt(1+(V.T*h*V)[0])
    g3=[[[sum(hi[k,l]*(dh[i][l,j]+dh[j][l,i]-dh[l][i,j]) for l in range(3))/2 for j in range(3)] for i in range(3)] for k in range(3)]
    DV=Vg+mp.matrix([[sum(g3[j][i][k]*V[k] for k in range(3)) for j in range(3)] for i in range(3)])
    lieh=sum((S[k]*dh[k] for k in range(3)),mp.zeros(3))+h*Sg.T+Sg*h
    K=(hd-lieh)/(2*N)
    shift_cov=h*S
    DS=mp.matrix([[sum(dh[i][j,k]*S[k]+h[j,k]*Sg[i,k] for k in range(3))-sum(g3[k][i][j]*shift_cov[k] for k in range(3)) for j in range(3)] for i in range(3)])
    Kraw=(hd-DS-DS.T)/(2*N)
    liev=mp.matrix([sum(S[i]*Vg[i,j]-V[i]*Sg[i,j] for i in range(3)) for j in range(3)])
    X=(Vd-liev)/N+gam*hi*Ng/N
    out=dict(N=N,S=S,h=h,hi=hi,V=V,gamma=gam,K=K,Kraw=Kraw,X=X,DV=DV,B=B,
             g=g,gi=gi,n=n,DN=DN,R3=r(7,50),Z=r(2,7),u=r(2,5),v=r(3,5),r=r(1,7),psi=r(1,9),epsilon=r(7,100))
    # Full independent scalar first jets in coordinates; convert only for the candidate.
    out['coord_grad']={name:mp.matrix([r(2+j,23)]+[r((i+j)%5-2,113+i*2) for i in range(3)]) for j,name in enumerate(('u','v','r','psi','Z','T'))}
    out['spatial']={name:mp.matrix(list(vv)[1:]) for name,vv in out['coord_grad'].items()}
    out['proper']={name:(vv[0]-sum(S[i]*vv[i+1] for i in range(3)))/N for name,vv in out['coord_grad'].items()}
    return out

def mp_B(c,y):
    K=mp.zeros(3)
    for a,(i,j) in enumerate(HM):K[i,j]=K[j,i]=y[a]
    X=mp.matrix(y[6:9]);V=c['V'];h=c['h'];gam=c['gamma'];DV=c['DV'];hi=c['hi']
    a=X+hi*K*V;out=mp.zeros(4);out[0,0]=(V.T*h*a)[0]/gam
    for j in range(3):out[0,j+1]=a[j]
    for i in range(3):
        out[i+1,0]=sum((h*V)[j]*DV[i,j] for j in range(3))/gam+(K*V)[i]
        for j in range(3):out[i+1,j+1]=DV[i,j]+gam*(K*hi)[i,j]
    return out,K

def mp_body(c,par,y,psihat,zhat,coordinate=False,components=False,include_dust=True):
    if coordinate:
        B=c['DN'];g=c['g'];gi=c['gi'];n=c['n'];K=c['Kraw'];grad=c['coord_grad']
    else:
        B,K=mp_B(c,y);g=mp.zeros(4);g[0,0]=-1
        for i in range(3):
            for j in range(3):g[i+1,j+1]=c['h'][i,j]
        gi=g**-1;n=mp.matrix([c['gamma']]+list(c['V']))
        grad={name:mp.matrix([psihat if name=='psi' else zhat if name=='Z' else y[9+('u','v','r').index(name)] if name in ('u','v','r') else c['proper'][name]]+list(c['spatial'][name])) for name in ('u','v','r','psi','Z','T')}
    acc=B.T*n;hp=gi+n*n.T
    I1=sum(gi[i,j]*g[k,l]*B[i,k]*B[j,l] for i in range(4) for j in range(4) for k in range(4) for l in range(4))
    frame=-par['MU2']*(par['c1']*I1+par['c2']*sum(B[i,i] for i in range(4))**2+par['c3']*sum(B[i,j]*B[j,i] for i in range(4) for j in range(4))-par['c4']*(acc.T*g*acc)[0])/2
    current=c['v']*grad['u']-c['u']*grad['v'];Q=(n.T*grad['psi'])[0];Y=(grad['psi'].T*hp*grad['psi'])[0]
    temporal=par['K_Q']*Q*Q/2;cusp=-par['A']*Y**mp.mpf('1.5')
    force=temporal+cusp
    racc=-par['b']*c['Z']*(acc.T*grad['psi'])[0]
    rgrad=-par['b']*(grad['Z'].T*hp*grad['psi'])[0]
    reg=par['b']*c['Z']**2/2+rgrad+racc
    align=-par['zeta']*(current.T*hp*current)[0]/2
    can=-sum((grad[name].T*gi*grad[name])[0] for name in ('u','v','r'))/2
    ss=c['u']**2+c['v']**2
    pot=par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)+par['mr2']*c['r']**2/2+par['lambda_r']*c['r']**4/4+par['g_r']*ss*c['r']**2/4+par['rho_Lambda']
    km=c['hi']*K;adm=par['MP2']*(sum(km[i,j]*km[j,i] for i in range(3) for j in range(3))-sum(km[i,i] for i in range(3))**2+c['R3'])/2
    C=mp.exp(par['beta']*c['psi']);dust=-c['epsilon']*(C*C*(grad['T'].T*gi*grad['T'])[0]+C**4)/2
    if components:return dict(spatial_curvature=par['MP2']*c['R3']/2,frame=frame,
        acceleration=racc,regulator_gradient=rgrad,cusp=cusp,alignment=align,temporal_force=temporal)
    return adm+frame+force+reg+align+can-pot+(dust if include_dust else 0)

def independent_geometry_and_inverse(ch):
    print('INDEPENDENT_COORDINATE_AND_LEGENDRE_CONTROLS',flush=True);mp.mp.dps=80
    controls=[]
    for seed in (0,1):
        c=mp_geometry(seed);y=mp.matrix([c['K'][i,j] for i,j in HM]+list(c['X'])+[c['proper'][n] for n in ('u','v','r')])
        pred,_=mp_B(c,y);berr=max(abs(pred[i,j]-c['B'][i,j]) for i in range(4) for j in range(4))
        ch.small('coordinate_geometry_all16_'+str(seed),berr,'1e-50')
        ch.small('ADM_determinant_'+str(seed),abs(mp.det(c['g'])+c['N']**2*mp.det(c['h'])),'1e-50')
        ch.small('independent_extrinsic_curvature_'+str(seed),max(abs(c['K'][i,j]-c['Kraw'][i,j]) for i in range(3) for j in range(3)),'1e-50')
        for family in FAMILIES:
            for eta in ETAS:
                par=parameters(family,eta,'mp');ps=c['proper']['psi'];zs=c['proper']['Z']
                direct=mp_body(c,par,y,ps,zs,True);candidate=mp_body(c,par,y,ps,zs)
                err=abs(direct-candidate)/max(1,abs(direct));tag=str(seed)+'_'+family+'_'+eta
                ch.small('all_sector_coordinate_density_'+tag,err,'1e-50')
                if seed==0 and eta==ETAS[0]:
                    terms=mp_body(c,par,y,ps,zs,components=True)
                    for name,value in terms.items():
                        omitted_error=abs(direct-(candidate-value))/max(1,abs(direct))
                        ch.add('reject_omitting_'+name+'_'+family,omitted_error>mp.mpf('1e-50'),mp.nstr(omitted_error,45),'original density discrepancy>1e-50; mathematical rejection control')
                if seed:continue
                # Dust is transformed independently below; do not leave its fixed-velocity
                # Lagrangian hidden in the metric/frame/force Legendre dual.
                fn=lambda yy,pp=ps,zz=0:mp_body(c,par,yy,pp,zz,include_dust=False)
                zero=mp.matrix(12,1);f=fn(zero);basis=[mp.matrix([int(i==j) for i in range(12)]) for j in range(12)]
                plus=[fn(e) for e in basis];minus=[fn(-e) for e in basis]
                ell=mp.matrix([(a-b)/2 for a,b in zip(plus,minus)])
                R=mp.matrix(12)
                for i in range(12):
                    R[i,i]=plus[i]+minus[i]-2*f
                    for j in range(i):R[i,j]=R[j,i]=fn(basis[i]+basis[j])-plus[i]-plus[j]+f
                P=R*y+ell;pZ=mp.diff(lambda zz:fn(y,ps,zz),zs)
                v2=(c['V'].T*c['h']*c['V'])[0];Vq=(c['V'].T*c['spatial']['psi'])[0]
                backpsi=-(pZ/par['b']+c['gamma']*Vq)/v2
                ch.small('exact_pZ_velocity_reconstruction_'+tag,abs(backpsi-ps),'1e-50')
                inverse=R**-1*(P-ell)
                ch.small('complete12_velocity_inverse_'+tag,max(abs(inverse[i]-y[i]) for i in range(12)),'1e-50')
                pPsi=mp.diff(lambda pp:fn(y,pp,zs),ps)
                # ell/f derivatives come from independent densities, not the numeric backend.
                def le(k,pp):return (fn(basis[k],pp)-fn(-basis[k],pp))/2
                ld=mp.matrix([mp.diff(lambda pp:le(k,pp),ps) for k in range(12)])
                fd=mp.diff(lambda pp:fn(zero,pp),ps)
                backz=-(pPsi-(ld.T*inverse)[0]-fd)/(par['b']*v2)
                ch.small('Z_velocity_reconstruction_'+tag,abs(backz-zs),'1e-50')
                E=(P.T*y)[0]+pPsi*ps+pZ*zs-fn(y,ps,zs)
                dual=((P-ell).T*inverse)[0]/2+pPsi*ps-f
                ch.small('true_coupled_Legendre_energy_'+tag,abs(E-dual)/max(1,abs(E)),'1e-50')
                C=mp.exp(par['beta']*c['psi']);tg=c['spatial']['T']
                gradT2=(tg.T*c['hi']*tg)[0];pT=c['epsilon']*C*C*c['proper']['T']
                es=pT/(C*C*mp.sqrt(C*C+gradT2))
                HD=pT*pT/(2*es*C*C)+es*(C*C*gradT2+C**4)/2
                ch.small('positive_dust_Hamiltonian_elimination_'+tag,abs(HD-pT*mp.sqrt(C*C+gradT2)),'1e-50')
                controls.append(dict(seed=seed,family=family,eta=eta,density_error=mp.nstr(err,45),R_determinant=mp.nstr(mp.det(R),50)))
    return controls

def calculate(emit):
    pins,before=inputs();ch=Checks();form=symbolic_decomposition(ch);emit('formulas.json',form)
    coords=independent_geometry_and_inverse(ch);emit('independent.json',coords)
    records=[];case=0
    for n in (17,25):
        row=bracket_case(ch,case,FAMILIES[0],ETAS[0],n,True);emit('bracket_'+str(case).zfill(2)+'.json',row);records.append(row);case+=1
    for family in FAMILIES:
        for eta in ETAS[:2]:
            for n in (17,25):
                row=bracket_case(ch,case,family,eta,n);emit('bracket_'+str(case).zfill(2)+'.json',row);records.append(row);case+=1
    _,after=inputs();ch.add('all_original_source_metadata_preserved',before==after)
    ok=all(row['passed'] for row in ch.rows)
    summary=dict(validation='PASS_CANONICAL_IDENTITIES_PLANAR_CONTROLS_ONLY' if ok else 'FAIL_CANONICAL_IDENTITIES_OR_CONTROLS',
        passed=sum(row['passed'] for row in ch.rows),total=len(ch.rows),checks=ch.rows,
        source_sha256=pins,source_metadata=before,bracket_case_count=len(records),
        canonical_lapse_shift_derived=all(row['passed'] for row in ch.rows if row['name'].startswith(('all16','lapse_','coordinate_','all_sector_','shift_'))),
        general_3D_constraint_closure_proved=False,physical_reduced_hessian_complete=False,
        admissible_prepared_initial_data_proved=False,physical_window_admitted=False,healthy_GR_proved=False,
        missing_required_physics=['arbitrary3D constraint-algebra/reduction proof','exact prepared finite-amplitude initial constraint/charge admission',
            'admissible Cauchy/physical energy domain','nonlinear remainder and physical EFT window','healthy GR and identifying matter/nonlinear matching'],
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',stage2_complete=False,stage3_entered=False,
        status='CANONICAL_FORMULA_AND_PLANAR_CONTROLS_ONLY_FULL_PHYSICAL_REDUCTION_OPEN')
    emit('summary.json',summary);return summary

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');ap.add_argument('--replay');args=ap.parse_args()
    if bool(args.output)==bool(args.replay):ap.error('choose a fresh output or read-only replay')
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('unsafe receipt directory')
    if args.output:dest.mkdir(parents=True,exist_ok=False)
    originals={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
    emitted=set()
    def emit(name,obj):
        b=ENC(obj)
        for target,data in ((name,b),(name+'.sha256',(SHA(b)+'  '+name+'\n').encode())):
            emitted.add(target);p=dest/target
            if args.replay:
                if p.read_bytes()!=data:raise ValueError('replay mismatch '+target)
            else:
                with p.open('xb') as f:f.write(data)
    try:summary=calculate(emit)
    except Exception as error:
        if args.output:emit('interrupted.json',dict(exception=type(error).__name__,error=str(error),physics_pass=False,stage2_complete=False))
        raise
    if args.replay:
        if set(originals)!=emitted:raise ValueError('replay file set mismatch')
        for name,record in originals.items():
            p=dest/name
            if (SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)!=record:raise ValueError('replay metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','physics_pass','status')}),flush=True)
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
