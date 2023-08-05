from setuptools import setup, find_packages

setup(
    name = "contemplate",
    version = "0.1",
    packages = find_packages(),
    author = "Nicolas Limage",
    author_email = 'github@xephon.org',
    description = "multi templating engines command-line interface",
    license = "MIT",
    keywords = "content template command-line",
    url = "https://github.com/nlm/contemplate",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = [
    ],
    entry_points = {
        'console_scripts': [
            'contemplate = contemplate.__main__:main',
            'tpl = contemplate.__main__:main',
        ],
        'contemplate_source_v1': [
            'file = contemplate.source.file:FileSource',
        ],
        'contemplate_parser_v1': [
            'json = contemplate.parser.json:JSONParser',
            'env = contemplate.parser.env:EnvParser',
        ],
        'contemplate_engine_v1': [
            'format = contemplate.engine.format:FormatEngine',
        ],
    },
)
