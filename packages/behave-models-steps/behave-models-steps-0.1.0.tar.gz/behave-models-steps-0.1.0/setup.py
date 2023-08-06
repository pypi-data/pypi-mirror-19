from setuptools import setup
import behave_models_steps

install_requires = [
    'behave>=1.2.4',
    'behave-web-api==1.0.6',
    'bottle==0.12.9',
    'Faker==0.7.3',
    'freezegun==0.3.8',
    'inflect==0.2.5',
    'inflection==0.3.1',
    'nose==1.3.7',
    'ordereddict==1.1',
    'requests>=2.0.0',
    'SQLAlchemy==1.0.15'
]


setup(
    name='behave-models-steps',
    version=behave_models_steps.__version__,
    packages=['behave_models_steps', 'behave_models_steps.steps'],
    setup_requires=['wheel'],
    install_requires=install_requires,
    description="Provides testing for Flask-SQLAlchemy models with Behave",
    author='Victor Anjos, Tristan Monger',
    author_email='va@deeplearni.ng',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)

