from ghostwriter.writer import Writer
from ghostwriter.utils.template.dsl import *
import typing as t
import other

class LexFile(Component):
    def __init__(self, tokens, lex_handlers):
        self.tokens = tokens
        self.lex_handlers = lex_handlers
        self.chars = ''.join([c for c in tokens.keys() if len(c) == 1])

    @property
    def template(self) -> str:
        return """
        package lexer

        import "monkey/token"

        type Lexer struct {
            input string
            position int  // current position in input (points to current char)
            readPosition int  // current reading position in input (after current char)
            ch byte // current char under examination
        }

        func New(input string) *Lexer {
            l := &Lexer{input: input}
            l.readChar()
            return l
        }

        % r LexNextToken(tokens=self.tokens, chars=self.chars, handlers=self.lex_handlers)
        % /r

        func (l *Lexer) skipWhitespace() {
            for l.ch == ' ' || l.ch == '\\t' || l.ch == '\\n' || l.ch == '\\r' {
                l.readChar()
            }
        }

        func (l *Lexer) readChar() {
            if l.readPosition >= len(l.input) {
                l.ch = 0
            } else {
                l.ch = l.input[l.readPosition]
            }
            l.position = l.readPosition
            l.readPosition += 1
        }

        func (l *Lexer) peekChar() byte {
            if l.readPosition >= len(l.input) {
                return 0
            } else {
                return l.input[l.readPosition]
            }
        }

        func (l *Lexer) readIdentifier() string {
            position := l.position
            for isLetter(l.ch) {
                l.readChar()
            }
            return l.input[position:l.position]
        }

        func (l *Lexer) readNumber() string {
            position := l.position
            for isDigit(l.ch) {
                l.readChar()
            }
            return l.input[position:l.position]
        }

        func (l *Lexer) readString() string {
            position := l.position + 1
            for {
                l.readChar()
                if l.ch == '"' || l.ch == 0 {
                    break
                }
            }
            return l.input[position:l.position]
        }

        func isLetter(ch byte) bool {
            return 'a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || ch == '_'
        }

        func isDigit(ch byte) bool {
            return '0' <= ch && ch <= '9'
        }

        func newToken(tokenType token.TokenType, ch byte) token.Token {
            return token.Token{Type: tokenType, Literal: string(ch)}
        }"""


class LexZero(Component):
    @property
    def template(self) -> str:
        return """
        tok.Literal = ""
        tok.Type = token.EOF"""

class LexQuote(Component):
    @property
    def template(self) -> str:
        return """
        tok.Type = token.STRING
        tok.Literal = l.readString()"""


class LexBang(Component):
    @property
    def template(self) -> str:
        return """
        if l.peekChar() == '=' {
            ch := l.ch
            l.readChar()
            literal := string(ch) + string(l.ch)
            tok = token.Token{Type: token.NOT_EQ, Literal: literal}
        } else {
            tok = newToken(token.BANG, l.ch)
        }"""


class LexEqual(Component):
    @property
    def template(self) -> str:
        return """
        if l.peekChar() == '=' {
            ch := l.ch
            l.readChar()
            literal := string(ch) + string(l.ch)
            tok = token.Token{Type: token.EQ, Literal: literal}
        } else {
            tok = newToken(token.ASSIGN, l.ch)
        }"""


class LexNextToken(Component):
    def __init__(self, tokens: t.Dict[str, str], chars: str, handlers: t.Mapping[str, Component]):
        self.tokens = tokens
        self.chars = chars
        self.lex_handlers = handlers

    @property
    def template(self) -> str:
        return """
func (l *Lexer) NextToken() token.Token {
    var tok token.Token

    l.skipWhitespace()

    switch l.ch {
    % for char in self.chars
    case '<<char>>':
        % if char in self.lex_handlers
        % r self.lex_handlers[char]()
        % /r
        % else
        tok = newToken(token.<<self.tokens[char]>>, l.ch)
        % /if
    % /for
    default:
        if isLetter(l.ch) {
            tok.Literal = l.readIdentifier()
            tok.Type = token.LookupIdent(tok.Literal)
            return tok
        } else if isDigit(l.ch) {
            tok.Type = token.INT
            tok.Literal = l.readNumber()
            return tok
        } else {
            tok = newToken(token.ILLEGAL, l.ch)
        }
    }
    l.readChar()
    return tok
}"""


# def test(context, prefix, writer):
#     writer.write("hello")
#     writer.write(" world!!!")
#     print(context)
#     print(context.src)


class MiniProg(Component):
    def __init__(self):
        self.person_fields = {'name': 'string', 'age': 'int'}
    
    template = """\
        //prologue
        %r other.Struct('Person', self.person_fields)
        %/r
        //epilogue"""

@snippet()
def test():
    return MiniProg()

# @snippet()
# def test():
#     return Struct('Person', {'name': 'string', 'age': 'int'})


@snippet()
def main():
    tokens = {
        # <token lexeme> => <token type>
        '=': 'ASSIGN',
        '+': 'PLUS',
        '-': 'MINUS',
        '!=': 'NOT_EQ',
        '!': 'BANG',
        '/': 'SLASH',
        '*': 'ASTERISK',
        '>': 'GT',
        '<': 'LT',
        ';': 'SEMICOLON',
        ':': 'COLON',
        ',': 'COMMA',
        '{': 'LBRACE',
        '}': 'RBRACE',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '"': 'STRING',
        '[': 'LBRACKET',
        ']': 'RBRACKET',
        '0': 'EOF',
    }
    lex_handlers = {
        '0': LexZero,
        '"': LexQuote,
        '!': LexBang,
        '=': LexEqual
    }
    return LexFile(tokens, lex_handlers)

# class Email(Component):
#     def __init__(self, recipient, sender):
#         print(f"self.recipient = '{recipient}'")
#         self.recipient = recipient
#         print(f"self.sender = '{sender}'")
#         self.sender = sender
#         self.name = ' '.join([s.capitalize() for s in sender.split('@')[0].split('-')])

#     template = """
#     To: <<self.recipient>>
#     From: <<self.sender>>

#     % body

#     Regards, <<self.name>>.
#     EvilCorp - Eroding your privacy with 'free' services.

#     This message is confidential and intended for the recipient specified
#     in the message only. It is strictly forbidden to share any part of this
#     message"""

# class MyMessage(Component):
#     template = """
#     % r Email('joe@example.org', 'jane-doe@evilcorp.org')
#     Dear Joe,
    
#     We have a business proposal for you, please swing by our offices
#     at your earliest convenience.
#     % /r"""

# @snippet()
# def my_message():
#     return MyMessage()