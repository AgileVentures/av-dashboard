from setuptools import find_packages, setup

setup(
    name='av_dashboard',
    version='0.01',
    license='MIT',
    maintainer='Agile Ventures',
    maintainer_email='support@agileventures.org',
    description='An internal dashboard for Agile Ventures analytics',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
