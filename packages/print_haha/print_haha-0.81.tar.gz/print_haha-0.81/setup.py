from setuptools import setup

setup(
    name = 'print_haha',
    package = ['print_haha', 'print_haha/data'],
    package_data = {'print_haha.data': ['data_file.dat']},
    discription = 'Just a test.',
    version = '0.81',
    author = 'wombatwen',
    author_email = 'wombatwen@gmail.com',
    scripts = ['print_haha/print_haha'],
)
