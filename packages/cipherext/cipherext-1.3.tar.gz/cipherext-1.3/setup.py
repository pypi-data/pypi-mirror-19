from distutils.core import setup, Extension

module1 = Extension('ciputils', sources = ['cipherext/ciputils.c'])

setup(name='cipherext',
      version='1.3',
      description='CRC checker and fast hex2int',
      url='https://github.com/AkhilNairAmey/cipherutils',
      author='Akhil Nair',
      author_email='akhil.nair@amey.co.uk',
      license='MIT',
      packages=['cipherext'],
      ext_modules = [module1])
