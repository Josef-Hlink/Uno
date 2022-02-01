class Bigvalue():
    def __init__(self):
        self.dict = self.get_dict()

    def __call__(self, key):
        """The key can be either a string or an int"""
        return self.dict[key]

    def get_dict(self) -> dict:
        """With this dict the big notation for every possible card value can be accessed"""
        zero: list[str] = [
            ' ' * 8 + ' __ ' + ' ' * 8,
            ' ' * 8 + '/  \\' + ' ' * 8,
            ' ' * 8 + '\\__/' + ' ' * 8
        ]
        one: list[str] = [
            ' ' * 9 + ',| ' + ' ' * 8,
            ' ' * 9 + ' | ' + ' ' * 8,
            ' ' * 9 + '_|_' + ' ' * 8
        ]
        two: list[str] = [
            ' ' * 8 + ' ___ ' + ' ' * 7,
            ' ' * 8 + ' ___)' + ' ' * 7,
            ' ' * 8 + '(___ ' + ' ' * 7
        ]
        three: list[str] = [
            ' ' * 8 + '___ ' + ' ' * 8,
            ' ' * 8 + '___)' + ' ' * 8,
            ' ' * 8 + '___)' + ' ' * 8
        ]
        four: list[str] = [
            ' ' * 8 + ' /| ' + ' ' * 8,
            ' ' * 8 + '/_| ' + ' ' * 8,
            ' ' * 8 + ' _|_' + ' ' * 8
        ]
        five: list[str] = [
            ' ' * 8 + ' ___ ' + ' ' * 7,
            ' ' * 8 + '|___ ' + ' ' * 7,
            ' ' * 8 + ' ___)' + ' ' * 7
        ]
        six: list[str] = [
            ' ' * 8 + '  /  ' + ' ' * 7,
            ' ' * 8 + ' /__ ' + ' ' * 7,
            ' ' * 8 + '(___)' + ' ' * 7
        ]
        seven: list[str] = [
            ' ' * 8 + '___ ' + ' ' * 8,
            ' ' * 8 + ' _/_' + ' ' * 8,
            ' ' * 8 + ' /  ' + ' ' * 8
        ]
        eight: list[str] = [
            ' ' * 8 + ' ___ ' + ' ' * 7,
            ' ' * 8 + '(___)' + ' ' * 7,
            ' ' * 8 + '(___)' + ' ' * 7
        ]
        nine: list[str] = [
            ' ' * 8 + ' ___ ' + ' ' * 7,
            ' ' * 8 + '(___)' + ' ' * 7,
            ' ' * 8 + '   / ' + ' ' * 7
        ]
        reverse: list[str] = [
            ' ' * 3 + ' __   __      ' + ' ' * 3,
            ' ' * 3 + '|__) |__  \\  /' + ' ' * 3,
            ' ' * 3 + '| \\  |__   \\/ ' + ' ' * 3
        ]
        skip: list[str] = [
            ' ' * 3 + ' __  |   o  __ ' + ' ' * 2,
            ' ' * 3 + '(__  |/  | |__)' + ' ' * 2,
            ' ' * 3 + ' __) |\\  | |   ' + ' ' * 2
        ]
        plusfour: list[str] = [
            ' ' * 5 + '  |     /| ' + ' ' * 4,
            ' ' * 5 + '--+--  /_| ' + ' ' * 4,
            ' ' * 5 + '  |     _|_' + ' ' * 4
        ]
        plustwo: list[str] = [
            ' ' * 4 + '  |     ___ ' + ' ' * 4,
            ' ' * 4 + '--+--   ___)' + ' ' * 4,
            ' ' * 4 + '  |    (___ ' + ' ' * 4
        ]
        wild: list[str] = [
            ' ' * 2 + '       o |   __|' + ' ' * 2,
            ' ' * 2 + '\\    / | |  /  |' + ' ' * 2,
            ' ' * 2 + ' \\/\\/  | |_ \\__|' + ' ' * 2
        ]
        dictionary: dict = {
            0: zero, 1: one, 2: two, 3: three, 4: four, 5: five, 6: six, 7: seven, 8: eight, 9: nine,
            'Reverse': reverse, 'Skip': skip, 'Draw Four': plusfour, 'Draw Two': plustwo, 'Wild': wild
        }
        return dictionary
    