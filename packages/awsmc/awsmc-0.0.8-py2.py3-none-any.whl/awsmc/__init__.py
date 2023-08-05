"""
AWS Minecraft hosting utilities.

This package/tool provides the ability to create and manage a Minecraft server
running on Amazon EC2. In particular, it allows for easily starting and
stopping server instances so that you can save on EC2 when there are no users
online.
"""

# this must come first
import awsmc.cli

import awsmc.ami
import awsmc.server
import awsmc.spigot
