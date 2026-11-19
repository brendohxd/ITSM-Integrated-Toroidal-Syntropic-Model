# Retained Volterra V1 receipt serialization failure

19 November 2026. All five filtered inputs and independent solution archives
were saved before comparison. V1 then failed while writing mode receipts:
TypeError: Object of type bool is not JSON serializable. A NumPy floating
comparison produced a non-native boolean. No main scientific receipt was
produced and V1 is not labeled PASS. Preserve source, contract, pins, archives
and the private failure log output-173c34788a764cbd8cf032bbf9327301.txt,
SHA256 8a8bcfaba6ab71c9f60a6ec2c3ace2eba267231f3968f5142de7693f653975e5.
V2 converts diagnostic metadata to Python float/bool; equations are unchanged.
