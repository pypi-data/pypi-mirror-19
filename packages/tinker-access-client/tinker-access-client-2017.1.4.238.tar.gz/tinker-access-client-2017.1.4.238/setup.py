from setuptools import setup
from setuptools.command.install import install as _install

from tinker_access_client.ServiceInstaller import ServiceInstaller
from tinker_access_client.PackageInfo import PackageInfo



class install(_install):
    def run(self):
        _install.run(self)
        msg = "\nInstalling {0} service...".format(PackageInfo.python_package_name)

        # TODO: maybe change this to just use subprocess call in a loop['tinker-access-client install-service', etc..]
        self.execute(ServiceInstaller.install, (self.install_lib,), msg=msg)


config = {
    'name': PackageInfo.pip_package_name,
    'description': PackageInfo.pip_package_name,
    'author': 'Erick McQueen',
    'url': 'http://github.com/tinkerMill/tinkerAccess',
    'download_url': 'https://github.com/tinkerAccess/archive/v{0}.tar.gz'.format(PackageInfo.version),
    'author_email': 'ronn.mcqueen@tinkermill.org',
    'version': PackageInfo.version,
    'zip_safe': False,
    'include_package_data': True,
    'package_data': {
        PackageInfo.python_package_name: [
            'scripts/*'
        ]
    },
    'install_requires': [
        'daemonize==2.4.7',
        'pyserial==3.2.1',
        'requests==2.12.4'
    ],
    'packages': [
        PackageInfo.python_package_name
    ],
    'test_suite': 'nose.collector',
    'tests_require': [
        'daemonize==2.4.7',
        'pyserial==3.2.1',
        'requests==2.12.4',
        'mock==2.0.0',
        'nose==1.3.7'
    ],
    'entry_points': {
        'console_scripts': [
            '{0}={1}.CommandLineSupport:run'.format(PackageInfo.pip_package_name, PackageInfo.python_package_name)
        ]
    },
    'cmdclass': {
        'install': install
    }
}

setup(**config)
