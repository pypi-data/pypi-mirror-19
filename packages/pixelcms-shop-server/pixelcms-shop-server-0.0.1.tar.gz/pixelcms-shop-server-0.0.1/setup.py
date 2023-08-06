from setuptools import setup, find_packages


setup(
    name='pixelcms-shop-server',
    version='0.0.1',
    description='Server part of ecommerce module for PixelCMS.',
    author='Michał Werner',
    author_email='michal@hurtowniapixeli.pl',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pixelcms-server>=0.4.0,<1',
        'django-mptt>=0.8.6,<1',
        'hashids>=1.1.0,<2',
        'django-ipware>=1.1.6,<2',
        'django-nested-admin>=3.0.12,<4'
    ]
)
