from setuptools import setup
from subprocess import Popen, PIPE


def call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip().decode('ascii')
    except:
        # !! DANGER DANGER !!
        # This is the release version. Will be returned if running setup outside Git repo.
        # If you bump this, also add a tag to git with the same number:
        # e.g.: git tag -a 0.3
        # !! DANGER DANGER !!
        return '0.2'


def pep386adapt(version):
    if version is not None and '-' in version:
        # adapt git-describe version to be in line with PEP 386
        parts = version.split('-')
        parts[-2] = 'rc'+parts[-2]
        version = ''.join(parts[:-1])
    return version


setup(
    name='azuremlcli',
    version=pep386adapt(call_git_describe(4)),
    description='Microsoft Azure Machine Learning Command Line Tools',
    url='https://github.com/Azure/amlbdcli',
    author='Microsoft',
    author_email='azureml@microsoft.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
    packages=[
        'azuremlcli'
    ],
    package_data={
        '':['data/*.json', 'data/preamble', 'data/sample.*', 'data/example_app.py', 'data/getsample.py']
    },
    install_requires=[
        'azure-cli>=0.1.0b11',
        'azure-storage>=0.33',
        'tabulate>=0.7.7',
        'future',
    ],
    scripts=[
        'aml',
        'aml.bat'
    ],
    zip_safe=False
)
