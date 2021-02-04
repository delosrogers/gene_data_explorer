from setuptools import setup

setup(
    name='gene_data_explorer',
    packages=['gene_data_explorer'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask',
        'mysql-connector-python',
        'pandas',
        'configparser',
        'flask-sqlalchemy',
        'mysqlclient'
    ],
)