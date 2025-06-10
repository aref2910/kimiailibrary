from setuptools import setup, find_packages

setup(
    name='kimiai',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pillow',
        'pydub'
    ],
    author='Your Name',
    description='کتابخانه تحلیل سیگنال صوتی با رسم و محاسبه انرژی و توان',
    url='https://github.com/YourUsername/kimiai',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)