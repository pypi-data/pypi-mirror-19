from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
synapse=glue_synapse.cluster:setup
"""
package_data = {'glue_synapse': ['*.ui']}

setup(name='glue-synapse',
      version='0.4',
      description='Synapse localization clustering and analysis for Glue. Uses DBSCAN clustering algorithm to group channels and display centroid distances.',
      url='http://thesettleproject.com',
      author='Brett Settle',
      author_email='brettjsettle@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_data=package_data,
      install_requires=['pyopengl', 'glueviz>=0.9', 'glue-vispy-viewers'],
      entry_points=entry_points)
