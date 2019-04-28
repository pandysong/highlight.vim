import sys
import json


def parse_to_dict(path, fn):
    with open(fn) as f:
        file_to_lines = dict()
        for line in f:
            file_path, line_num = line.split(':')
            # remove the prefix path so it becomes the relative path
            if file_path.startswith(path):
                file_path = file_path[len(path):]
                if file_path.startswith('/'):
                    file_path = file_path[1:]
            # update the dictionary
            newset = file_to_lines.get(file_path, set())
            newset.add(int(line_num))
            file_to_lines[file_path] = newset
        return file_to_lines


def line_set_to_pattern(line_dict):
    ''' convert a set like set([2, 3]) to pattern '\%2l\|\%3l'
    '''
    return '\\|'.join('\\%{}l'.format(ln) for ln in sorted(line_dict))


def convert_to_database(file_to_lines):
    print("{", end='')
    for key in sorted(file_to_lines.keys()):
        patterns = line_set_to_pattern(file_to_lines[key])
        print("'{}':'{}',".format(key, patterns), end='')
    print("}", end='')


if len(sys.argv) < 3:
    print("usage: {} path linesfile".format(sys.argv[0]))
    print("       convert the linefiles to a database recognized by vim plugin"
          "       `highlight.vim` in https://github.com/pandysong/highlight.vim"
          "       path: is the leading path to be removed from file path in linesfile")
    exit(1)

convert_to_database(parse_to_dict(sys.argv[1], sys.argv[2]))
