# V1 trace momentum drift execution failure

The first executable stopped before writing a receipt. An interval scalar
on the left of a Taylor jet product in the lapse rate caused mpmath to
attempt conversion of the jet to an interval scalar and raise
`NotImplementedError`. This execution supplied no numerical result.

- V1 source SHA-256 `1e4a0a60ce3ee6e07011c851358fd93e244073d25f0714afa12933466cb831b1`
- Local optimizer transcript SHA-256 `089d66f6a6a4d51be98c9d18620194a21465c8a32d9e5d5faacc0f0c3cbca6cf`

V2 uses the jet's multiplication with the same interval scalar on the
right. The inputs, equations and controls are unchanged. The V1 source and
sidecar are preserved.
