# from ghostwriter.writer import Writer
# from ghostwriter.utils.template.dsl import *
# import typing as t

# model_fns_prefix = 'IDENT INT STRING BANG MINUS TRUE FALSE LPAREN IF FUNCTION LBRACKET LBRACE'.split()
# model_fns_infix = 'PLUS MINUS SLASH ASTERISK EQ NOT_EQ LT GT'.split()
# model_fns_call = 'LPAREN LBRACKET'.split()

# class RegisterFns(Component):
#     def __init__(self):
#         self.fns_prefix = model_fns_prefix
#         self.fns_infix = model_fns_infix
#         self.fns_call = model_fns_call

#     @property
#     def template(self) -> str:
#         return """
#         % for token in self.fns_prefix
#         p.registerPrefix(token.IDENT, p.parseIdentifier)
#         % /for
#         tok.Literal = ""
#         tok.Type = token.EOF"""

# @snippet()
# def register_fns():
#     return RegisterFns()