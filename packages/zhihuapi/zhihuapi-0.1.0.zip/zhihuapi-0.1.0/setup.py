from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='zhihuapi',
    version='0.1.0',
    description='Unofficial API for zhihu.',
    long_description=readme,
    url='https://github.com/syaning/zhihuapi-py',
    author='Alex Sun',
    author_email='syaningv@gmail.com',
    license='MIT',
    packages=['zhihuapi'],
    zip_safe=False,
    install_requires=['requests', 'pyquery'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='zhihuapi zhihu api crawler spider'
)
