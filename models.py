from dataclasses import dataclass

@dataclass
class User:
    username: str
    id: str
    token: str = ''

@dataclass
class Post:
    title: str
    text: str
