### Sphinx installation
1. Install sphinx and a theme 
```
python3 -m pip install Sphinx sphinx-rtd-theme
mkdir docs && cd docs 
sphinx-quickstart   # defaults for all 
cd ../src/ 
sphinx-apidoc -o docs .
cd ../docs/ 
make html
```
2. change extensions to: 
```
extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']
```
3. Add source directory path to conf.py by adding: 
```
import sys 
sys.path.append("../../path/to/src_dir")
```
