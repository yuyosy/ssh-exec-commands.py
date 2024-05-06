import json

from loguru import logger
from ruamel.yaml import YAML

from ssh_exec_commands.connect import connect_ssh
from ssh_exec_commands.resource_path import resource_path
from ssh_exec_commands.types import CommandInfo, Config

logger.add(resource_path("app.log"))


def load_config() -> Config:
    # Load SSH connection settings from JSON
    yaml = YAML(typ="safe")
    with resource_path("ssh_config.yaml").open("r") as f:
        config_file = yaml.load(f)
    command_list = []
    timeout = config_file.get("timeout", 60)
    for info in config_file.get("command_list", []):
        command_list.append(
            CommandInfo(
                command=info.get("command", ""),
                timeout=info.get("timeout", timeout),
                prompt_pattern=info.get("prompt_pattern", None),
            )
        )
    config = Config(
        ip_address=config_file.get("ip_address", ""),
        username=config_file.get("username", ""),
        timeout=timeout,
        private_key=config_file.get("private_key_path", None),
        passphrase=config_file.get("passphrase", None),
        prompt_pattern=config_file.get("prompt_pattern", ".*$\\s*"),
        command_list=command_list,
    )
    return config


if __name__ == "__main__":
    logger.info("Start")

    config = load_config()
    connect_ssh(config)

    logger.info("Finished!")
