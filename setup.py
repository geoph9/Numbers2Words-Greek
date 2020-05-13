from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='num2word',
    version='0.1',
    author='George Karakasidis',
    license='MIT',
    packages=find_packages(),
    description='Number to Word conversion for the Greek Language.',
    long_description=long_description,
    url='https://github.com/geoph9/Numbers2Words-Greek',
    keywords=['digit to word', 'numbers-to-words', 'number to words greek',
              'digit to word greek', 'convert digits to words in greek',
              'convert numbers to words'
              ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6+',
        'Topic :: Scientific/Engineering',
    ],
    include_package_data=True
)