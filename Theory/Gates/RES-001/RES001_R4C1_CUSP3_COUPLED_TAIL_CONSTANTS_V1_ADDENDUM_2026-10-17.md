# Complete cusp response: low-neighbour and leading-wave constant proof

17 October 2026. Frozen before the companion executable. No change to V3,
its constants, source inputs, action, acceptance or tolerances.
Conditional; review DEFERRED; physics_pass=false; gate_effect=NONE.

The first tail output m=4 couples to n=3. Do not apply the old n>=4 coefficient
estimate to this neighbour. Instead, for every odd |n|>=3,

~~~text
|c_n| = 4/[pi |n|(n^2-4)] <= 36/[5 pi |n|^3],
36/(5 n^3)-4/[n(n^2-4)] = 16(n^2-9)/[5 n^3(n^2-4)].
~~~

For even m>=4, |m+-1|>=3m/4. With pi>3, P=45/10108 and
sqrt(5/722)<1/12, the required scaled input constants are at most
256/45 for c, 256P/45 for r_dot, and 256P/405 for r. These are bounded
by V3's existing 128/9, 128P/9 and 64P/27 constants respectively.
For the direct h_m coefficient, its existing 1024/(105 m^4) bound follows
from m^2-1>=15m^2/16, m^2-9>=7m^2/16 and pi>3.

The companion must verify those inequalities analytically on the full domain,
not by a finite-mode scan, and bind its constants to the unchanged V3 source.
It must check mean c_1=h_0=4/(3pi), the displacement conversion, the leading
frequency >12, leading energy inequality, and |w_dot|<205/4.
The infinite tail begins at |m|>=4. Also compute an explicit continuous
bound for the retained m=+-2 pair from V3's full weighted forcing numerator
at ell=80, with all22 field/rate reconstructions. Its lower neighbours are
n=1,3, with scaled input majorants
[P/27,4P/9,P/405,4P/45,4/9,4/45,4/15].
Use the inherited full linear growth constant and zero free initial data;
do not treat earlier sampled m=2 trajectories as a continuum proof.
LambdaU has no time derivative in the generic action. V3's zero LambdaU
velocity slot is an unused Euler-jet representative, not a prediction that
the time derivative of the reconstructed multiplier vanishes. Verify the
absence of those generic Hessian time-jet entries and label that slot
explicitly. No actual LambdaU_dot bound is admitted by these artifacts.
Fresh exclusive receipts, exact read-only replay and hash/size/mtime checks
are required. It proves constants used in the complete coupled calculation;
it does not replace that calculation or admit a physical window.
