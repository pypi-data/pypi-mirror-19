from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='wolfeutils',
    version='0.0.1a1',
    description='Utilities for Wolfe Lab',
    long_description=readme(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    url='http://github.com/kastman/wolfeutils',
    author='Erik Kastman',
    author_email='erik.kastman@gmail.com',
    license='GPL',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'labelTree = wolfeutils.cli:labelNewickCli',
            'createPanseqFasta = wolfeutils.cli:labelNewickCli',
            'pgapBasicAnalysis = wolfeutils.cli:pgapBasicAnalysisCli',
        ]
    },
    scripts=['wolfeutils/comparative/panseq/runPanSeq.sh'],
    install_requires=['biopython', 'pandas', 'seaborn', 'matplotlib',
                      'matplotlib_venn', 'numpy', 'scipy'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
