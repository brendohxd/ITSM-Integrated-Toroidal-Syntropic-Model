# Trace Green rate V2 receipt construction failure

The computation reached receipt construction, where a filename substitution
had changed the reference to the frozen V1 contract to a nonexistent V2
contract. No receipt was produced. V3 restores the exact V1 contract path
and labels the executable's own version separately. Equations, coefficient
evaluation and checks are unchanged. The optimizer retained the traceback in
`.local/itsm-context/output-07834186654149e2876a97c36a09e3e3.txt`.
