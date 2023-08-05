"""
lazy doc module

This module guesses the information and tries to generate the
information based on the sphinx quickstart.

"""


import os
import sys
import subprocess

def cleanup():
    """Removes the doc folder to clean up the sphinx docs"""
    from shutil import rmtree
    try:
        rmtree("doc")
    except:
        pass

def get_config(config_file='setup.cfg'):
    """Extract the metadata from the appropriate config file.

    Supports `setup.cfg` and reading in `yaml` related files.
    """
    if config_file.endswith('cfg'):
        if sys.version_info > (3, 0):
            import configparser
            config = configparser.ConfigParser()
            config.read(config_file)
        else:
            import ConfigParser
            config = ConfigParser.ConfigParser()
            config.read(open(config_file, 'r'))

        version = config.get('metadata', 'version')
        project = config.get('metadata', 'name')
        author = config.get('metadata', 'author')
    elif config_file.endswith('yml') or config_file.endswith('yaml'):
        import yaml
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        version, project, author = cfg['version'], cfg['project'], cfg['author']
    return version, project, author

def generate():
    """Generate the sphinx quickstart settings based on biased defaults"""
    version, project, author = get_config()
    quickstart = ['sphinx-quickstart', 'doc', '-q',
                  '-p', '"{project}"'.format(project=project),
                  '-a', '"{author}"'.format(author=author),
                  '-v', '"{version}"'.format(version=version),
                  '--ext-autodoc', '--extensions=sphinx.ext.autosummary']

    recommonmark_settings = """
from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
"""
    cleanup()
    subprocess.call(quickstart)

    with open('doc/conf.py', 'a') as f:
        f.write(recommonmark_settings)

def document():
    """(Re)generate all documentation."""
    _, project, _ = get_config()
    # generate doc stuff
    gen_docs = ['sphinx-apidoc', '-o', 'doc',
                project, '--force']
    make_html = ['make', 'html']
    subprocess.call(gen_docs)
    os.chdir("doc")
    subprocess.call(make_html)
    os.chdir("..")
