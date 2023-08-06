""" Register on PyPI """
import io
from setuptools import setup

with io.open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='ms-cognitive-speaker-recognition',
    packages=['cognitive_sr'],
    version='0.1',
    description='API client for Microsoft Cognitive Services (Speaker Recognition)',
    long_description=readme,
    author='Rob Ladbrook',
    author_email='mscognitive@slyfx.com',
    url='https://github.com/robladbrook/ms-cognitive-speaker-recognition',
    download_url='https://github.com/robladbrook/ms-cognitive-speaker-recognition/tarball/0.1',
    keywords=['speaker', 'voice', 'microsoft', 'recognition', 'cognitive'],
    license='MIT',
    install_requires=['requests'],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    )
)
