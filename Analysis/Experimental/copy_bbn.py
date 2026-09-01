import shutil
import os

src = os.path.join(os.path.dirname(__file__), 'external')
dst = os.path.join(os.path.dirname(__file__), 'build', 'lib.win-amd64-cpython-313', 'classy', 'external')

if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)
print("SUCCESS: Copied external folder to classy build library!")
