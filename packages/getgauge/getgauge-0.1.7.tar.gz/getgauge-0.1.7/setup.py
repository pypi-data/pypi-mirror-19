from distutils.core import setup

setup(
    name='getgauge',
    packages=['getgauge', 'getgauge/messages'],
    version='0.1.7',
    description='Enables Python support for Gauge',
    author='Kashish Munjal',
    author_email='kashishmunjal64@gmail.com',
    url='https://github.com/kashishm/gauge-python',
    download_url='https://github.com/kashishm/gauge-python/archive/v0.1.7.zip',
    keywords=['testing', 'gauge', 'gauge-python', 'getgauge', 'automation'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['protobuf==3.0.0b2.post2', 'redBaron', 'colorama'],
)
