from dataclasses import dataclass


@dataclass
class Tasks:
    completed: list[str]
    active: list[str]


@dataclass
class User:
    username: str
    company: str
    email: str
    todos: dict[Tasks]
