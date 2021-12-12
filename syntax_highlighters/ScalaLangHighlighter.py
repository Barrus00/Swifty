from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp

"""
This is based on the https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting example.
"""


def _format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)

    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax elements highlight colors.
STYLES = {
    'keyword': _format('orange'),
    'special_operator': _format('darkOrange'),
    'operator': _format('red'),
    'brace': _format('darkMagenta'),
    'string': _format('darkGreen'),
    'comment': _format('gray', 'italic'),
    'number': _format('blue'),
}


class ScalaHighlighter(QSyntaxHighlighter):
    # Here we define the syntax elements to highlight, feel free to add more, but please be careful
    # as they are used in the regexes, so make sure that you escape every special character.

    keywords = [
        'abstract', 'finally', 'object', 'trait',
        'case', 'for', 'override', 'true',
        'catch', 'forSome', 'package', 'try',
        'class', 'if', 'private', 'type',
        'def', 'implicit', 'protected', 'val',
        'do', 'import', 'return', 'var',
        'else', 'lazy', 'sealed', 'while',
        'extends', 'match', 'super', 'with',
        'false', 'new', 'this', 'yield',
        'final', 'null', 'throw', 'func'
    ]

    special_operators = [
        '⇒', '=>', '=', '<%', '<:', '←',
        '<-', '#', '@', ':', '_'
    ]

    operators = [
        '=',
        # Comparison
        '==', '===', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '\%',
        # Bitwise
        '\&', '\|', '\^', '\~', '<<', '>>', '>>>',
        # Boolean
        '\&\&', '\|\|', '!'
    ]

    braces = ['\{', '\}', '\[', '\]', '\(', '\)']

    def __init__(self, document):
        super().__init__(document)

        # Here we combine all the elements to highlight into a list of tuples, where each tuple is
        # (regex, nth, format) where 'nth' is the index of matched group in regex, and 'format is
        # the style format to apply on that group.
        self.rules = []

        self.rules += [(r'\b%s\b' % x, 0, STYLES['keyword']) for x in self.keywords]
        self.rules += [(r'%s' % x, 0, STYLES['special_operator']) for x in self.special_operators]
        self.rules += [(r'%s' % x, 0, STYLES['operator']) for x in self.operators]
        self.rules += [(r'%s' % x, 0, STYLES['brace']) for x in self.braces]

        self.rules += [
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['number']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['number']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['number']),
            # String literals
            (r'"([^"\\]|\\.)*"', 0, STYLES['string']),
            # Comments
            (r'//[^\n]*', 0, STYLES['comment']),
        ]

        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in self.rules]

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text.
        """
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
