from setuptools import setup, find_packages

setup(
    name='minibase',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
      'sqlite3',
      'os'
    ],
    author='Samuel DeSantis',
    author_email='minibase.py@gmail.com',
    description='A simple SQLite database wrapper.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Samuel-DeSantis/minibase',
    classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.6',
)