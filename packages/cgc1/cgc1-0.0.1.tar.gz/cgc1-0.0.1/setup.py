from setuptools import setup, find_packages
pkg = "cgc1"
ver = '0.0.1'
setup(name             = pkg,
      version          = ver,
      description      = "conveniently good containers",
      long_description = "lxc for the lazy",
      author           = "Eduard Christian Dumitrescu",
      author_email     = "eduard.c.dumitrescu@gmail.com",
      license          = "LGPLv3",
      url              = "https://hydra.ecd.space/f/cgc/",
      packages         = find_packages(),
      install_requires = [],
      package_data     = {pkg: ['conf/*.conf']},
      entry_points     = {
          'console_scripts': ['cgc1='+pkg+'.main:main']},
      classifiers      = ["Programming Language :: Python :: 3 :: Only"])
