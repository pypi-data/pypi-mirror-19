from setuptools import setup

setup(
    name = 'magicstr',
    packages = ['magicstr'],
    discription = 'Do some magic on your strings files.',
    version = '1.69',
    author = 'wombatwen',
    author_email = 'wombatwen@gmail.com',
    install_require = [
        'gspread', 
        'lxml',
        'oauth2client'    
    ],
    scripts = ['magicstr/magicstr']
)
