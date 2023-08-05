from setuptools import setup, find_packages

setup(
    name='relevancer',
    version='0.1.0a1',
    description='Relevancer aims at identifying relevant content in social media streams. Text mining is the main approach.',
    long_description=open('README.md').read(),
    url='https://bitbucket.org/hurrial/relevancerml',
    author='Ali Hürriyetoğlu',
    author_email='ali.hurriyetoglu@gmail.com',
    license='GPL',
    keywords='machine-learning text-mining clustering k-means',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    py_modules=['relevancer'],
    install_requires=[
        'scikit-learn',
        'scipy',
        'pandas',
    ],
)
