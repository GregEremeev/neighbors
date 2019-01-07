from setuptools import setup, find_packages


version = __import__('neighbors').__version__


INSTALL_REQUIRES = (
    'Django==1.10.8',
    'django-extra-fields==0.9',
    'djangorestframework==3.5.3',
    'psycopg2==2.6.2',
)


setup(
    name='neighbors',
    version=version,
    description='Test task neighbors',
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
)
