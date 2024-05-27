import os
import sys
sys.path.insert(0, os.path.abspath('.'))

from my_style import MyStyle

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]



# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'my_style.MyStyle'
