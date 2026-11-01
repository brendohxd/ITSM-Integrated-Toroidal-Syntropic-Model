# Clock identity V2 implementation correction

V1 stopped before numerical evaluation: INITIAL was looked up as a local rather
than the frozen module constant. V2 pins its explicit existing receipt path.
Static inspection also corrects use of the Jet power API for sqrt and avoids
interval-left multiplication of a Jet. Same identity, probes and 1e-28 limit.
V1 source/failure retained. No action, inputs or physical scope changed.
