# coding: utf-8


# Russian alphabet
cyrillic = [
    ['А', 'A'],
    ['Б', 'B'],
    ['В', 'V'],
    ['Г', 'G'],
    ['Д', 'D'],
    ['Е', 'E'],
    ['Ё', 'E'],
    ['Ж', 'ZH'],
    ['З', 'Z'],
    ['И', 'I'],
    ['Й', 'I'],
    ['К', 'K'],
    ['Л', 'L'],
    ['М', 'M'],
    ['Н', 'N'],
    ['О', 'O'],
    ['П', 'P'],
    ['Р', 'R'],
    ['С', 'S'],
    ['Т', 'T'],
    ['У', 'U'],
    ['Ф', 'F'],
    ['Х', 'KH'],
    ['Ц', 'TS'],
    ['Ч', 'CH'],
    ['Ш', 'SH'],
    ['Щ', 'SHCH'],
    ['Ы', 'Y'],
    ['Ь', ''],
    ['Ъ', 'IE'],
    ['Э', 'E'],
    ['Ю', 'IU'],
    ['Я', 'IA'],
]


def decode(string, lower=True, replace=None):
    """
    Decode rus to lat

    :type string: str
    :type lower: bool
    :type replace: list
    :return: str
    """

    new_str = ''

    for item in string:
        character = search_character(item)

        if replace:
            character = replace_character(character, replace)

        if lower:
            new_str += character.lower()
        else:
            if item.isupper():
                new_str += character
            else:
                new_str += character.lower()

    return new_str.strip()


def search_character(char):
    """
    :type char: str
    :return: str
    """
    for item in cyrillic:
        if item[0] == char.upper():
            return item[1]

    return char


def replace_character(char, replace):
    """
    Замена символа на определённый пользователем. Пример ``replace``:

        [
            [' ', '-']
        ]

    :param char:
    :param replace:
    :return:
    """
    for item in replace:
        if item[0].upper() == char:
            return item[1]

    return char
