from dataclasses import dataclass
from typing import Optional


@dataclass
class CommandInfo:
    command: str
    timeout: int


@dataclass
class Config:
    ip_address: str
    username: str
    timeout: int
    private_key: Optional[str]
    passphrase: Optional[str]
    command_list: list[CommandInfo]
