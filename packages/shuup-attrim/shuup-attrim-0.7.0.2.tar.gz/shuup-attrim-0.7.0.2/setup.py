import os
from importlib.util import find_spec

import pip
import setuptools


def main():
    setuptools.setup(
        name='shuup-attrim',
        version=_get_version_from_hgtags_file(),
        description='Multi-value attributes addon for Shuup E-Commerce Platform',
        url='https://gitlab.com/nilit/shuup-attrim',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Framework :: Django :: 1.9',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Office/Business',
        ],
        keywords=['shuup', 'attributes'],
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={'shuup.addon': 'attrim=attrim'},
        cmdclass=_get_commands(),
        install_requires=[
            'shuup >= 1, < 2',
            'psycopg2 >= 2.6.2, < 3',
            'shuup-dev-testutils >= 0.1, < 0.2',
            _shuup_dev_utils_version,
        ],
    )


_shuup_dev_utils_version = 'shuup-dev-utils >= 0.2, < 0.3'


def _get_version_from_hgtags_file() -> str:
    pip.main(['install', _shuup_dev_utils_version])
    
    from shuup_dev_utils.setuptools.versions import get_version_from_hgtags_file
    package_dir_path = os.path.dirname(os.path.abspath(__file__))
    version = get_version_from_hgtags_file(hgtags_dir_path=package_dir_path)
    
    return version


def _get_commands() -> dict:
    is_shuup_installed = find_spec('shuup') is not None
    is_shuup_dev_utils_installed = find_spec('shuup_dev_utils') is not None
    if is_shuup_installed and is_shuup_dev_utils_installed:
        import shuup_setup_utils
        from shuup_dev_utils.setuptools.commands import build_static
        
        shuup_commands = shuup_setup_utils.COMMANDS
        project_commands = {'build_static': build_static}
        return {**shuup_commands, **project_commands}
    else:
        return {}


if __name__ == '__main__':
    main()
