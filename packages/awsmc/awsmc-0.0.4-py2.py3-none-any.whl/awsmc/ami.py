"""
awsmc.ami - manage Amazon Machine Image for minecraft
"""

import boto3


def create_instance():
    c = boto3.client('ec2')
