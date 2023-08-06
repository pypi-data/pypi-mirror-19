from setuptools import setup

setup(
      name="ram-pack",
      version="0.0.1",
      description="A sample python package",
      long_description = '''it has sum of digits method''',
      author="Ramya",
      author_email="munja.ramya@gmail.com",
      maintainer="ramya",
      maintainer_email="munja.ramya@gmail.com",
      url=" http://pypi.python.org/pypi/ram-pack",
      download_url=" http://pypi.python.org/pypi/ram-pack/ram-pack-0.0.1.tar.gz",
      packages=["package"],
      package_dir={"package":""},
      py_modules=["package/sod"],
      classifiers=[ 
       "Programming Language :: Python",
       "Natural Language :: English",
       "Operating System :: Microsoft :: Windows",
       "Intended Audience :: Developers"],
      keywords="sum",
      license="freeware"

)
