from setuptools import setup, find_packages

config = {
    "name": "vortex",
    "description": "Dependency Graph.",
    "author": "David Sparrow",
    "author_email": "dsparrow27@gmail.com",
    "url": "https://github.com/dsparrow27/vortex",
    "version": "0.0.1",
    "install_requires": [],
    "setup_requires": [],
    "packages": ["ds",
                 "ds.vortex",
                 "ds.vortex.core",
                 "ds.vortex.tests",
                 "ds.vortex.examples",
                 "ds.vortex.nodes",
                 "ds.vortex.nodes.array",
                 "ds.vortex.nodes.comparison",
                 "ds.vortex.nodes.constants",
                 "ds.vortex.nodes.conversion",
                 "ds.vortex.nodes.dict",
                 "ds.vortex.nodes.directories",
                 "ds.vortex.nodes.math",
                 "ds.vortex.nodes.math.basic",
                 "ds.vortex.nodes.math.trigonometry",
                 "ds.vortex.nodes.string",
                 "ds.vortex.utils"],
    "package_dir": {"": "src"},

    "scripts": []}


setup(**config)
