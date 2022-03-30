from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

# Parse dependencies
with open('requirements.txt','r') as f:
    install_requires = [ s.replace('\n','') for s in f.readlines() ]
    # Fix syntax for packages that are directly install from GitHub
    for i, req in enumerate(install_requires):
        if req[0:3] == 'git':
            package_name = req.split('/')[-1].split('.')[0].lower()
            # Replace command
            install_requires[i] = f"{package_name} @ {req}"
        if 'en_core_web_sm' in req:
            install_requires[i] = f"en_core_web_sm @ {req}"

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        post_install_commands()
        develop.run(self)

class PostInstallCommand(install):
    """ Post-installation commands for install mode. """
    def run(self):
        post_install_commands()
        install.run(self)

def post_install_commands():
    """ Run post install commands"""
    # Sentencepiece is dependency of gramformer,
    # but causes issues with transformers
    check_call("pip uninstall -y sentencepiece", shell=True)
    # Download the spacy corpus
    check_call("python -m spacy download en", shell=True)
        


setup(name='chatbot',
      version = '0.1.0',
      license='MIT',
      author='Aloïs Villa, Frank Schlosser',
      description='A language learning chatbot',
      url='https://github.com/franksh/chatbot',
      packages=find_packages(),
      install_requires=install_requires,
      python_requires='>=3.9',
      dependency_links=[
      ],
      project_urls={
          'Contributing Statement': 'https://github.com/franksh/chatbot/blob/master/CONTRIBUTING.md',
          'Bug Reports': 'https://github.com/franksh/chatbot/issues',
          'Source': 'https://github.com/franksh/chatbot/',
      },
      include_package_data=True,
      zip_safe=False,
        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },
  )
