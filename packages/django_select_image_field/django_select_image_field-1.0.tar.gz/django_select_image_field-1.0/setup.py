from distutils.core import setup
setup(
  name = 'django_select_image_field',
  packages = ['django_select_image_field'], # this must be the same as the name above
  version = '1.0',
  description = 'A select-image field for django , using msdropdown(jquery)',
  author = 'Aleksandar Shaklev',
  author_email = 'saklevaleksandar@gmail.com',
  url = 'https://github.com/shaklev/django_select_image_field', # use the URL to the github repo
  download_url = 'https://github.com/shaklev/django_select_image_field/tarball/0.1', # I'll explain this in a second
  keywords = ['django', 'django-fields', 'django-forms','django-widgets'], # arbitrary keywords
  classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
