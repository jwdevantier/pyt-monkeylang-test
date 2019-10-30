from ghostwriter.writer import Writer
from ghostwriter.utils.template.dsl import *
import typing as t

class DefObj(Component):
    def __init__(self, typ, fields, obj_type, inspect_expr):
        self.typ = typ
        self.fields = fields
        self.obj_type = obj_type
        self.inspect_expr = inspect_expr

    @property
    def template(self) -> str:
        return """
        type <<self.typ>> struct {
            % for ident,typ in self.fields.items()
            <<ident>> <<typ>>
            % /for
        }

        func (<<self.typ.lower()[0]>> *<<self.typ>>) Type() ObjectType { return <<self.obj_type>> }
        func (<<self.typ.lower()[0]>> *<<self.typ>>) Inspect() string  { return <<self.inspect_expr>> }"""

@snippet()
def mk_int():
    return DefObj('Integer', {'Value': 'int64'}, 'INTEGER_OBJ', """fmt.Sprintf("%d", i.Value)""")

@snippet()
def mk_bool():
    return DefObj('Boolean', {'Value': 'bool'}, 'BOOLEAN_OBJ', """fmt.Sprintf("%t", b.Value)""")

@snippet()
def mk_null():
    return DefObj('Null', {}, 'NULL_OBJ', '"null"')

@snippet()
def mk_retval():
    return DefObj('ReturnValue', {'Value': 'Object'}, 'RETURN_VALUE_OBJ', 'r.Value.Inspect()')

@snippet()
def mk_error():
    return DefObj('Error', {'Message': 'string'}, 'ERROR_OBJ', '"ERROR: " + e.Message')

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