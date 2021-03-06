from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='thresholdclustering',
    version='1.01',
    description='Community detection for directed, weighted networkX graphs with spectral thresholding.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Ingo Marquart',
    author_email='ingo.marquart@esmt.org',
    keywords=['community detection','clustering','networkx','python-louvain'],
    url='https://github.com/IngoMarquart/python-threshold-clustering',
    download_url='https://pypi.org/project/thresholdclustering'
)

install_requires = [
    'numpy',
    'networkx'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)