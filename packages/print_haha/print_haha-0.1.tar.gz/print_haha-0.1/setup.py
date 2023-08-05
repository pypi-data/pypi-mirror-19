from setuptools import setup

setup(
    name = 'print_haha',
    package = ['print_haha'],
    discription = 'Just a test.',
    version = '0.1',
    author = 'wombatwen',
    author_email = 'wombatwen@gmail.com',
    scripts = ['print_haha/print_haha'],
    data_files = [('src', ['data/data_file'])] 
)
