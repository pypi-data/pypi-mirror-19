from setuptools import setup

setup(
    name = 'my_print_haha_program',
    version = '0.4',
    author = 'wombatwen',
    author_email = 'wombatwen@gmail.com',
    scripts = ['src/print_haha'],
    data_files = [('data', ['src/data/data_file'])] 
)
