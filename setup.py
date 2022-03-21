from setuptools import setup, find_packages

# Parse dependencies
with open('requirements.txt','r') as f:
    install_requires = [ s.replace('\n','') for s in f.readlines() ]
    # Fix syntax for packages that are directly install from GitHub
    for i, req in enumerate(install_requires):
        if req[0:3] == 'git':
            package_name = req.split('/')[-1].split('.')[0].lower()
            # Replace command
            install_requires[i] = f"{package_name} @ {req}"


setup(name='chatbot',
      version = '0.0.2',
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
  )