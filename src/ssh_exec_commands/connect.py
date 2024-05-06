import time

import paramiko
import paramiko_expect
from loguru import logger

from ssh_exec_commands.resource_path import resource_path
from ssh_exec_commands.types import Config


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
            config.ip_address,
            username=config.username,
            pkey=private_key,
            timeout=config.timeout,
        )

        with paramiko_expect.SSHClientInteraction(
            client, timeout=config.timeout, display=False
        ) as interact:
            logger.info(f"expect: {config.prompt_pattern}")
            interact.expect(config.prompt_pattern)
            interact.send("")
            with resource_path("output.txt").open("a") as output_file:
                for command_info in config.command_list:
                    logger.info(f"execute: {command_info.command}")
                    interact.expect(config.prompt_pattern)
                    interact.send(command_info.command)
                    output_file.write(interact.current_output)
                interact.expect(config.prompt_pattern)
                interact.send("")
                output_file.write(interact.current_output)

        logger.info(f"Exit from {config.ip_address}.")
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt!")
    except Exception as e:
        logger.trace(e)
    finally:
        client.close()
