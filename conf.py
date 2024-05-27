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

# conf.py

# Import the Furo theme
html_theme = "furo"

# Specify Pygments styles for code highlighting
pygments_style = "sphinx"  # for light mode
pygments_dark_style = "monokai"  # for dark mode


html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
    },
    "dark_css_variables": {
        "color-brand-primary": "#FF79C6",
        "color-brand-content": "#FF79C6",
    }
}


