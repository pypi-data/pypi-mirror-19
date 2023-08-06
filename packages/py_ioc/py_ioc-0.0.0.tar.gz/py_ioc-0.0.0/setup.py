from setuptools import setup, find_packages

setup(
    name='py_ioc',
    version='0.0.0',
    description='Inversion of Control Container '
                'for Automatic Dependency Injection',
    author='Emil Person',
    author_email='emil.n.persson@gmail.com',
    url='https://github.com/emilniklas/py_ioc',
    download_url='https://github.com/emilniklas/py_ioc/tarball/0.0.0',
    keywords=['ioc', 'di', 'dependency injection', 'inversion of control'],
    packages=find_packages(exclude=('tests')),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
