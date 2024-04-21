import json
import time

import paramiko
from loguru import logger

from ssh_exec_commands.resource_path import resource_path
from ssh_exec_commands.types import CommandInfo, Config


def connect_ssh(config: Config):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        logger.info(config.ip_address, config.username)
        private_key = None
        if config.private_key:
            private_key = paramiko.Ed25519Key.from_private_key_file(
                resource_path(config.private_key).as_posix(), config.passphrase
            )
        client.connect(
            config.ip_address, username=config.username, pkey=private_key, timeout=10
        )

        transport = client.get_transport()
        if not transport:
            return
        channel = transport.open_session(timeout=10)

        # Execute a command on the remote server
        for command_info in config.command_list:
            execute_commands(channel, command_info)

        channel.close()
        logger.info(f"Exit from {config.ip_address}.")

    except Exception as e:
        logger.trace(e)
    finally:
        client.close()


def execute_commands(channel: paramiko.Channel, command_info: CommandInfo):
    logger.info(f"Command(timeout:{command_info.timeout}): {command_info.command}")
    try:
        channel.exec_command(command_info.command)
        RECV_SIZE = 1024 * 32
        stdout_data = b""
        stderr_data = b""

        start_time = time.time()

        # Wait for the commands to complete
        while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
            stdout_data += channel.recv(RECV_SIZE)
            stderr_data += channel.recv_stderr(RECV_SIZE)

            elapsed_time = time.time() - start_time
            if elapsed_time >= command_info.timeout:
                logger.warning(
                    f"Timeout occurred ({command_info.timeout}s). Exiting the loop."
                )
                break

        if stdout_data:
            logger.info(stdout_data)
        if stderr_data:
            logger.info(stderr_data)
    except Exception as e:
        logger.trace("e")
