from setuptools import setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django_box',
    version='0.1.0',
    description='Django template fragment',
    license='BSD',
    author='HQM',
    author_email='hakim@detik.com',
    url='https://github.com/hqms/django-box.git',
    keywords="django, django admin, template",
    packages=['django_box'],
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    install_requires=[
    ],
    classifiers=[
        'Framework :: Django',
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Widget Sets',
    ],
)

