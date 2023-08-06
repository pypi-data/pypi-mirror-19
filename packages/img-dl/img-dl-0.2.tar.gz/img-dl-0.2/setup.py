from setuptools import setup

setup(
    name='img-dl',
    version='0.2',
    description='CLI to download images',
    author='Ganessh Kumar R P',
    author_email='rpganesshkumar@gmail.com',
    url='https://github.com/ganesshkumar/imgdl',
    download_url='https://github.com/ganesshkumar/imgdl/tarball/0.2',
    keywords=['image', 'downloader', 'imgur', 'image download'],
    py_modules=['imgdl'],
    install_requires=[
        'click',
        'validators',
        'beautifulsoup4',
        'imgurpython'
    ],
    entry_points='''
        [console_scripts]
        img-dl=imgdl:imgdl
    '''
)
