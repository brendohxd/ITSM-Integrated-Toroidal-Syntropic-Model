# A16.2 pressure evolution V1 stopped attempt

16 November 2026. Code inspection found that two controls used IV object
identity rather than endpoint equality. These would falsely fail even with
matching numerical enclosures. The running V1 attempt was interrupted before
receipts; no Python computation remained afterward. No physical failure or
valid trajectory certificate was produced. Preserve V1 source, contract,
manifest and empty attempt directory. V2 compares explicit endpoint values;
all equations and acceptance requirements remain unchanged.
