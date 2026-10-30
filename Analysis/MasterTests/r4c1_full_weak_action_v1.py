"""Original implicit planar action, including nonlinear curvature and dust.

No evolution solver, projection, nodal inversion or physical admission.
Layout: q16,v16,d16,S3,Sz3,N,Nz (56 entries).
q: h6,V3,u,v,r,psi,Z,tau,epsilon. All lapse/shift variations retained.
"""
import mpmath as mp

HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))


class WeakAction:
    def __init__(self,body,parameters):
        self.body=body
        self.par=parameters

    def curvature(self,q,d):
        b=self.body;h=b.tensor(q);hi=b.inv3(h);dh=b.tensor(d)
        volume=b.sqrt(b.det3(h))
        G=[[[sum(hi[k][l]*((dh[l][j] if i==2 else 0)+(dh[l][i] if j==2 else 0)
                           -(dh[i][j] if l==2 else 0))/2 for l in range(3))
              for j in range(3)] for i in range(3)] for k in range(3)]
        gg=volume*sum(hi[i][j]*sum(G[k][i][l]*G[l][j][k]-G[k][i][j]*G[l][k][l]
                                   for k in range(3) for l in range(3))
                      for i in range(3) for j in range(3))
        flux=volume*(sum(hi[i][j]*G[2][i][j] for i in range(3) for j in range(3))
                     -sum(hi[i][2]*G[j][i][j] for i in range(3) for j in range(3)))
        return gg,flux

    def curvature_density(self,A):
        gg,flux=self.curvature(A[:16],A[32:48])
        return self.par['MP2']*(A[54]*gg-A[55]*flux)/2

    def density(self,A):
        if len(A)!=56:raise ValueError('expected 56 original-jet entries')
        b=self.body;p=self.par
        q,v,d,S,Sz,N,Nz=A[:16],A[16:32],A[32:48],A[48:51],A[51:54],A[54],A[55]
        h=b.tensor(q);hi=b.inv3(h);R=S[2]
        K=[]
        for slot,(i,j) in enumerate(HM):
            lie=R*d[slot]+(sum(h[i][a]*Sz[a] for a in range(3)) if j==2 else 0)
            lie+=(sum(h[j][a]*Sz[a] for a in range(3)) if i==2 else 0)
            K.append((v[slot]-lie)/(2*N))
        c=b.dot(q[6:9],b.mv(h,q[6:9]));gamma=b.sqrt(1+c)
        X=[(v[6+i]-R*d[6+i]+q[8]*Sz[i]+gamma*hi[i][2]*Nz)/N for i in range(3)]
        canonical=[(v[i]-R*d[i])/N for i in (9,10,11)]
        ps=(v[12]-R*d[12])/N;zh=(v[13]-R*d[13])/N
        volume=b.sqrt(b.det3(h))
        local=b.body(q[:14]+[mp.mpf(0)],d[:14]+[mp.mpf(0)],K+X+canonical,ps,p)
        temporal=-p['b']*zh*(c*ps+gamma*q[8]*d[12])
        tauhat=(v[14]-R*d[14])/N
        C=b.exp(p['beta']*q[12])
        dust=-q[15]*(C*C*(-tauhat*tauhat+hi[2][2]*d[14]**2)+C**4)/2
        L=N*volume*(local+temporal+dust)+self.curvature_density(A)
        return L,[2*z for z in K]+X+canonical+[ps,zh,tauhat,(v[15]-R*d[15])/N]

    def gradient(self,A,curvature_only=False):
        b=self.body;tape=b.Tape();variables=[tape.var(z) for z in A]
        L=self.curvature_density(variables) if curvature_only else self.density(variables)[0]
        return b.val(L),mp.matrix(tape.grad(L,variables))

    def hv(self,A,direction,step,curvature_only=False):
        _,grad=self.gradient([z+mp.j*step*v for z,v in zip(A,direction)],curvature_only)
        return mp.matrix([mp.im(v)/step for v in grad])
