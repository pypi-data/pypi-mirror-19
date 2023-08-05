"""
awsmc.util - utilities for awsmc
"""

import contextlib

import paramiko

HOST = 'ec2-52-90-187-150.compute-1.amazonaws.com'
USER = 'ubuntu'
ID = '/home/stephen/.ssh/ctf.pem'


@contextlib.contextmanager
def shell():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, key_filename=ID)
    channel = client.invoke_shell()
    channel.set_combine_stderr(True)
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')
    yield stdin, stdout
    channel.close()
    client.close()


def remote_cmd(command):
    with shell() as (stdin, stdout):
        stdin.write(command + b'; exit')
        return stdout.read()
