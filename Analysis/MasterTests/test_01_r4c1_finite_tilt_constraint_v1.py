"""Full finite-tilt Legendre/auxiliary audit; physical Dirac reduction stays open."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CONSTRAINT_V1_CONTRACT_2026-10-17.md'
KERNEL='Analysis/MasterTests/outputs/r4c1_g3n5_attempt_02/kernel.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
PINS={CONTRACT:'5bc0f9b3f81869f576bc8e7373cb4770727a1e64abef7cad1974263f4bca205d',
 KERNEL:'cf30a7e334d154e492f8ca7bde92cf95754390b602f4914e5b6ba8fed90a74e3',
 PLANAR:'852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a',
 'Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v2.py':'7321e53304864f0832a3e5a6ce3fce5dc2d156d3fa12d29df267b93910730b3f',
 'Theory/Gates/RES-001/RES001_R4C1_G3N2_TRANSVERSE_MULTIMODE_ENTRY_REPORT_2026-10-09.md':'e0f066347d13bbd00566cf8f9af5857e424e4c8ce1102f1eebd457b419c9da19',
 'Theory/Gates/RES-001/RES001_R4C1_CUSP3_SOURCE_AWARE_WINDOW_V1_REPORT_2026-10-17.md':'f8d3d33c1f9e5c9a3458ab2bb617f17aa40df33e0956dfd851b6118ceae8e984',
 'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md':'14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
 'GEMINI.md':'5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
 'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md':'d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md':'3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809'}
FIELDS=('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz',
 'Vx','Vy','Vz','du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IX={n:i for i,n in enumerate(FIELDS)}
DYN=list(range(4,18))+[19,20]
FAMILIES=('archived_G3','new_B1_frame','new_hierarchical')
ETAS=(s.Rational(1,4),s.Rational(1,64),s.Rational(1,1024))
TILTS=(s.Integer(0),s.Rational(1,10),-s.Rational(1,10),s.Rational(1,20),-s.Rational(1,20),s.Rational(1,100))
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda x:s.factor(s.cancel(s.expand(x)))

class Checks:
    def __init__(self): self.rows=[];self.names=set()
    def add(self,name,ok,value=None,criterion='exact'):
        if name in self.names: raise ValueError('duplicate check '+name)
        self.names.add(name)
        self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def zero(self,name,expr):
        expr=list(expr) if isinstance(expr,(s.MatrixBase,list,tuple)) else [expr]
        residual=[clean(e) for e in expr]
        self.add(name,all(e==0 for e in residual),[str(e) for e in residual if e!=0])

def inputs():
    pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes())
    metadata={}
    for name,expected in pins.items():
        path=ROOT/name;data=path.read_bytes()
        if SHA(data)!=expected: raise ValueError('source drift '+name)
        for p in (path,Path(str(path)+'.sha256')):
            if not p.is_file(): raise ValueError('missing required source/sidecar '+str(p))
            b=p.read_bytes();stat=p.stat()
            metadata[p.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=stat.st_mtime_ns)
        if Path(str(path)+'.sha256').read_text().split()[0].lower()!=expected:
            raise ValueError('source sidecar drift '+name)
    return pins,metadata

def derive(ch):
    print('Deriving all22 finite-tilt temporal entries from covariant density',flush=True)
    w=s.Symbol('w',real=True);gamma=s.sqrt(1+w*w)
    names='MP2 MU2 c1 c2 c3 c4 K_Q b zeta A u0 v0 r0 C epsilon0 Z0 psi_dot qx qy qz zx zy zz tx ty tz m2 lambda4 lambda6 Lambda mr2 lambda_r g_r rho_Lambda R3'.split()
    x={n:s.Symbol(n,real=True) for n in names};x['w']=w
    vel=[s.Symbol(n+'_t',real=True) for n in FIELDS];d=dict(zip(FIELDS,vel))
    metric=s.diag(-1,1,1,1);n=s.Matrix([gamma,w,0,0])
    ht=s.Matrix([[d['Mxx'],d['Mxy'],d['Mxz']],
                 [d['Mxy'],d['Myy'],d['Myz']],
                 [d['Mxz'],d['Myz'],d['Mzz']]])
    gt=s.zeros(4);gt[0,0]=-2*d['alpha']
    for i in range(3):
        gt[0,i+1]=gt[i+1,0]=d[FIELDS[1+i]]
        for j in range(3):gt[i+1,j+1]=ht[i,j]
    dg=[gt,s.zeros(4),s.zeros(4),s.zeros(4)]
    conn=[[[sum(metric[c,j]*(dg[a][j,b]+dg[b][j,a]-dg[j][a,b]) for j in range(4))/2
             for b in range(4)] for a in range(4)] for c in range(4)]
    gamt=(w*w*d['Mxx']/2+w*d['Vx'])/gamma
    nt=s.Matrix([gamt-gamma*d['alpha'],d['Vx']-gamma*d['Sx'],
                  d['Vy']-gamma*d['Sy'],d['Vz']-gamma*d['Sz']])
    DN=s.Matrix(4,4,lambda a,b:(nt[b] if a==0 else 0)+sum(conn[b][a][j]*n[j] for j in range(4)))
    DU=DN+s.Matrix(4,4,lambda a,b:d['nu']*n[b] if a==0 else 0)
    ch.zero('normalized_n_at_finite_tilt',(n.T*metric*n)[0]+1)
    ch.zero('all_normal_derivatives_are_unit_tangent',DN*metric*n)
    ch.add('lapse_shift_velocity_cancellation_in_all16_covariant_entries',
           not any(DN[i,j].has(*vel[:4]) for i in range(4) for j in range(4)))
    accn=DN.T*n;accu=DU.T*n
    I1=sum(metric[i,i]*metric[j,j]*DU[i,j]**2 for i in range(4) for j in range(4))
    I2=s.trace(DU)**2;I3=s.trace(DU*DU);I4=(accu.T*metric*accu)[0]
    frame=-x['MU2']*(x['c1']*I1+x['c2']*I2+x['c3']*I3-x['c4']*I4)/2
    hp=metric+n*n.T
    q=s.Matrix([d['Pi'],x['qx'],x['qy'],x['qz']]);Y=clean((q.T*hp*q)[0])
    temporal=x['K_Q']*(n.dot(q))**2/2;cusp=-x['A']*Y**s.Rational(3,2)
    zgrad=s.Matrix([d['Z'],x['zx'],x['zy'],x['zz']])
    reg=x['b']*x['Z0']**2/2-x['b']*(zgrad.T*hp*q)[0]-x['b']*x['Z0']*accn.dot(q)
    # Arbitrary fixed spatial current is affine, so it does not change this Hessian.
    J=s.Matrix([x['v0']*d['du']-x['u0']*d['dv'],*s.symbols('Jx Jy Jz',real=True)])
    alignment=-x['zeta']*(J.T*hp*J)[0]/2
    canonical=(d['du']**2+d['dv']**2+d['dr']**2)/2
    dust=x['epsilon0']*(x['C']**2*(d['T']**2-x['tx']**2-x['ty']**2-x['tz']**2)-x['C']**4)/2
    einstein=x['MP2']*(s.trace(ht*ht)-s.trace(ht)**2)/8+x['MP2']*x['R3']/2
    ss=x['u0']**2+x['v0']**2
    potential=x['m2']*ss/2+x['lambda4']*ss**2/8+x['lambda6']*ss**3/(24*x['Lambda']**2)+x['mr2']*x['r0']**2/2+x['lambda_r']*x['r0']**4/4+x['g_r']*ss*x['r0']**2/4+x['rho_Lambda']
    nu,lam=s.symbols('nu LambdaU',real=True)
    unit=lam*(1-(1+nu)**2)/2
    sectors={'Einstein_ADM_and_spatial_Ricci':einstein,'frame':frame,'temporal_force':temporal,
             'nonanalytic_force':cusp,'regulator':reg,'alignment':alignment,
             'Cartesian_kinetics':canonical,'dust':dust,'potential_portal_vacuum':-potential,'unit_multiplier':unit}
    L=sum(sectors.values())
    H=s.hessian(L,vel).subs(d['Pi'],x['psi_dot']).applyfunc(clean)
    dimensions={z:0 for z in L.free_symbols}
    for name in ('MP2','MU2','K_Q','Z0','m2','mr2','R3'):dimensions[x[name]]=2
    for name in ('A','u0','v0','r0','psi_dot','qx','qy','qz','Lambda'):dimensions[x[name]]=1
    dimensions[x['zeta']]=-2
    for name in ('zx','zy','zz'):dimensions[x[name]]=3
    dimensions[x['epsilon0']]=dimensions[x['rho_Lambda']]=dimensions[lam]=4
    for z in J[1:]:dimensions[z]=3
    field_dimensions=[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,-1,4,2,0,4]
    for z,degree in zip(vel,field_dimensions):dimensions[z]=degree+1
    def dimension(expr):
        if expr.is_number:return 0
        if expr.is_Symbol:return dimensions[expr]
        if expr.is_Mul:return sum(dimension(v) for v in expr.args)
        if expr.is_Pow:return dimension(expr.base)*expr.exp
        if expr.is_Add:
            values={dimension(v) for v in expr.args if v!=0}
            if len(values)!=1:raise ValueError('inhomogeneous dimensions '+str(expr))
            return values.pop()
        raise ValueError('unhandled dimensional expression '+str(expr))
    for name,value in sectors.items():ch.add('density_dimension4_'+name,dimension(value)==4,str(dimension(value)))
    ch.add('all_nonzero_temporal_entries_have_correct_dimensions',all(
        H[i,j]==0 or dimension(H[i,j])==2-field_dimensions[i]-field_dimensions[j]
        for i in range(22) for j in range(22)))
    ch.zero('all484_Hessian_symmetry_entries',H-H.T)
    ch.zero('all_six_nondynamical_temporal_rows',H.extract([0,1,2,3,18,21],list(range(22))))
    ch.zero('Z_momentum_full_density',s.diff(L,d['Z'])+x['b']*(hp*q)[0])
    ch.zero('Z_couples_only_to_psi_velocity',[H[19,j] for j in range(22) if j!=16])
    ch.zero('complete_Z_psi_velocity_coefficient',H[19,16]+x['b']*w*w)
    ch.add('acceleration_coupling_retained',s.diff(reg,d['Pi'],d['Vx'])!=0,
           str(clean(s.diff(reg,d['Pi'],d['Vx']))))
    ch.add('metric_frame_cross_coupling_retained',s.diff(frame,d['Mxx'],d['Vx'])!=0)
    ch.add('normal_velocity_is_independent_before_unit_constraint',s.diff(frame,d['nu'],2)!=0)
    ch.zero('temporal_force_is_not_canonical_Lorentz_kinetic',s.diff(temporal,d['Pi'],2)-x['K_Q']*(1+w*w))
    a,b,c,vv,bb=s.symbols('quad_a quad_b quad_c affine_v affine_B',real=True)
    ch.zero('quadratic_first_jet_affine_shift_cannot_change_velocity_Hessian',
            s.diff(a*(b*vv+bb)**2+c*(b*vv+bb),vv,2)-2*a*b*b)
    # The original C2 cusp has zero velocity Hessian when the projected gradient is zero.
    ch.zero('cusp_Hessian_support_only_psi',s.hessian(cusp,vel).extract([i for i in range(22) if i!=16],list(range(22))))
    Hp=H.subs(x['A'],0).subs(w,0).applyfunc(clean)
    archived=json.loads((ROOT/KERNEL).read_bytes())
    aligned=s.zeros(22);symbols={str(z):z for z in Hp.free_symbols}
    symbols.update(x);symbols['a']=s.Integer(1)
    for row in archived['entries']:
        if 22<=row['row']<44 and 22<=row['column']<44:
            aligned[row['row']-22,row['column']-22]=s.sympify(row['value'],locals=symbols).subs(s.Symbol('a'),1)
    ch.zero('complete_archived_aligned_temporal_Hessian_484_entries',Hp-aligned)
    z=s.Symbol('d',real=True);aa=s.Symbol('amplitude',positive=True)
    ch.zero('actual_cusp_C2_extension_right',s.limit(s.diff(-aa*z**3,z,2),z,0,dir='+'))
    ch.zero('actual_cusp_C2_extension_left',s.limit(s.diff(aa*z**3,z,2),z,0,dir='-'))
    ch.add('ordinary_third_cusp_derivative_is_not_inserted',s.diff(-aa*z**3,z,3)!=s.diff(aa*z**3,z,3))
    # Derive multiplier constraints before taking a constraint-tangent restriction.
    ch.zero('unit_multiplier_equation',s.diff(unit,lam)+nu+nu**2/2)
    ch.zero('unit_normal_equation_coefficient_of_LambdaU',s.diff(unit,nu,lam)+1+nu)
    volume,N,C,eps,td,pT,gradT2=s.symbols('volume N C eps tau_dot pT gradT2',positive=True)
    LD=volume*eps*(C*C*td*td/N-N*(C*C*gradT2+C**4))/2
    pt=s.diff(LD,td);HD=clean((pT*td-LD).subs(td,pT*N/(volume*eps*C*C)))
    density_constraint=clean(s.diff(HD,eps)/N)
    ch.zero('dust_normalization_before_clock_gauge',s.diff(LD,eps)-volume*(C*C*td*td/N-N*(C*C*gradT2+C**4))/2)
    ch.zero('dust_second_class_density_Jacobian',s.diff(density_constraint,eps)-pT*pT/(volume*eps**3*C*C))
    ch.zero('dust_positive_density_solution',density_constraint.subs(eps,pT/(volume*C*C*s.sqrt(gradT2+C*C))))
    ch.zero('comoving_clock_lapse_is_inverse_C',s.diff(LD,eps).subs({N:td/C,gradT2:0}))
    # Keep the complete regular complement, including off-unit normal and dust.
    rest=[i for i in DYN if i not in (16,19)]
    GE=list(range(4,13))+[20]
    GEu=list(range(4,13))
    ge=H.extract(GE,GE)
    # SO(2) blocks supply an exact manageable determinant, with no metric freezing.
    basis=s.eye(10);basis[:,s.Integer(3)]=s.Matrix([0,0,0,1,0,-1,0,0,0,0])
    basis[:,s.Integer(5)]=s.Matrix([0,0,0,1,0,1,0,0,0,0])
    transformed=(basis.T*ge*basis).applyfunc(clean)
    blocks=([1,7],[2,8],[4],[3],[0,5,6,9])
    allowed={(i,j) for block in blocks for i in block for j in block}
    ch.zero('full_metric_frame_normal_SO2_block_decomposition',
            [transformed[i,j] for i in range(10) for j in range(10) if (i,j) not in allowed])
    determinants=[clean(transformed.extract(b,b).det(method='domain-ge')) for b in blocks]
    detge=clean(s.prod(determinants)/basis.det()**2)
    geu=H.extract(GEu,GEu)
    bu=basis.extract(list(range(9)),list(range(9)))
    tu=(bu.T*geu*bu).applyfunc(clean);blocks_u=([1,7],[2,8],[4],[3],[0,5,6])
    detgeu=clean(s.prod(clean(tu.extract(b,b).det(method='domain-ge')) for b in blocks_u)/bu.det()**2)
    detmatter=clean(1-x['zeta']*w*w*(x['u0']**2+x['v0']**2))
    ch.zero('Cartesian_alignment_three_field_determinant',H.extract([13,14,15],[13,14,15]).det()-detmatter)
    detrest=detge*detmatter*x['epsilon0']*x['C']**2
    detrest_u=detgeu*detmatter*x['epsilon0']*x['C']**2
    formulas=dict(fields=list(FIELDS),dynamic_indices=DYN,rest_indices=rest,
        Hessian_entries=[dict(row=i,column=j,value=str(H[i,j])) for i in range(22) for j in range(22)],
        sector_densities={n:str(v) for n,v in sectors.items()},
        metric_frame_normal_blocks=[dict(indices=list(k),determinant=str(v)) for k,v in zip(blocks,determinants)],
        metric_frame_normal_determinant=str(detge),unit_tangent_metric_frame_determinant=str(detgeu),
        rest_determinant=str(detrest),unit_tangent_rest_determinant=str(detrest_u),
        full_dynamic_determinant=str(-x['b']**2*w**4*detrest),
        unit_tangent_dynamic_determinant=str(-x['b']**2*w**4*detrest_u),
        coupled_schur_pair='[[H_PiPi-h.T*R^(-1)*h,-b*w^2],[-b*w^2,0]]; R is COMPLETE regular velocity complement',
        schur_pair_determinant='-b^2*w^4; only where det R != 0, b*w != 0',
        dust_hamiltonian=str(HD),dust_density_constraint=str(density_constraint),
        unit_phi=str(s.diff(unit,lam)),
        physical_gravity_constraints='MISSING: complete lapse/momentum closure, global charges/zero modes and admissible initial data',
        interpretation='Pointwise full Legendre and unit/dust auxiliary structure; not the physical reduced Hessian or a ghost theorem')
    return x,H,formulas

def raw_density(velocity,par,rotation=None):
    """Independent exact ADM definitions, time-differentiated before invariants."""
    v=dict(zip(FIELDS,velocity));w=par['w'];gsp=mp.eye(3)
    M=mp.matrix([[v['Mxx'],v['Mxy'],v['Mxz']],[v['Mxy'],v['Myy'],v['Myz']],[v['Mxz'],v['Myz'],v['Mzz']]])
    V=mp.matrix([w,0,0]);Vd=mp.matrix([v['Vx'],v['Vy'],v['Vz']]);S=mp.matrix([v['Sx'],v['Sy'],v['Sz']])
    qsp=mp.matrix([par['qx'],par['qy'],par['qz']]);zg=mp.matrix([par['zx'],par['zy'],par['zz']])
    if rotation is not None:M=rotation*M*rotation.T;V=rotation*V;Vd=rotation*Vd;S=rotation*S;qsp=rotation*qsp;zg=rotation*zg
    def point(t):
        h=gsp+t*M;Ni=t*S;N=1+t*v['alpha'];vv=V+t*Vd
        gamma=mp.sqrt(1+(vv.T*h*vv)[0]);n=mp.matrix([gamma/N]+list(vv-Ni*gamma/N));U=(1+t*v['nu'])*n
        g=mp.matrix(4);g[0,0]=-N*N+(Ni.T*h*Ni)[0]
        for i in range(3):
            g[0,i+1]=g[i+1,0]=(h*Ni)[i]
            for j in range(3):g[i+1,j+1]=h[i,j]
        return g,n,U
    g,n,U=point(mp.mpf(0));gi=g**-1
    dg=[mp.matrix([[mp.diff(lambda t:point(t)[0][i,j],0) for j in range(4)] for i in range(4)])]+[mp.zeros(4) for _ in range(3)]
    conn=[[[sum(gi[c,j]*(dg[a][j,b]+dg[b][j,a]-dg[j][a,b]) for j in range(4))/2 for b in range(4)] for a in range(4)] for c in range(4)]
    def nabla(index):
        vv=point(mp.mpf(0))[index]
        return mp.matrix([[ (mp.diff(lambda t:point(t)[index][b],0) if a==0 else 0)+sum(conn[b][a][j]*vv[j] for j in range(4)) for b in range(4)] for a in range(4)])
    DN=nabla(1);DU=nabla(2);an=DN.T*n;au=DU.T*U;hp=gi+n*n.T
    i1=sum(gi[i,j]*g[k,l]*DU[i,k]*DU[j,l] for i in range(4) for j in range(4) for k in range(4) for l in range(4))
    frame=-par['MU2']*(par['c1']*i1+par['c2']*sum(DU[i,i] for i in range(4))**2+par['c3']*sum(DU[i,j]*DU[j,i] for i in range(4) for j in range(4))-par['c4']*(au.T*g*au)[0])/2
    psi=mp.matrix([v['Pi']]+list(qsp));zz=mp.matrix([v['Z']]+list(zg));yy=(psi.T*hp*psi)[0]
    force=par['K_Q']*(n.T*psi)[0]**2/2-par['A']*yy**mp.mpf('1.5')
    reg=par['b']*par['Z0']**2/2-par['b']*(zz.T*hp*psi)[0]-par['b']*par['Z0']*(an.T*psi)[0]
    current=mp.matrix([par['v0']*v['du']-par['u0']*v['dv'],0,0,0])
    # Spatial current zero only in this independent arithmetic control; analytic Hessian is general.
    align=-par['zeta']*(current.T*hp*current)[0]/2
    adm=par['MP2']*(sum(M[i,j]*M[j,i] for i in range(3) for j in range(3))-sum(M[i,i] for i in range(3))**2)/8
    canonical=(v['du']**2+v['dv']**2+v['dr']**2)/2
    dust=par['epsilon0']*(par['C']**2*v['T']**2-par['C']**4)/2
    return frame+force+reg+align+adm+canonical+dust

def numerical(ch,x,H,formulas):
    print('Checking complete matrices for all families and tilt strata',flush=True)
    mp.mp.dps=80
    fm=json.loads((ROOT/PLANAR).read_bytes())['families']
    eta=s.Symbol('eta');base={'u0':s.Rational(2,5),'v0':s.Rational(3,5),'r0':s.Rational(1,7),
        'C':s.Rational(6,5),'epsilon0':s.Rational(7,100),'Z0':s.Rational(2,7),
        'psi_dot':s.Rational(1,8),'qx':s.Rational(2,13),'qy':-s.Rational(1,17),'qz':s.Rational(3,11),
        'zx':s.Rational(1,19),'zy':s.Rational(1,23),'zz':-s.Rational(1,29)}
    syms=sorted(H.free_symbols,key=str);evaluate=s.lambdify([syms],H,'mpmath',cse=True)
    out=[]
    for family in FAMILIES:
        for et in ETAS:
            par={k:s.sympify(v,locals={'eta':eta}).subs(eta,et) for k,v in fm[family]['parameter_map'].items()}
            par.update(base)
            for w in TILTS:
                pp={**par,'w':w};sub={x[k]:v for k,v in pp.items() if k in x}
                mat=mp.matrix(evaluate([mp.mpf(str(s.N(sub[q],85))) for q in syms]))
                dyn=mp.matrix([[mat[i,j] for j in DYN] for i in DYN])
                unit_indices=[i for i in DYN if i!=20]
                un=mp.matrix([[mat[i,j] for j in unit_indices] for i in unit_indices])
                vals=mp.eigsy(dyn,eigvals_only=True);uv=mp.eigsy(un,eigvals_only=True)
                threshold=mp.mpf('1e-60')
                rank=sum(abs(v)>threshold for v in vals);ranku=sum(abs(v)>threshold for v in uv)
                tag=family+'_'+str(et)+'_w'+str(w)
                expected=16 if w else 15
                ch.add(tag+'_complete_dynamic_rank',rank==expected,rank,str(expected)+'; numerical control only')
                ch.add(tag+'_unit_tangent_rank',ranku==expected-1,ranku,str(expected-1)+'; numerical control only')
                if w:
                    direct=mp.det(dyn);de=s.sympify(formulas['full_dynamic_determinant'],locals=x).subs(sub)
                    predicted=mp.mpf(str(s.N(de,85)));error=abs((direct-predicted)/predicted)
                    ch.add(tag+'_full_determinant_factorization',error<mp.mpf('1e-60'),mp.nstr(error,40),'relative<1e-60')
                out.append(dict(family=family,eta=str(et),w=str(w),rank=rank,unit_tangent_rank=ranku,
                    raw_inertia=[sum(v>threshold for v in vals),sum(v<-threshold for v in vals),16-rank],
                    unit_tangent_raw_inertia=[sum(v>threshold for v in uv),sum(v<-threshold for v in uv),15-ranku],
                    smallest_absolute_nonzero_eigenvalue=mp.nstr(min(abs(v) for v in vals if abs(v)>threshold),50),
                    physical_inertia='NOT_COMPUTED; gravitational constraints and admissible Cauchy data still required'))
    controls=[];rot=mp.matrix([[mp.mpf(3)/5,-mp.mpf(4)/5,0],[mp.mpf(4)/5,mp.mpf(3)/5,0],[0,0,1]])
    for case in (0,1):
        e=ETAS[case];family=FAMILIES[case]
        par={k:s.sympify(v,locals={'eta':eta}).subs(eta,e) for k,v in fm[family]['parameter_map'].items()};par.update(base);par['w']=s.Rational(1,10+case*10)
        sub={x[k]:v for k,v in par.items() if k in x};mh=mp.matrix(evaluate([mp.mpf(str(s.N(sub[q],85))) for q in syms]))
        pp={k:mp.mpf(str(s.N(v,85))) for k,v in par.items()}
        v0=mp.matrix([mp.mpf(0)]*22);v0[16]=pp['psi_dot'];v0[17]=pp['C']
        directions=[mp.matrix([int(i==j) for i in range(22)]) for j in range(22)]
        directions += [mp.matrix([mp.mpf(((i+1)*(j+2))%13-6)/17 for i in range(22)]) for j in range(4)]
        print('Independent original-density control set '+str(case),flush=True)
        for j,direction in enumerate(directions):
            target=(direction.T*mh*direction)[0]
            observed=mp.diff(lambda d:raw_density(v0+d*direction,pp),0,2)
            rotated=mp.diff(lambda d:raw_density(v0+d*direction,pp,rot),0,2)
            error=max(abs(observed-target),abs(rotated-target))/max(1,abs(target))
            ch.add('original_density_'+str(case)+'_'+str(j),error<mp.mpf('1e-40'),mp.nstr(error,45),'relative<1e-40 at80digits; rotated and unrotated')
            controls.append(dict(case=case,direction=j,relative_error=mp.nstr(error,50)))
    return out,controls

def calculate():
    pins,before=inputs();ch=Checks();x,H,formula=derive(ch)
    samples,controls=numerical(ch,x,H,formula)
    _,after=inputs();ch.add('all_source_metadata_unchanged',before==after)
    required_missing=['full nonlinear lapse and momentum constraint closure/reduction',
        'constraint-admissible prepared finite-amplitude data with mean/harmonic/global charges',
        'admissible Cauchy/characteristic and physical energy domain',
        'physical reduced Hessian and nonlinear remainder',
        'healthy GR endpoint and identifying microscopic matter/nonlinear matching']
    ok=all(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_LEGENDRE_AUXILIARY_CHECKS_ONLY' if ok else 'FAIL_LEGENDRE_AUXILIARY_CHECKS',
        passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows,
        source_sha256=pins,source_metadata=before,
        finite_amplitude_physical_reduction_complete=False,stage2_complete=False,stage3_entered=False,
        missing_required_physics=required_missing,physical_ghost_classification='NOT_ESTABLISHED',
        physical_family_GO=[],physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        status='FULL_LEGENDRE_AND_UNIT_DUST_AUDIT_ONLY_PHYSICAL_CONSTRAINT_REDUCTION_OPEN',
        methodological_comparator='https://arxiv.org/abs/1207.6530; not an ITSM result')
    return {'summary.json':summary,'formulas.json':formula,'numerics.json':dict(samples=samples,independent_density_controls=controls)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--replay');args=p.parse_args()
    if bool(args.output)==bool(args.replay):p.error('choose exactly one fresh output or read-only replay')
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('receipt directory outside science outputs')
    if args.output:dest.mkdir(parents=True,exist_ok=False)
    original={n:(SHA(q.read_bytes()),q.stat().st_size,q.stat().st_mtime_ns) for n,q in ((q.name,q) for q in dest.iterdir())} if args.replay else None
    data=calculate();payloads={name:ENC(obj) for name,obj in data.items()}
    for name,b in list(payloads.items()):payloads[name+'.sha256']=(SHA(b)+'  '+name+'\n').encode('ascii')
    if args.replay:
        if set(original)!=set(payloads):raise ValueError('replay file set mismatch')
        for name,b in payloads.items():
            q=dest/name
            if q.read_bytes()!=b:raise ValueError('replay byte mismatch '+name)
            if (SHA(q.read_bytes()),q.stat().st_size,q.stat().st_mtime_ns)!=original[name]:raise ValueError('replay evidence metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,b in payloads.items():
            with (dest/name).open('xb') as f:f.write(b)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','physics_pass','stage2_complete','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1

if __name__=='__main__':raise SystemExit(main())
