from setuptools import setup

setup(
    name = 'magicstr',
    packages = ['magicstr'],
    package_data = {'magicstr': ['config']},
    discription = 'Do some magic on your strings files.',
    version = '1.76',
    author = 'wombatwen',
    author_email = 'wombatwen@gmail.com',
    install_requires = [
        'gspread', 
        'lxml',
        'oauth2client'    
    ],
    scripts = ['magicstr/magicstr']
)
