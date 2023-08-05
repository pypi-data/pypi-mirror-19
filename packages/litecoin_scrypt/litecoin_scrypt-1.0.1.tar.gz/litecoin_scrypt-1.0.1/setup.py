from distutils.core import setup, Extension

litecoin_scrypt_module = Extension('litecoin_scrypt',
                               sources = ['litecoin_scrypt/scryptmodule.c',
                                          'litecoin_scrypt/scrypt.c'],
                               include_dirs=['./litecoin_scrypt/'])

setup (
    name = 'litecoin_scrypt',
    version = '1.0.1',
    description = 'Bindings for scrypt proof of work used by Litecoin',
    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    ext_modules = [litecoin_scrypt_module]
)
