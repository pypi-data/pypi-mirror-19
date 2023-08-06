from setuptools import setup

setup(
    name="tickler",
    version="1.0.2a",
    description="A scriptable CLI utility and support library for 'tickler' style file trees",
    long_description="Tickler can be used to create a tickler directory structure automatically on the filesystem. It provides a utility function for building tickler compatible file paths from a standard datetime object. This function can also be accessed for scripting purposes by using the --get-path argument and passing a dateutil compatible date string.",
    url="https://github.com/wkmanire/tickler",
    author="William Kevin Manire",
    author_email="williamkmanire@gmail.com",
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # audience
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',

        # topics
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',        

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords="tickle tickler cli filesystem week number iso date",
    install_requires=["python-dateutil==2.6.0",
                      "isoweek==1.3.3"],
    entry_points={
    'console_scripts': [
        'tickler=tickler:main',
    ]},
    py_modules=["tickler"],
    data_files = [("", ["LICENSE"])])
