from setuptools import setup

setup(
    author = 'Łukasz Żarnowiecki',
    author_email = 'lukasz.z@nfdi.me',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],
    description = 'Wrapper around localytics API',
    download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1',
    install_requires = [
        'requests>=2.11.1'
    ],
    keywords = ['lib', 'library', 'localytics', 'wrapper', 'http'],
    license = 'MIT',
    name = 'localyticspy',
    packages = ['localytics'],
    url = 'https://github.com/nfdi/localyticspy',
    version = '0.1-alpha1'
)
