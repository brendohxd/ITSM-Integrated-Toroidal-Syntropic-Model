"""Necessary next scalar-node transport; the coupled frame acceleration is open."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = 'Analysis/MasterTests/test_01_r4c1_initial_admission_v1.py'
PARENT_SHA = 'd994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_NODE_VELOCITY_TRANSPORT_V1_CONTRACT_2026-10-18.md'
COUPLED = 'Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01/'
NORMAL = 'Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02/normalization.json'
PROOF = 'Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/proof.json'
OLD_CERT = 'Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/certificates.json'
SHA = lambda raw: hashlib.sha256(raw).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
READ = lambda name: json.loads((ROOT/name).read_bytes())
CLEAN = lambda value: s.factor(s.cancel(s.expand(value)))
SHOW = lambda value: mp.nstr(value, 60)
if SHA((ROOT/PARENT).read_bytes()) != PARENT_SHA:
    raise ValueError('frozen utility source drift before import')
spec = importlib.util.spec_from_file_location('node_transport_frozen_utilities', ROOT/PARENT)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
iv = mp.iv
PINS = dict(base.PINS)
PINS.update({
    PARENT: PARENT_SHA,
    CONTRACT: '6213246535807f2c8486373c0e976a510ee504a3f884617b8c96a49d21772e1f',
    PROOF: 'b96ee17ec3d3f14500d0bf59d786411f5e241cbbb238ef49f3dc34657a18646b',
    OLD_CERT: '7c3465014fd85d7a98b905eed721c907f2f7764ccefadf856680ecf068d7127a',
    NORMAL: '447192694f9d65cd7791cfe93444dfe9a7d2566dfc99f453f590ae00825c668f',
    COUPLED+'summary.json': 'e66ac815aada3fa577db841cc99d55f095115dc203956426a9606fc9ba41ac8e',
    COUPLED+'certificates.json': 'e02cef26c9776f1c4df2b827995ddf2e887038fad886be5f3034bc5133a17cce',
    COUPLED+'independent.json': '3fd32bd7cf07408c0e0a0c62e2ea0348e2f10079d91f59620425feac78eb6eca',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_REPORT_2026-10-18.md': '833dc0f5217a39b5017694d0a3fbd40fa8a4886bb0eb7a2634b1d0d2756b06ab',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_ENDPOINT_ADDENDUM_2026-10-18.md': 'a901a269e762ba0e844f94edcfef103fcd84f50fa3b1e7b03d4bea4691266ff8',
    'Theory/Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V2_REPORT_2026-10-18.md': '7fc348b923e55a8807fe597897fbbd1af20e1d5969260f7f31efa4c2dfc58d87',
})


def sources():
    pins = dict(PINS)
    pins[SELF] = SHA((ROOT/SELF).read_bytes())
    metadata = {}
    for name, digest in pins.items():
        path = ROOT/name
        if SHA(path.read_bytes()) != digest:
            raise ValueError('source hash drift '+name)
        side = Path(str(path)+'.sha256')
        if side.read_text().split()[0].lower() != digest:
            raise ValueError('source sidecar mismatch '+name)
        for item in (path, side):
            raw = item.read_bytes()
            metadata[item.relative_to(ROOT).as_posix()] = dict(
                sha256=SHA(raw), bytes=len(raw), mtime_ns=item.stat().st_mtime_ns)
    return pins, metadata


def derive(ch):
    print('DERIVE_NEXT_NODE_TRANSPORT_WITH_INDEPENDENT_GEOMETRY_JETS', flush=True)
    K,b,beta,H,HB,p,U,Ud,r1,rt,F,aa,jj,rho,rhod,ss,trdd,hyy = s.symbols(
        'K b beta H Hbg p U Ud r1 rt F acceleration jerk rho rho_dot slope_squared trace_hdd hdd_yy', real=True)
    # C = div(hp^{a0}) - acc^0 in E_Z/b = Z + hp^{ab} psi_ab + C psi_t.
    # At N=1, arbitrary planar h and V, C = (V^2)_t/2
    # +V^2*(log(sqrt(h))_t-R_z)-R*(V^2)_z/2+gamma*V^z_z-K_ij V^i V^j.
    ct_over_c = 2*(H-HB)
    ctt_over_2c = hyy/2-4*H*HB+HB**2+F
    Ct_over_c = (ctt_over_2c+ct_over_c*(3*H-r1)
                  +trdd/2-6*H**2-rt-rt-2*r1*(H-HB)-hyy/2+2*H*HB)
    expected_ct = F+HB**2-8*H*HB+trdd/2-2*rt-4*r1*(H-HB)
    ch.zero('general_geometry_C_time_coefficient', Ct_over_c-expected_ct)
    C_over_c = 3*H-HB-2*r1
    ez_time = Ud+jj+(ct_over_c+C_over_c)*aa+p*Ct_over_c
    epsi_time = -K*(jj+(trdd/2-6*H**2-rt)*p+(3*H-r1)*aa)+2*b*ss*(Ud-2*H*U)-beta*rhod
    jerk_from_psi = s.solve(epsi_time, jj)[0]
    transport = CLEAN(ez_time.subs(jj, jerk_from_psi))
    expected = ((1+2*b*ss/K)*Ud+(2*H-3*HB-r1)*aa
                +p*(F+HB**2-8*H*HB+6*H**2-rt-4*r1*(H-HB))
                -(4*b*H*U*ss+beta*rhod)/K)
    ch.zero('eliminated_jerk_transport_identity', transport-expected)
    ch.zero('all_metric_acceleration_trace_cancels_after_elimination', s.diff(transport,trdd))
    ch.zero('transverse_metric_acceleration_cancels_before_jerk_elimination', s.diff(Ct_over_c,hyy))
    ch.add('reject_frozen_metric_before_elimination', s.diff(epsi_time,trdd)!=0 and s.diff(ez_time,trdd)!=0)
    for name, var in (('regulator_velocity',Ud),('actual_frame_acceleration_slope',F),
                      ('shift_time_gradient',rt),('dust_source_evolution',rhod)):
        ch.add('reject_omitted_'+name, s.diff(transport,var)!=0)
    ch.add('reject_omitted_regulator_spatial_Hessian_drift', s.diff(epsi_time,U)!=0)
    # Independently varied future dust: pT=sqrt(h)*rho/C, pT_dot=div(S*pT).
    # T_z=0 and (T_dot)_z=0 on this slice; normal dust flux therefore vanishes initially.
    dd,CC,pt,ptd,logvol = s.symbols('density_dot C pT pT_dot volume_log_dot', real=True)
    density_chain = dd-rho*(ptd/pt-logvol+beta*p)
    dust_rate = (-3*H+r1+beta*p)*rho
    ch.zero('dust_current_density_transport', density_chain.subs({dd:dust_rate,ptd:r1*pt,logvol:3*H}))
    acc_ez = -U-(3*H-HB-2*r1)*p
    acc_psi = -(3*H-r1)*p+2*b*U*ss/K-beta*rho/K
    G = (K+2*b*ss)*U-K*HB*p-K*p*r1-beta*rho
    ch.zero('earlier_scalar_compatibility_retained', K*(acc_ez-acc_psi)+G)
    req = CLEAN(s.solve(expected,F)[0])
    ch.zero('required_frame_slope_substitution', expected.subs(F,req))
    ch.add('undivided_identity_regular_at_p_zero', not CLEAN(expected).as_numer_denom()[1].has(p))
    hd,pd,rd,wd = s.symbols('Hdot_background pdot_background rhodot_background wave_ddot',real=True)
    U0 = HB*p+beta*rho/K
    Ud0 = hd*p+HB*pd+beta*rd/K-wd*p
    bridge = expected.subs({H:HB,r1:0,rt:0,ss:0,aa:pd,rhod:rd,F:wd-hd+HB**2,Ud:Ud0,U:U0})
    ch.zero('unchanged_quadratic_background_bridge', bridge)
    dims = {K:2,b:0,beta:0,H:1,HB:1,p:1,U:2,Ud:3,r1:1,rt:2,F:2,aa:2,rhod:5,ss:2}
    powers = [sum(dims[x]*n for x,n in term.as_powers_dict().items() if x in dims)
              for term in s.Add.make_args(s.expand(expected))]
    ch.add('transport_mass_dimension_three', all(x==3 for x in powers), [int(x) for x in powers])
    # Along this node V=V_dot=0, grad(psi)=grad(psi_dot)=0. Its original cusp
    # momentum and the required time/spatial derivative vanish; no third cusp tensor.
    t,z,A,sl,pp = s.symbols('t x A slope p_positive', positive=True)
    for sign in (-1,1):
        # A general O(t^2) frame value gives P_cusp^0=O(t^6).
        pc = -3*A*pp**2*(sl*t*t)**3
        ch.zero('original_cusp_node_two_time_derivatives_'+str(sign), s.diff(pc,t,2).subs(t,0))
    equations = dict(
        coordinate_gauge='N=1; initial h=I,h_dot=2H I; shift R=r1*x+..., R_dot=rt*x+...',
        C_general='(V^2)_t/2+V^2*((log sqrt(h))_t-R_z)-R*(V^2)_z/2+gamma*partial_z(V^z)-K_ij V^i V^j',
        C_over_w_squared=str(C_over_c), C_time_over_w_squared=str(CLEAN(Ct_over_c)),
        regulator_time_normal_limit=str(CLEAN(ez_time)), psi_time_at_node=str(epsi_time),
        jerk_from_psi=str(jerk_from_psi), undivided_transport=str(expected),
        rho_dot_from_dust_current=str(dust_rate), psi_acceleration_at_compatible_root=str(acc_ez),
        required_frame_slope=str(req), frame_slope_definition='F=partial_z(V_ddot_y)/partial_z(V_y) at node; NOT supplied by scalar equations',
        regulator_velocity_definition='Ud=Z_dot/w^2; not U_dot. A general U(t) ansatz is not adopted.',
        regularity='Necessary for a jointly time-differentiable regular-side quotient and finite scalar third-time jet; stronger than continuous acceleration; no weak-solution no-go.',
        metric='Arbitrary six metric second-time jets allowed; trace cancels only after eliminating jerk. They still enter the missing coupled frame acceleration equation.',
        cusp='Original C2 cusp retained; required nodal composite derivatives vanish; no ordinary third cusp derivative.',
        selected_velocity_disposition='UNRESOLVED_WITHOUT_ACTION_DERIVED_COUPLED_FRAME_SLOPE',
        no_new_data_adopted_or_evolved=True)
    return equations


def coordinate_controls(ch):
    print('INDEPENDENT_FOUR_COORDINATE_DENSITY_TIME_VARIATIONS', flush=True)
    records=[]
    for seed in (0,1):
        for orientation in (-1,1):
            H=mp.mpf(2+seed)/7; HB=mp.mpf(3)/11; p=mp.mpf(1+seed)/9
            aa=mp.mpf(2-seed)/13; jj=-mp.mpf(3+seed)/17; U=mp.mpf(3)/17; Ud=mp.mpf(2)/19
            slope=mp.mpf(orientation)/3; r1=mp.mpf(2)/29; ty=mp.mpf(3)/31
            rt=-mp.mpf(2)/41; tyt=mp.mpf(1)/37; F=-mp.mpf(2+seed)/7
            K=mp.mpf(3)/5; b=mp.mpf(5)/11; A=mp.mpf(2)/7; beta=mp.mpf(1)/17
            rho=mp.mpf(1)/5; rhod=(-3*H+r1+beta*p)*rho
            hdd=mp.matrix([[mp.mpf(1+i+j+seed)/43 for j in range(3)] for i in range(3)])
            hddz=mp.matrix([[mp.mpf(2+i+j)/53 for j in range(3)] for i in range(3)])
            fx=mp.mpf(1)/47; fz=-mp.mpf(2)/59; axx=mp.mpf(1)/61

            def geometry(t,z):
                hm=hdd+z*hddz
                h=(1+2*H*t)*mp.eye(3)+t*t*hm/2; hi=h**-1
                ht=2*H*mp.eye(3)+t*hm; hz=t*t*hddz/2
                shift=mp.matrix([0,(ty+tyt*t)*z,(r1+rt*t)*z])
                st=mp.matrix([0,tyt*z,rt*z]); sz=mp.matrix([0,ty+tyt*t,r1+rt*t])
                v=mp.matrix([fx*slope*z*t*t/2,slope*z*(1-HB*t+F*t*t/2),fz*slope*z*t*t/2])
                vt=mp.matrix([fx*slope*z*t,slope*z*(-HB+F*t),fz*slope*z*t])
                vz=mp.matrix([fx*slope*t*t/2,slope*(1-HB*t+F*t*t/2),fz*slope*t*t/2])
                gam=mp.sqrt(1+(v.T*h*v)[0]); n=mp.matrix([gam]+list(v-gam*shift))
                g=mp.zeros(4); gi=mp.zeros(4); g[0,0]=-1+(shift.T*h*shift)[0]; gi[0,0]=-1
                for i in range(3):
                    g[0,i+1]=g[i+1,0]=(h*shift)[i]; gi[0,i+1]=gi[i+1,0]=shift[i]
                    for j in range(3):
                        g[i+1,j+1]=h[i,j]; gi[i+1,j+1]=hi[i,j]-shift[i]*shift[j]
                dg=[]; dn=mp.zeros(4)
                for mu in range(4):
                    hh,sv,vv=(ht,st,vt) if mu==0 else (hz,sz,vz) if mu==3 else (mp.zeros(3),mp.zeros(3,1),mp.zeros(3,1))
                    gm=((v.T*hh*v)[0]+2*(v.T*h*vv)[0])/(2*gam)
                    dm=mp.zeros(4); dm[0,0]=2*(sv.T*h*shift)[0]+(shift.T*hh*shift)[0]
                    hv=hh*shift+h*sv
                    dn[mu,0]=gm
                    for i in range(3):
                        dm[0,i+1]=dm[i+1,0]=hv[i]
                        dn[mu,i+1]=vv[i]-gm*shift[i]-gam*sv[i]
                        for j in range(3): dm[i+1,j+1]=hh[i,j]
                    dg.append(dm)
                conn=[[[sum(gi[c,l]*(dg[a][l,bb]+dg[bb][l,a]-dg[l][a,bb]) for l in range(4))/2 for bb in range(4)] for a in range(4)] for c in range(4)]
                cov=mp.matrix(dn)
                for mu in range(4):
                    for j in range(4): cov[mu,j]+=sum(conn[j][mu][l]*n[l] for l in range(4))
                return mp.sqrt(mp.det(h)),gi+n*n.T,n,cov.T*n

            def fields(t,z):
                q=mp.matrix([p+(aa+axx*z*z)*t+jj*t*t/2,0,0,axx*z*t*t])
                zdd=mp.mpf(4)/23+z*z/67
                qz=mp.matrix([Ud*slope*slope*z*z+zdd*t,0,0,
                              2*U*slope*slope*z+2*Ud*slope*slope*z*t+z*t*t/67])
                zz=U*slope*slope*z*z+Ud*slope*slope*z*z*t+zdd*t*t/2
                return q,qz,zz

            def density(t,z,q,qz,zz):
                vol,hp,n,acc=geometry(t,z); Q=(n.T*q)[0]; Y=(q.T*hp*q)[0]
                return vol*(K*Q*Q/2-A*Y**mp.mpf('1.5')+b*zz*zz/2
                            -b*(qz.T*hp*q)[0]-b*zz*(acc.T*q)[0])

            def momentum(t,z,which,index):
                q,qz,zz=fields(t,z); original=q if which=='psi' else qz
                def at(value):
                    varied=mp.matrix(original); varied[index]=value
                    return density(t,z,varied if which=='psi' else q,varied if which=='Z' else qz,zz)
                return mp.diff(at,original[index])

            def ez(t,z):
                q,qz,zz=fields(t,z)
                direct=mp.diff(lambda value:density(t,z,q,qz,value),zz)
                return (direct-mp.diff(lambda tt:momentum(tt,z,'Z',0),t)
                        -mp.diff(lambda xx:momentum(t,xx,'Z',3),z))/(b*geometry(t,z)[0])

            def epsi(t):
                return (-mp.diff(lambda tt:momentum(tt,0,'psi',0),t)
                        -mp.diff(lambda xx:momentum(t,xx,'psi',3),0))/geometry(t,0)[0]-beta*(rho+rhod*t)

            predicted_psi=-K*(jj+(sum(hdd[i,i] for i in range(3))/2-6*H*H-rt)*p+(3*H-r1)*aa)+2*b*slope*slope*(Ud-2*H*U)-beta*rhod
            got=mp.diff(epsi,0); ep=abs(got-predicted_psi)/(1+abs(got)+abs(predicted_psi))
            ch.small('coordinate_differentiated_psi_'+str(seed)+'_'+str(orientation),ep,'1e-45')
            predicted_z=(Ud+jj+(5*H-3*HB-2*r1)*aa
                         +p*(F+HB*HB-8*H*HB+sum(hdd[i,i] for i in range(3))/2-2*rt-4*r1*(H-HB)))
            errors=[]
            for step,tolerance in (('1e-12','1e-20'),('1e-18','1e-30')):
                x=mp.mpf(step)
                got=(mp.diff(lambda tt:ez(tt,x),0)+mp.diff(lambda tt:ez(tt,-x),0))/(2*slope*slope*x*x)
                er=abs(got-predicted_z)/(1+abs(got)+abs(predicted_z))
                ch.small('coordinate_regulator_time_normal_limit_'+str(seed)+'_'+str(orientation)+'_'+step,er,tolerance)
                errors.append(dict(normal_probe=step,normalized_error=SHOW(er),tolerance=tolerance))
            records.append(dict(seed=seed,slope=SHOW(slope),psi_time_error=SHOW(ep),regulator_time_probes=errors,
                                all_six_metric_second_time_jets=True,spatial_metric_second_time_jets=True,
                                arbitrary_three_frame_second_time_jets=True,shift_time_gradient=SHOW(rt),
                                regulator_second_time_jet='nonzero arbitrary; not solved or set to zero'))
    return records


def unpack(record):
    a,b=record['exact_binary_endpoints']
    return iv.mpf([mp.mpf(tuple(a)),mp.mpf(tuple(b))])


def required_case_enclosures(ch):
    print('ENCLOSE_REQUIRED_NOT_YET_DERIVED_FRAME_SLOPES_ALL_NINE_CASES', flush=True)
    names='MP2 MU2 c1 c2 c3 c4 K_Q A b beta zeta Rc H H0 vz vz1 vz2 R q p Z Zd Z1 Z2 D rd pot k alpha xi zc zdc'
    u={n:s.Symbol(n,real=True) for n in names.split()}; u['p']=s.Symbol('p',positive=True)
    parse=lambda text:s.sympify(text,locals=u)
    al,x,k=u['alpha'],u['xi'],u['k']
    pieces=[parse(text) for text in READ(PROOF)['polynomial_pieces']]
    polynomial=sum(al**j*pn for j,pn in enumerate(pieces))
    qscaled=(k*((2*x-1)*polynomial-2*x*(1-x)*s.diff(polynomial,x))).subs(x,0)
    exact=READ(base.PREV+'formulas.json')
    sub={u['vz']:0,u['vz1']:k*s.sqrt(al),u['vz2']:0,u['R']:0,u['Z']:0,u['Zd']:0,u['Z1']:0,u['Z2']:2*u['zc']*k*k*al}
    energy=CLEAN(parse(exact['energy_without_dust']).subs(sub,simultaneous=True))
    flux=CLEAN(parse(exact['lapse_flux_divergence']).subs(sub,simultaneous=True))
    qe=base.Eval([qscaled]); ef=base.Eval([energy,flux])
    old={(row['family'],row['eta']):row for row in READ(OLD_CERT)}
    out=[]; es=s.Symbol('eta')
    for row in READ(COUPLED+'certificates.json'):
        key=(row['family'],row['eta']); item=old[key]; et=s.Rational(row['eta'])
        par=READ(base.PLANAR)['families'][row['family']]['parameter_map']
        vals={n:base.interval_s(s.sympify(v,locals={'eta':es}).subs(es,et)) for n,v in par.items()}
        eta=base.interval_s(et); rc=iv.sqrt(eta)
        vals.update(H=unpack(row['H_bracket']),H0=unpack(item['H_background']),zc=unpack(row['U_bracket']),
                    zdc=unpack(item['regulator_velocity_coefficient']),alpha=unpack(item['amplitude_squared_range']),
                    k=iv.mpf(40),p=eta/5,Rc=rc,rd=rc/4,
                    pot=3*eta/2+eta**2*(iv.mpf(1)/24+iv.mpf(1)/28)+eta**3*(iv.mpf(1)/480+iv.mpf(3)/28))
        vals['D']=rc/(1-vals['zeta']*rc**2*vals['alpha']/2)
        err=unpack(row['normalized_inverse_errors'][0]['gradient'])
        vals['q']=vals['alpha']*(qe.interval(vals)[0]+base.box(err))
        ev,jv=ef.interval(vals); rho=-ev-jv
        H,HB,U,Ud,pp,r1,K,bb,be,ss=[vals[n] for n in ('H','H0','zc','zdc','p','q','K_Q','b','beta','alpha')]
        ss*=vals['k']**2
        acc=-U-(3*H-HB-2*r1)*pp
        rhod=(-3*H+r1+be*pp)*rho
        remainder=((1+2*bb*ss/K)*Ud+(2*H-3*HB-r1)*acc-(4*bb*H*U*ss+be*rhod)/K)
        required=-HB**2+8*H*HB-6*H**2+4*r1*(H-HB)-remainder/pp
        ident=row['family']+'_'+row['eta']
        ch.add('inherited_restricted_root_'+ident,row['status']=='CERTIFIED_RESTRICTED_COUPLED_MEAN_NODE_ROOT')
        ch.add('positive_node_density_and_nonzero_p_'+ident,base.lo(rho)>0 and base.lo(pp)>0)
        ch.add('finite_required_slope_enclosure_'+ident,mp.isfinite(base.lo(required)) and mp.isfinite(base.hi(required)))
        out.append(dict(family=row['family'],eta=row['eta'],amplitude_squared=base.pack(vals['alpha']),
                        node_shift_gradient=base.pack(r1),node_density=base.pack(rho),
                        required_frame_acceleration_slope_for_rt_zero=base.pack(required),
                        physical_frame_slope='NOT_COMPUTED_FROM_COUPLED_FRAME_METRIC_EQUATIONS',
                        selected_velocity_disposition='UNRESOLVED',
                        interpretation='Necessary input range at the certified restricted root, not a frame equation, frequency, physical cutoff, sufficiency certificate or velocity rejection.'))
    ch.add('all_registered_cases_retained',len(out)==9)
    return out


def calculate():
    mp.mp.dps=100; iv.dps=80
    pins,before=sources(); ch=base.Checks()
    equations=derive(ch); independent=coordinate_controls(ch); cases=required_case_enclosures(ch)
    _,after=sources(); ch.add('all_source_bytes_sidecars_metadata_unchanged',before==after)
    ok=all(row['passed'] for row in ch.rows)
    summary=dict(validation='PASS_NECESSARY_NODE_VELOCITY_TRANSPORT_ONLY' if ok else 'FAIL_OR_UNRESOLVED_NODE_VELOCITY_TRANSPORT',
                 passed=sum(row['passed'] for row in ch.rows),total=len(ch.rows),checks=ch.rows,
                 source_sha256=pins,source_metadata=before,tested_case_count=len(cases),
                 selected_regulator_velocity='UNRESOLVED_WITHOUT_COUPLED_FRAME_ACCELERATION',
                 full_coupled_frame_acceleration_solved=False,full_initial_data_admission=False,
                 state_adopted_or_evolved=False,action_no_go=False,stage2_complete=False,stage3_entered=False,
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
                 status='NECESSARY_TIME_TRANSPORT_DERIVED_COUPLED_FRAME_INPUT_AND_PHYSICAL_WINDOW_OPEN',
                 missing_required_physics=['actual action-derived coupled metric/frame acceleration slope',
                    'remaining rank-changing consistency and persistence, physical reduced Hessian/Cauchy/energy domain',
                    'nonlinear evolution error, nonempty physical window and healthy GR',
                    'identifying matter-residue and nonlinear-force matching inputs'])
    return {'summary.json':summary,'equations.json':equations,'independent.json':independent,'cases.json':cases}


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output'); parser.add_argument('--replay')
    args=parser.parse_args()
    if bool(args.output)==bool(args.replay): parser.error('choose exactly one output or read-only replay')
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'): raise ValueError('outside science output root')
    if args.output: dest.mkdir(parents=True,exist_ok=False)
    original={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
    results=calculate(); payloads={name:ENC(value) for name,value in results.items()}
    for name,raw in list(payloads.items()): payloads[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode('ascii')
    if args.replay:
        if set(original)!=set(payloads): raise ValueError('replay file-set mismatch')
        for name,raw in payloads.items():
            path=dest/name
            if path.read_bytes()!=raw: raise ValueError('recomputed bytes differ '+name)
            if (SHA(path.read_bytes()),path.stat().st_size,path.stat().st_mtime_ns)!=original[name]:
                raise ValueError('original metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payloads.items():
            with (dest/name).open('xb') as stream: stream.write(raw)
    su=results['summary.json']
    print(json.dumps({name:su[name] for name in ('validation','passed','total','selected_regulator_velocity','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1


if __name__=='__main__': raise SystemExit(main())
