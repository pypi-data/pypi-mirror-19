from setuptools import setup, find_packages

version = 1.0

long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='affinitic.tools',
    version=version,
    description='Bunch of python tools',
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='affinitic tools',
    author='Affinitic',
    author_email='info@affinitic.be',
    url='https://github.com/affinitic/affinitic.tools',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['affinitic'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
)
