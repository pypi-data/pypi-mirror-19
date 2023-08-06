from setuptools import setup
import behave_web_api_extended

install_requires = [
    'behave>=1.2.4',
    'behave-web-api==1.0.6',
    'bottle==0.12.9',
    'freezegun>=0.3.8',
    'ordereddict==1.1',
    'nose==1.3.7',
    'requests>=2.0.0'
]


setup(
    name='behave-web-api-extended',
    version=behave_web_api_extended.__version__,
    packages=['behave_web_api_extended', 'behave_web_api_extended.steps'],
    setup_requires=['wheel'],
    install_requires=install_requires,
    description="Provides testing for JSON APIs with Behave",
    author='Victor Anjos',
    author_email='va@deeplearni.ng',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ]
)

#  url='behave-web-api-extended',
