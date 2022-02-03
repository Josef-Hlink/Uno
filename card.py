import typing

class Card:
    def __init__(self, colour: str, value):
        self.colour: str = colour
        self.value: typing.Union[str, int] = value # can be string or int
    
    def __str__(self) -> str:
        return f'[{self.colour} | {self.value}]'

    def is_valid_move(self, topCard) -> bool:
        if self.colour == 'Black': # always legal
            return True
        elif self.colour == topCard.colour or self.value == topCard.value:
            return True
        return False
    
    def is_valid_last_move(self, topCard) -> bool:
        if isinstance(self.value, int) and self.is_valid_move(topCard):
            return True
        return False
