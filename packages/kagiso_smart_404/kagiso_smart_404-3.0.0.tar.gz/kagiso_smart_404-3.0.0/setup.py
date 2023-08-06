from setuptools import find_packages, setup


setup(
    name='kagiso_smart_404',
    version='3.0.0',
    author='Kagiso Media',
    author_email='development@kagiso.io',
    description='Kagiso Smart 404',
    url='https://github.com/Kagiso-Future-Media/kagiso_smart_404',
    packages=find_packages(),
    install_requires=[
        'wagtail>=1.8.0',
    ]
)
