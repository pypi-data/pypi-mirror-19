"""
Build (locally) the spigot server for copying onto an AWS instance.
"""

import os
import os.path
import glob
import shutil
import subprocess
import tempfile

import requests

from awsmc.cli import BaseCommand, register_command

BUILD_TOOLS = r'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar'
DIRECTORY = os.path.expanduser('~/.awsmc')

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)


def get_build_tools_jar_path():
    return os.path.join(DIRECTORY, 'BuildTools.jar')


def get_build_tools():
    path = get_build_tools_jar_path()
    if os.path.exists(path):
        return path
    with open(path, 'wb') as handle:
        response = requests.get(BUILD_TOOLS, stream=True)
        for chunk in response.iter_content(chunk_size=4096):
            handle.write(chunk)
    return path


def have_spigot(rev='latest'):
    if rev == 'latest':
        return None
    existing_spigot = os.path.join(DIRECTORY, 'spigot-%s.jar' % rev)
    if os.path.exists(existing_spigot):
        return existing_spigot
    return None


def build_spigot(rev='latest'):
    jar = get_build_tools()
    work = tempfile.mkdtemp()
    print('WORKING IN ' + work)
    subprocess.check_output(['java', '-jar', jar, '--rev', rev], cwd=work)
    spigot = glob.glob(os.path.join(work, 'spigot-*.jar'))[0]
    spigot_basename = os.path.basename(spigot)
    spigot_destination = os.path.join(DIRECTORY, spigot_basename)
    shutil.copyfile(spigot, spigot_destination)
    shutil.rmtree(work)
    return spigot_destination


def get_spigot(rev='latest'):
    existing = have_spigot(rev)
    if existing:
        return existing
    return build_spigot(rev)


@register_command
class BuildSpigotCommand(BaseCommand):

    def name(self):
        return 'build_spigot'

    def arguments(self, parser):
        parser.add_argument('--version', type=str, default='latest',
                            help='Spigot version to build')

    def execute(self, args):
        path = get_spigot(args.version)
        print('Spigot JAR is at: %s' % path)
