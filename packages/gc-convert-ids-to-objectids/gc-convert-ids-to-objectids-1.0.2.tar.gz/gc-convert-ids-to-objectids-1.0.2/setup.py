from setuptools import setup, Extension

setup(
    name='gc-convert-ids-to-objectids',
    version='1.0.2',
    author='Alex Etling',
    author_email='alex@gc.com',
    packages=['convert_ids'],
    package_dir={'': '.'},
    zip_safe=False,
    url='https://github.com/gamechanger/gc-convert-ids',
    ext_modules = [Extension("convert_ids/convert_ids_to_objectids", ["convert_ids/convert_ids_to_objectids.c"])]
)