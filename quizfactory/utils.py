from re import compile as re_compile

re_identation = re_compile(r"^ *")


def strip_indents(text, tab_to_space=4):
    """Remove useless indentations"""

    text = text.replace("\t", " " * tab_to_space)
    text = text.replace("\r", "")  # unix ftw

    # split to lines
    lines = [line if line.strip() else "" for line in text.split("\n")]

    # search useless indentations
    try:
        min_identation = min(
            (re_identation.search(line).group(0) for line in lines if line),
            key=lambda spaces: len(spaces)
        )
    except ValueError:
        return '\n'.join(lines)
    else:
        # replace min_identation in every line
        return '\n'.join(l.replace(min_identation, "", 1) for l in lines)
