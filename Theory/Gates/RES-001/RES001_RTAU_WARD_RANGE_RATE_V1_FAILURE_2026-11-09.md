# Weighted Ward range rate V1 control failure

V1 compared two algebraically equivalent periodic integrals by SymPy
expression-tree equality. The direct weighted residual check returned
false while the differentiated identity and all other controls passed.
V2 simplifies the difference of the exact integrals before comparing
with zero. Neither the identity nor a tolerance changes. The optimizer
preserved the exact traceback in
`.local/itsm-context/output-17fe876449bd4faaa33633a5a2f75aa6.txt`.
