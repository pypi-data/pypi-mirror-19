try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        name="distractinator",
        version='0.4',
        description="For use with the Distractinator USB receiver.",
        author="Joe Dougherty",
        author_email="joseph.dougherty@gmail.com",
        packages=['distractinator'],
        package_data = {'distractinator': ['examples/.distractinator.conf', 'examples/customevents.py']},
        install_requires=['pyserial>=3.1.1', 'six>=1.10.0'],
        entry_points={
            'console_scripts': ['distractd = distractinator:main'],
            },
        zip_safe=False,
        )

