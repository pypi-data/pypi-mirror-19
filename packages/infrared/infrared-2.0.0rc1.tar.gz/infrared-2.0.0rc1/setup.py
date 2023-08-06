from setuptools import setup, find_packages
import platform
from pip import req

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = req.parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='infrared',
    version='2.0.0rc1',
    description='Drive Ansible projects from a nice CLI',
    url='http://infrared.readthedocs.io/en/ir2',
    license='GPLv3',
    keywords='ansible cli openstack',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "infrared = infrared.main:main",
            'ir = infrared.main:main'
        ]
    },
    # TODO(yfried): use this section to setup confg in ~/.infrared
    # data_files=['config', ],
    install_requires=reqs,
    author='Red Hat OpenStack Infrastructure Team',
    author_email='rhos-infrared@redhat.com'
)

if all(platform.linux_distribution(supported_dists="redhat")):
    print("Fixing selinux for redhat systems...")
    from infrared.core.utils.selinux_fix import copy_system_selinux
    copy_system_selinux()
