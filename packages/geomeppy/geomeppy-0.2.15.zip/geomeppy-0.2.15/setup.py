import os

from setuptools import setup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def read_md(f):
    try:
        from pypandoc import convert
        try:
            return convert(os.path.join(THIS_DIR, f), 'rst')
        except:
            return "GeomEppy"
    except ImportError:
        print("warning: pypandoc module not found, could not convert Markdown to RST")
        try:
            with open(os.path.join(THIS_DIR, f), 'r') as f_in:
                return f_in.read()
        except:
            return "GeomEppy"
    
setup(
    name='geomeppy',
    packages=['geomeppy',
              'tests',
              ],
    version='0.2.15',
    description='Geometry editing for E+ idf files',
    long_description=read_md('README.md'),
    author='Jamie Bull',
    author_email='jamie.bull@oco-carbon.com',
    url='https://github.com/jamiebull1/geomeppy',
    download_url='https://github.com/jamiebull1/geomeppy/tarball/v0.2.15',
    license='MIT License',
    keywords=['EnergyPlus', 
              'geometry',
              'building performance simulation',
              ],
    platforms='any',
    install_requires = [
        "eppy>=0.5.41",
        "numpy>=1.11.1",
        "six>=1.10.0",  # python2/3 compatibility
        "pyclipper>=1.0.2",  # geometry intersection
        "transforms3d>=0.3",  # geometry transformations
        "shapely>=1.5.17",  # geometry transformations
#        "matplotlib>=1.5.1",  # simple geometry viewer
        ],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        ],
)
