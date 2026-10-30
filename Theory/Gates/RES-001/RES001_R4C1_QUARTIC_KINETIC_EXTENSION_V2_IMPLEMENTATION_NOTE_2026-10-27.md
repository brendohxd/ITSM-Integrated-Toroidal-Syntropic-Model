# Kinetic extension V2: exact endpoint controls

27 October 2026. Same scientific contract as QUARTIC_KINETIC_EXTENSION_V1.
No equation, interval range, partition sequence or tolerance changes.

V1 source SHA256 083fe670886cc2d1fdfc222ac61d28c2c4aa66a6ce12d91ffdfa67b19a335000
and attempt-01 receipt SHA256
4b68c9ae0cf43350caad2b94f70e557a795aacd7eaa61fc5f258eb05f8b4d689
remain unchanged. V1 passed 24/28, including exact block identities and the
uniform complement inverse. Four signed endpoint/step controls failed.

Their ratio loop used Python integers for +/-1, then evaluated ratio/500
before SymPy conversion. Python floating 0.002 is slightly outside the
exact interval endpoint. acos(500*w) became complex; a complex-step Hessian
test on a complex baseline divided an existing imaginary component by the
step. The exact half controls used SymPy Rational and did not have this defect.
This failure is not interpreted as agreement or as a physical operator failure.

V2 converts the ratio to SymPy Rational BEFORE division and computes the
control angle from the exact ratio. It also rejects nonreal baselines and
out-of-domain field values explicitly. All five original controls and both
steps remain. Freeze V2 before launch; pin V1 and its failure receipt.
Conditional, review DEFERRED, physics_pass=false, G1 INCOMPLETE.
