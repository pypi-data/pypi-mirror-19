from distutils.core import setup

setup(
    name='unebus',
    version='0.1.1',
    description='API for bus GPS in Hermosillo, Sonora.',
    author='Gamaliel Espinoza Macedo',
    author_email='gamaliel.espinoza@gmail.com',
    url='https://github.com/gamikun/unebus-python',
    packages=['unebus'],
    install_requires=['requests'],
    keywords=['bus', 'sonora', 'api']
)
