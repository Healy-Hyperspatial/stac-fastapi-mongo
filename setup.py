"""stac_fastapi: mongodb module."""

from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    desc = f.read()

install_requires = [
    "stac-fastapi.core==2.4.1",
    "motor==3.3.2",
    "pymongo==4.6.2",
    "uvicorn",
    "starlette",
    "typing_extensions==4.8.0",
]

extra_reqs = {
    "dev": [
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "pre-commit",
        "requests",
        "ciso8601",
        "httpx",
    ],
    "docs": ["mkdocs", "mkdocs-material", "pdocs"],
    "server": ["uvicorn[standard]==0.19.0"],
}

setup(
    name="stac-fastapi.mongo",
    version="3.2.1",
    description="Mongodb stac-fastapi backend.",
    long_description=desc,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
    url="https://github.com/Healy-Hyperspatial/stac-fastapi-mongo",
    license="MIT",
    packages=find_namespace_packages(),
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extra_reqs,
    entry_points={"console_scripts": ["stac-fastapi-mongo=stac_fastapi.mongo.app:run"]},
)
