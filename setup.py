from setuptools import setup

setup(
    name = "CLI",
    version = '2.0.0',
    python_requires = '==3.6.9',
    url='https://github.com/Kosia2000/CLI-Click',
    py_modules = ['click_app'],
    install_requires=[
        'click==7.1.2',
    ],
    entry_points = '''
        [console_scripts]
        click_app=click_app:cli
    ''',
)
