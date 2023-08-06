from setuptools import setup

setup(name='ArvadsFit',
      version='0.8',
      description='A custom wrapper of IMinuit',
      url='https://github.com/Arvad/ArvadsFit',
      author='Asbjorn Arvad Jorgensen',
      author_email='Arvad91@gmail.com',
      license='MIT',
      packages=['ArvadsFit'],
      install_requires=[
                        'numpy',
                        'iminuit',
                        'probfit'],
      zip_safe=False)