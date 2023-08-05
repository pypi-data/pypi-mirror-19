from setuptools import setup, find_packages

setup(
        name='easypkg',
        namespace_packages=['easypkg'],
        description='Easy downloader of private repositories.',
        author='Jota Junior',
        author_email='jotavrj@gmail.com',
        url='https://github.com/jotajunior/easypkg',
        download_url='https://github.com/jotajunior/easypkg/tarball/0.1.1',
        version='0.1.1',
        packages=find_packages('src'),
        install_requires=[
            'requests',
            ],
        package_dir={'': 'src'},
        entry_points={
            'console_scripts': [],
            },
        keywords=[
            'bitbucket',
            'github',
            'private',
            'repository',
            'download',
            'repo',
            ],
)
