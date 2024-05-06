from dataclasses import dataclass
from typing import Optional


@dataclass
class CommandInfo:
    command: str = ""
    timeout: int = -1
    prompt_pattern: Optional[str] = None


@dataclass
class Config:
    ip_address: str
    username: str
    timeout: int
    private_key: Optional[str]
    passphrase: Optional[str]
    prompt_pattern: str
    command_list: list[CommandInfo]
