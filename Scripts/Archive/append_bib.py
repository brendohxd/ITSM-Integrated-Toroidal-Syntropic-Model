import os

bib_path = r"C:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Manuscript\references.bib"
bib_add = """
@book{misner_gravitation,
  title={Gravitation},
  author={Misner, C. W. and Thorne, K. S. and Wheeler, J. A.},
  year={1973},
  publisher={W. H. Freeman}
}

@article{ellis_maccallum,
  title={A Class of Homogeneous Cosmological Models},
  author={Ellis, G. F. R. and MacCallum, M. A. H.},
  journal={Communications in Mathematical Physics},
  volume={12},
  pages={108--141},
  year={1969}
}
"""
with open(bib_path, "a", encoding="utf-8") as f:
    f.write(bib_add)
print("Added references.")
