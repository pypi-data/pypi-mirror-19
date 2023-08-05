"""
awsmc.server - server side commands
"""

import io
import os.path
import multiprocessing.pool
import time

import boto3
import paramiko
import screenutils

from awsmc.spigot import get_spigot, have_spigot
from awsmc.cli import register_command
from awsmc.cli import BaseCommand
from awsmc.exc import UserError

DIR = '/home/ubuntu/minecraft'
NAME = 'server'
CMD = 'java -Xms512M -Xmx1G -XX:+UseConcMarkSweepGC -jar spigot-1.11.2.jar'
_EC2 = None


def EC2():
    global _EC2
    if not _EC2:
        _EC2 = boto3.resource('ec2')
    return _EC2


def tag(resources, server=None):
    tags = [
        {'Key': 'Project', 'Value': 'Minecraft'},
    ]
    if server:
        tags.append({'Key': 'Server', 'Value': server})
    EC2().create_tags(
        Resources=resources,
        Tags=tags,
    )

def tag_filter(server=None):
    kwargs = {
        'Filters': [
            {'Name': 'tag:Project', 'Values': ['Minecraft']}
        ]
    }
    if server:
        kwargs['Filters'].append({'Name': 'tag:Server', 'Values': [server]})
    return kwargs


def get_instance_by_name(name):
    return list(EC2().instances.filter(**tag_filter(name)))[0]


class Ec2Server:
    """
    Provides convenience functions for managing and connecting to EC2 servers.

    This class can use the AWS API to create and delete EC2 instances, and it
    also uses the API along with paramiko to run commands remotely on it. It
    manages EC2 instances by tagging them with Project: Minecraft and Server:
    <name>, where <name> is a user-supplied name. This is useful because all
    other Minecraft-related resources will be similarly tagged, so you can see
    them all in a single resource group.
    """

    @classmethod
    def _get_security_group(cls):
        """
        Gets the security group resource that is used for all instances.

        If it exists, returns the existing one. If not, creates one. The rules
        are such that SSH and the minecraft port are accessible from the whole
        world.
        """
        try:
            return list(EC2().security_groups.filter(GroupNames=['minecraft']))[0]
        except:
            print('You do not have a minecraft security group. Creating one...')
            group = EC2().create_security_group(
                #DryRun=True,
                GroupName='minecraft',
                Description='allows SSH and minecraft from any host',
            )
            group.authorize_ingress(
                IpPermissions=[
                    dict(
                        IpProtocol='tcp',
                        FromPort=22,
                        ToPort=22,
                        IpRanges=[
                            dict(
                                CidrIp='0.0.0.0/0',
                            ),
                        ],
                    ),
                    dict(
                        IpProtocol='tcp',
                        FromPort=25565,
                        ToPort=25565,
                        IpRanges=[
                            dict(
                                CidrIp='0.0.0.0/0',
                            ),
                        ],
                    ),
                ],
            )
            tag([group.id])
            return group

    @classmethod
    def create(cls, name):
        """
        Create a new instance with a given server name.

        This will create any auxiliary resources (EBS volumes, security groups,
        etc) as needed.
        """
        # TODO: check that no instances exist with given name
        group = cls._get_security_group()
        print('Creating EC2 instance...')
        instance = EC2().create_instances(
            ImageId='ami-e13739f6',
            MinCount=1,
            MaxCount=1,
            KeyName='ctf',
            SecurityGroupIds=[
                group.id,
            ],
            InstanceType='t2.micro',
            Placement=dict(
                AvailabilityZone='us-east-1b',
            ),
        )[0]
        tag([instance.id], server=name)
        return Ec2Server(instance=instance)

    def __init__(self, id=None, instance=None, name=None):
        if name:
            self.instance = get_instance_by_name(name)
        elif instance:
            self.instance = instance
        else:
            self.instance = EC2().Instance(id=id)
        self._client = None

    def initialize(self, server_jar):
        self.wait_until_ready()
        print('Updating package databases...')
        self.run('sudo apt update')
        print('Upgrading packages...')
        self.run('sudo apt upgrade -y')
        print('Installing Java and Pip...')
        self.run('sudo apt install -y --no-install-recommends '
                 'default-jre python3-pip python3-setuptools')
        print('Installing awsmc...')
        self.run('sudo pip3 install awsmc')
        self.run('mkdir $HOME/minecraft')
        print('Copying server jar...')
        remote = os.path.join('/home/ubuntu/minecraft',
                              os.path.basename(server_jar))
        self.put(server_jar, remote)

    def wait_until_ready(self):
        print('Waiting until the instance is running...')
        self.instance.wait_until_running()
        print('Waiting until the instance status is ok...')
        ec2 = boto3.client('ec2')
        status_waiter = ec2.get_waiter('instance_status_ok')
        status_waiter.wait(InstanceIds=[self.instance.id])

    @property
    def hostname(self):
        # When setting up, the DNS name usually hasn't propagated by the time
        # we want to connect, so we use the IP address instead.
        return self.instance.public_ip_address

    @property
    def username(self):
        # AWS won't give us the username to ssh into, so we'll just make it
        # hardcoded for now
        return 'ubuntu'

    @property
    def key_file(self):
        return '/home/stephen/.ssh/ctf.pem'

    @property
    def client(self):
        if self._client:
            return self._client

        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(self.hostname, username=self.username,
                             key_filename=self.key_file)
        return self._client

    def _read_thread(self, channel):
        total = io.BytesIO()
        output = channel.recv(4096)
        while output:
            total.write(output)
            output = channel.recv(4096)
        return total.getvalue()

    def run(self, command, shell=False):
        channel = self.client.get_transport().open_session()
        channel.set_combine_stderr(True)
        if shell:
            channel.invoke_shell()
            channel.sendall(command + '\n')
        else:
            channel.exec_command(command=command)
        return self._read_thread(channel)

    def put(self, local, remote):
        sftp = self.client.open_sftp()
        sftp.put(local, remote)
        sftp.close()


def _get_screen():
    s = screenutils.Screen(NAME)
    return s


def _get_existing_screen():
    s = _get_screen()
    if not s.exists:
        raise UserError('The server is not running.')
    s.enable_logs()  # to ensure that the logs generator is set up
    return s


def _get_output(screen, command):
    next(screen.logs)
    screen.send_commands(command)
    output = ''
    while not output.endswith('\n>'):
        time.sleep(0.03)
        output += next(screen.logs)
    output = output[:-2]  # trim newline and prompt
    if output.startswith(command):
        output = output[len(command)+1:]
    return output


def start_server():
    s = _get_screen()
    s.initialize()
    s.send_commands('bash')
    s.send_commands('cd ' + DIR)
    s.enable_logs()
    s._screen_commands('logfile flush 0')
    s.send_commands(CMD)


def say(message):
    screen = _get_existing_screen()
    screen.send_commands('say ' + message)


def list_players():
    return _get_output(_get_existing_screen(), 'list')


@register_command
class ServerStartCommand(BaseCommand):

    def name(self):
        return 'server_start'

    def execute(self, args):
        start_server()


@register_command
class ServerListCommand(BaseCommand):

    def name(self):
        return 'server_list'

    def execute(self, args):
        print(list_players())
        print('hi')


@register_command
class ServerSayCommand(BaseCommand):

    def name(self):
        return 'server_say'

    def arguments(self, parser):
        parser.add_argument('message', type=str, nargs='+')

    def execute(self, args):
        say(args.message)


@register_command
class InitCommand(BaseCommand):

    def name(self):
        return 'init'

    def arguments(self, parser):
        parser.add_argument('name', type=str, help='name of the server')
        parser.add_argument('--version', type=str, default='1.11.2',
                            help='spigot jar version')

    def execute(self, args):
        name = args.name
        jar = have_spigot(args.version)
        if not jar:
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(get_spigot, (args.version,))
        server = Ec2Server.create(name)
        if not jar:
            jar = async_result.get()
        server.initialize(jar)

@register_command
class StartCommand(BaseCommand):

    def name(self):
        return 'start'

    def arguments(self, parser):
        parser.add_argument('name', type=str, help='name of the server')

    def execute(self, args):
        server = Ec2Server(name=args.name)
        print(server.run('awsmc server_start').decode('ascii'))
