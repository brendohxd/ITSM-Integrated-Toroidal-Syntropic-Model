"""Actual unreduced canonical field/momentum rows at a prepared point.

Caller supplies spatial jets and shift variation. Gauge closure, auxiliary
rate reconstruction, current-density row and physical norm remain external.
"""
import mpmath as mp

def apply(ctx,dq,dd,dp,dS,dSz):
 J=ctx['J'];hj=ctx['hj'];L=ctx['L'];iv=mp.iv
 assert len(dq)==len(dd)==len(dp)==14 and len(dS)==len(dSz)==3
 assert dp[13]==0,'auxiliary primary momentum must be retained as zero'
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);mid=lambda x:(lo(x)+hi(x))/2
 ab=lambda x:max(abs(lo(x)),abs(hi(x)))
 M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)]
 Mz=[[hj(L,14+i,14+k).c[1] for k in range(13)] for i in range(13)]
 def solve(rhs):
  x=mp.lu_solve(mp.matrix([[mid(t) for t in row] for row in M]),mp.matrix([mid(t) for t in rhs]))
  xx=[iv.mpf(mp.nstr(t,75)) for t in x]
  residual=[rhs[i]-sum((M[i][k]*xx[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
  error=ctx['Minv']*iv.sqrt(sum((iv.mpf(ab(t))**2 for t in residual),iv.mpf(0)))
  return [iv.mpf([lo(t)-hi(error),hi(t)+hi(error)]) for t in xx],error
 rhs=[dp[i]-sum((hj(L,14+i,k)*dq[k]+hj(L,14+i,28+k)*dd[k] for k in range(14)),J(0))-sum((hj(L,14+i,42+k)*dS[k]+hj(L,14+i,45+k)*dSz[k] for k in range(3)),J(0)) for i in range(13)]
 v,e0=solve([t.c[0] for t in rhs]);vz,e1=solve([rhs[i].c[1]-sum((Mz[i][k]*v[k] for k in range(13)),iv.mpf(0)) for i in range(13)])
 dv=[J(coefficients=[a,b,iv.mpf(0)]) for a,b in zip(v,vz)]
 # The unused auxiliary-rate slot cannot enter these equations: this was
 # proved in the owning mixed operator. It is not returned as physical Zdot.
 dy=dq+dv+[J(0)]+dd+dS+dSz
 force=[];flux=[];momentum_rate=[];coefficient_drift=[]
 for i in range(14):
  f=sum((hj(L,i,k)*dy[k] for k in range(48)),J(0))
  g=sum((hj(L,28+i,k)*dy[k] for k in range(48)),J(0))
  force.append(f.c[0]);flux.append(g.c[1]);momentum_rate.append(f.c[0]-g.c[1])
  coefficient_drift.append(sum((hj(L,28+i,k).c[1]*dy[k].c[0] for k in range(48)),iv.mpf(0)))
 return dict(field_rate=dv,momentum_rate=momentum_rate,spatial_flux=flux,coefficient_drift=coefficient_drift,inverse_errors=[e0,e1],auxiliary_secondary_tangent=momentum_rate[13],auxiliary_field_rate='NOT_SUPPLIED',gauge_shift='CALLER_SUPPLIED_NOT_SOLVED',current_density_row='NOT_CLOSED')
