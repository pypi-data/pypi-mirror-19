from distutils.core import setup, Extension

module1 = Extension('ciputils', sources = ['cipher-utils/ciputils.c'])

setup(name='cipher-utils',
      version='1.0',
      description='CRC checker and fast hex2int',
      url='https://github.com/AkhilNairAmey/cipherutils',
      author='Akhil Nair',
      author_email='akhil.nair@amey.co.uk',
      license='MIT',
      packages=['cipher-utils'],
      ext_modules = [module1])
