from setuptools import setup, find_packages

setup(
    name='SafeScribe',
    version='1.0.0',
    author='Jorge Santos',
    author_email='jorgesmrc2023@example.com',
    description='A CLI tool to process PDFs for enhanced security by removing embedded URLs and action items.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/js4nt0s/safescribe',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rich',
        'pypdftk',
    ],
    entry_points={
        'console_scripts': [
            'safescribe = main:main',
        ],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)