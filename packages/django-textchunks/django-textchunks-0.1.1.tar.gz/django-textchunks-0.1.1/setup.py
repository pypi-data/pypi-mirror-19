from setuptools import setup, find_packages

setup(
    name='django-textchunks',
    version='0.1.1',
    description='Keyed blocks of text or html content for use in your Django templates',
    keywords="django text chunks templates",
    author='Aleksey Osadchuk',
    author_email='osdalex@gmail.com',
    url='https://github.com/aleosd/django-textchukns',
    maintainer='aleosd',
    maintainer_email='osdalex@gmail.com',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities'
    ],
)
