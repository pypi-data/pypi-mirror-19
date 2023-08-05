from setuptools import setup

setup(
    name="docker-app",
    version="0.1.0",
    author="Diego A.",
    author_email="diego.acuna@mailbox.org",
    url="http://pypi.python.org/pypi/docker-app/",
    description="Ease your flow with docker-compose",
    license='MIT',
    # Dependent packages (distributions)
    install_requires=[
        "pyyaml",
    ],
    scripts=['bin/docker-app']
)