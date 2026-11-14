# Gauge mean and trace rate V1 preflight failure

The inherited density-comparison manifest did not directly pin the
prepared weak-coefficient receipt used for the scale rate. V1 halted
before evaluating any new bounds. V2 adds this existing receipt's
sidecar hash explicitly and verifies it with the other source pins.
The optimizer preserved the traceback in
`.local/itsm-context/output-4aca90c6cfd24dccb484193113d54f3e.txt`.
