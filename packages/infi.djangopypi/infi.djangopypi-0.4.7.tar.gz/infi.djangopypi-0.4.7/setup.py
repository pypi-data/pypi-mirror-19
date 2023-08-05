
SETUP_INFO = dict(
    name = 'infi.djangopypi',
    version = '0.4.7',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://github.com/Infinidat/djangopypi',
    license = 'PSF',
    description = """Simple PyPI server written in django""",
    long_description = """Simple PyPI server written in django. Allows you to register/upload with distutils and install with easy_install/pip.""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'django-haystack==2.4.0',
'django-registration==1.0',
'django<1.7',
'docutils',
'setuptools',
'south',
'Whoosh',
],
    namespace_packages = [],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = ['manage = app.scripts.manage:execute'],
        gui_scripts = [],
        ),
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

