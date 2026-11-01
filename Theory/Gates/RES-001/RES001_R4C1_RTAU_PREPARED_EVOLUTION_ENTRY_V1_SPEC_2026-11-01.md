# Prepared evolution entry implementation V1

High acknowledged. Implement the first required field/momentum block from
the frozen evolution contract before gauge/current closure. Use the actual
clock-substituted Hessian and its spatial coefficients, validated 13-rate
inverse and differentiated inverse. Return all fourteen momentum Euler
rows; the auxiliary row remains its secondary tangent, not an evolved
independent auxiliary momentum. Do not supply a physical Zdot or shift solve
by setting an unknown to zero. The inherited exact zero cross-coefficients
justify only an unused auxiliary-rate placeholder in this nonauxiliary block.

Validate rate round-trip and complete canonical momentum Euler variation
against independently prescribed rate jets at all three prepared points.
Use 1e-35 inverse error and 1e-28 local comparison requirements. Reject
omitted spatial Euler flux and coefficient derivatives. Preserve all sources
and exact replay. This component is NOT the complete evolution operator,
gauge closure, transported density row or a physical norm. Those remain
required by the owning contract. physics_pass=false; review DEFERRED.
