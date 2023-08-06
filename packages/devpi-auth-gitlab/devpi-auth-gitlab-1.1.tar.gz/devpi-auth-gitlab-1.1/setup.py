from setuptools import setup, find_packages


setup(
    name="devpi-auth-gitlab",
    description="An authentication plugin for use with gitlab-ci, utilising the build in registry token authentication scheme",
    version='1.1',
    author="Andrew Leech",
    author_email="andrew.leech@planetinnovation.com.au",
    url="https://gitlab.spring.localnet/anl/devpi-gitlab-auth",
    keywords="devpi plugin",
    entry_points={
        'devpi_server': [
            "devpi-auth-gitlab = devpi_auth_gitlab.main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'requests',
        'devpi-server>=2.0.0',
    ]
)
