from distutils.core import setup

# WARNING: don't edit this file it is generated from the setup.txt
# within the scripts/ directory - changes made to this file will be lost!

setup(
    name = 'electric',
    packages = ['electric', 'electric.icharger'],
    version = "0.7.1",
    description = "Battery charger integration, information and notification server",
    author = "John Clayton",
    author_email = "electric_charge@icloud.com",
    url = 'https://github.com/johncclayton/electric',
    download_url = 'https://github.com/johncclayton/electric/tarball/0.7.1',
    keywords = [ 'icharger', 'fma', 'hobby', 'charger' ],
    license = "GPLv3",
    classifiers = [
    ],
    install_requires = [
        
            'aniso8601==1.2.0',
        
            'argh==0.26.2',
        
            'arrow==0.10.0',
        
            'astroid==1.4.9',
        
            'backports.functools-lru-cache==1.3',
        
            'click==6.6',
        
            'configparser==3.5.0',
        
            'Flask==0.12',
        
            'Flask-Cors==3.0.2',
        
            'Flask-RESTful==0.3.5',
        
            'gunicorn==19.6.0',
        
            'hidapi==0.7.99.post20',
        
            'isort==4.2.5',
        
            'itsdangerous==0.24',
        
            'Jinja2==2.8',
        
            'lazy-object-proxy==1.2.2',
        
            'MarkupSafe==0.23',
        
            'mccabe==0.5.3',
        
            'modbus-tk==0.5.4',
        
            'pathtools==0.1.2',
        
            'pylint==1.6.4',
        
            'python-dateutil==2.6.0',
        
            'pytz==2016.10',
        
            'PyYAML==3.12',
        
            'schematics==1.1.1',
        
            'six==1.10.0',
        
            'watchdog==0.8.3',
        
            'Werkzeug==0.11.13',
        
            'wrapt==1.10.8',
        
    ],
    entry_points = {
        'console_scripts': ['electric-server=electric.main:run_server']
    }
)