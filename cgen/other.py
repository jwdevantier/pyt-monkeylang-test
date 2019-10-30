from ghostwriter.utils.template.dsl import *

class Struct(Component):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    
    template = """\
        type <<self.name>> struct {
            % for name, typ in self.fields.items()
            <<name>> <<typ>>
            % /for
        }"""
