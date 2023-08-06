from setuptools import setup, find_packages

setup(
    name = 'dictplus',
    version = '0.0.1',
    keywords = ('enhanced dictionary'),
    description = 'enhanced dictionary',
    license = 'MIT License',
    install_requires = ['pandas'],
    include_package_data=True,
    zip_safe=True,

    author = 'cchen224',
    author_email = 'phantomkidding@gmail.com',

    url = 'https://github.com/PhantomKidding',

    packages = find_packages(),
    platforms = 'any',
)