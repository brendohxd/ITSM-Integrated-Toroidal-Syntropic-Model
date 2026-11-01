# Clock-density V3 zero-slot type normalization

V2 stopped before a receipt when the density-time evaluator accessed a
spatial-jet coefficient on a literal zero in the original profile's metric
slots. The density differentiator already casts these correctly internally;
the new external reconstruction path needed the same explicit normalization.
V3 casts every returned state slot through the existing spatial Jet.cast.
Values, derivatives, equations, uncertainty domains and tolerances do not
change. Preserve V1/V2 failure records and source hashes.
