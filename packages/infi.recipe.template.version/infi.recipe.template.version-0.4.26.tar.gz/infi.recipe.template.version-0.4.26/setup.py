
SETUP_INFO = dict(
    name = 'infi.recipe.template.version',
    version = '0.4.26',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://github.com/Infinidat/infi.recipe.template.version',
    license = 'PSF',
    description = """'an extension to collective.recipe.template'""",
    long_description = """None""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'collective.recipe.template',
'git-py',
'infi.execute',
'infi.os_info',
'setuptools',
'zc.buildout'
],
    namespace_packages = ['infi', 'infi.recipe', 'infi.recipe.template'],

    package_dir = {'': 'src'},
    package_data = {'': [
'default.in'
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = """
    [zc.buildout]
    default = infi.recipe.template.version.recipe:Recipe
    """
    )

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

