import ast
import re
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('effectus/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='effectus',
    version=version,
    install_requires=[
        'click',
        'quicktions',
        'xlwings'
    ],
    entry_points={
        'console_scripts': [
            'make_summary= effectus.cli:cli_make_summary',
            'attain_causes = effectus.cli:cli_attain_causes',
            'attain_effects = effectus.cli:cli_attain_effects',
            'separate_causes = effectus.cli:cli_separate_causes',
            'separate_effects = effectus.cli:cli_separate_effects',
            'make_summary_xl = effectus.cli:cli_make_summary_xl',
            'attain_effects_xl = effectus.cli:cli_attain_effects_xl',
            'attain_causes_xl = effectus.cli:cli_attain_causes_xl',
            'separate_causes_xl = effectus.cli:cli_separate_causes_xl',
            'separate_effects_xl = effectus.cli:cli_separate_effects_xl',
        ],
    },
    description='effectus tells you which minority of causes provokes '
                'which majority of effects.',
    long_description=readme, #+ '\n\n' + history,
    author="Benjamin Weber",
    author_email='mail@bwe.im',
    url='http://bitbucket.com/hyllos/effectus-python',
    package_dir={'effectus': 'effectus'},
    packages=['effectus'],
    license="MIT license",
    zip_safe=False,
    include_package_data=True,
    package_data={
        '': ['csv/*']
    },
    keywords='pareto cause-effect power-law entropy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]
)
