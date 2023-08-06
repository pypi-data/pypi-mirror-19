from setuptools import setup, find_packages, Extension

setup(
    name='KR580',
    version='0.0.1',
    description='KR580 educational emulator.',
    url='https://github.com/gsedometov/KR580-emulator',
    author='Georgii Sedometov',
    author_email='gs@sedometov.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],

    keywords='KR580 emulator assembler education',

    packages=find_packages(),
    install_requires=['multipledispatch', 'ply', 'PyQt5'],
    #data_files=[('', 'KR580/emulator/CPU.so')],
    package_data={'KR580': ['emulator/CPU.so']},

    entry_points={
        'gui_scripts': [
            'KR580=KR580.__main__:main']}
)
