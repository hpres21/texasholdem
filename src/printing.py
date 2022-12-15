def print_file(filename):
    """
    generic function for printing from text files stored in util/
    """
    with open(filename) as f:
        file_contents = f.read()
        print(file_contents)


def print_title():
    """
    print the game title
    """
    print()
    print_file("util/title.txt")
    print()


def print_cowboy():
    """
    print the cowboy game host
    """
    print_file("util/cowboy.txt")


def print_cards(list_of_cards):
    """
    string formatting for a list of cards
    """
    return " ".join(map(str, list_of_cards))
