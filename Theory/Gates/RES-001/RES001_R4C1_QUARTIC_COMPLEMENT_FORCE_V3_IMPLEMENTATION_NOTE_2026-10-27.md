# Analytic complement force V3: AD-aware interval constants

27 October 2026. Same frozen contract, equations, domains and criteria.
V2 source ee07404a2d638624646d5c70ebda6f2919ea8f2e5a26b849c856d4e383f2601b
is preserved. It stopped before an enclosure receipt when a leading interval
parameter multiplied a reverse-mode Node: mpmath's interval conversion raises
NotImplementedError instead of delegating that operation to the Node.
The full ignored log .local/itsm-context/output-3a170a60a14e4a1e938710309e8958c4.txt
has SHA256 1940d06c44b98b63f091feeed0377cb91756a70c2db7e150daa382eeb57a7c23.

V3 wraps interval parameters as zero-direction Dual constants. Dual arithmetic
explicitly returns NotImplemented for the pinned reverse Node type, allowing
its original overload to build the tape. All actual value/direction arithmetic
still uses outward interval scalars; no interval-to-point conversion is used.
Keep V1/V2 and their sidecars/logs. Freeze V3 before launch. No failed run is
reported as an accepted enclosure, and no mathematical test is relaxed.
