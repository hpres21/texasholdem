def print_file(filename):
    with open(filename, 'r') as f:
        file_contents = f.read()
        print(file_contents)

def print_title():
    print()
    print_file('util/title.txt')
    print()

def print_subtitle():
    print_file('util/subtitle.txt')

def print_cowboy():
    print_file('util/cowboy.txt')