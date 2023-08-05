from setuptools import setup

setup(
    name = 'print_haha',
    package = ['print_haha'],
    package_data = {'print_haha': ['data_file']},
    discription = 'Just a test.',
    version = '0.2',
    author = 'wombatwen',
    author_email = 'wombatwen@gmail.com',
    scripts = ['print_haha/print_haha'],
)
