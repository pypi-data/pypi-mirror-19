import alabaster
import ictools

project = 'ic-tools'
copyright = 'AWeber Communications, Inc.'
version = ictools.version
release = '.'.join(str(v) for v in ictools.version_info[:2])

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
master_doc = 'index'
source_suffix = '.rst'

pygments_style = 'sphinx'
html_theme = 'alabaster'
html_theme_path = [alabaster.get_path()]
html_sidebars = {'**': ['about.html', 'navigation.html']}
intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
}
