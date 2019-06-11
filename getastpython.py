import textwrap

from interpreter.lexical_analysis.lexer import Lexer
from interpreter.syntax_analysis.interpreter import NodeVisitor, Num
from interpreter.syntax_analysis.parser import Parser
from interpreter.lexical_analysis.tokenType import INT, NOT


class ASTVisualizer(NodeVisitor):
    def __init__(self, parser):
        self.num_tabs = 0
        self.parser = parser
        self.dot_heder = [textwrap.dedent("""
            ### nonek ###
            
            import random
            import math
            
        """)]
        self.dot_body = []
        self.dot_footer = []
        self.memory = {}
        self.current_scope = 'main'
        self.memory[self.current_scope] = []
        self.libs = []                             # imported libraries
        # list of custom functions declared in Functions section
        self.funcs = []
        # dict where key is function name and value dict with details of the function
        """
        {
            'arg_types': [],
            'arg_names': [],
            'arg_count': 0,
            'ret_type': '',
        } """
        self.fun_details = {}
        # dict where key is scope name and value dict with {var_name: var_type}
        self.scope_details = {}
        self.add_to_scope_details('main')

    def tabs(self):
        res = ''
        for i in range(self.num_tabs):
            res += '\t'
        return res

    def add_to_fun_details(self, fun_name):
        self.fun_details[fun_name] = {
            'arg_types': [],
            'arg_names': [],
            'arg_count': 0,
            'ret_type': '',
        }

    def add_to_scope_details(self, scope):
        self.scope_details[scope] = {}

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Library(self, node):
        self.libs.append(node.library)

    def visit_FunCall(self, node):
        if node.lib_name != 'This' and node.lib_name not in self.libs:
            raise Exception('Library {} is not imported.\nLine: {}'.format(node.lib_name, node.line_number))

        if node.lib_name == 'Stdio':
            if node.fun_name == 'inINT':
                s = 'int(input())'
                self.dot_body.append(s)
            elif node.fun_name == 'inSTRING':
                s = 'input()'
                self.dot_body.append(s)
            elif node.fun_name == 'out':
                s = '\n{}print('.format(self.tabs())
                self.dot_body.append(s)
                self.visit(node.args_nodes[0])
                s = ')'
                self.dot_body.append(s)

        elif node.lib_name == 'String':
            if node.fun_name == 'equals':
                self.visit(node.args_nodes[0])
                self.dot_body.append(' == ')
                self.visit(node.args_nodes[1])

            elif node.fun_name == 'append':
                self.dot_body.append('\n{}'.format(self.tabs()))
                self.visit(node.args_nodes[0])
                self.dot_body.append(' = ')
                self.visit(node.args_nodes[0])
                self.dot_body.append(' + ')
                self.visit(node.args_nodes[1])

            elif node.fun_name == 'size':
                self.dot_body.append('len(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(')')

            elif node.fun_name == 'get':
                self.visit(node.args_nodes[0])
                self.dot_body.append('[int(')
                self.visit(node.args_nodes[1])
                self.dot_body.append(')]')

            elif node.fun_name == 'notEqual':
                self.visit(node.args_nodes[0])
                self.dot_body.append(' != ')
                self.visit(node.args_nodes[1])

            elif node.fun_name == 'isDigit':
                self.dot_body.append('int(')
                self.visit(node.args_nodes[0])
                self.dot_body.append('.isdigit())')

            elif node.fun_name == 'isLetter':
                self.dot_body.append('int(')
                self.visit(node.args_nodes[0])
                self.dot_body.append('.isalpha())')

            elif node.fun_name == 'isSpace':
                self.dot_body.append('int(')
                self.visit(node.args_nodes[0])
                self.dot_body.append('.isspace())')

            elif node.fun_name == 'isInterpunction':
                self.dot_body.append('int(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(' in [\',\', \'.\', \':\', \'?\', \'!\', \';\'])')

            elif node.fun_name == 'substring':
                self.dot_body.append('')
                self.visit(node.args_nodes[0])
                self.dot_body.append('[')
                self.visit(node.args_nodes[1])
                self.dot_body.append(':')
                self.visit(node.args_nodes[2])
                self.dot_body.append(']')

            elif node.fun_name == 'toUpper':
                self.visit(node.args_nodes[0])
                self.dot_body.append('.upper()')

        elif node.lib_name == 'Random':
            if node.fun_name == 'range':
                self.dot_body.append('random.randrange(int(')
                self.visit(node.args_nodes[0])
                self.dot_body.append('), int(')
                self.visit(node.args_nodes[1])
                self.dot_body.append('))')

        elif node.lib_name == 'Math':
            if node.fun_name == 'sqrt':
                self.dot_body.append('math.sqrt(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(')')

        elif node.lib_name == 'Arrays':
            if node.fun_name == 'init':
                self.dot_body.append('\n{}'.format(self.tabs()))
                self.visit(node.args_nodes[0])
                self.dot_body.append(' = []')

            elif node.fun_name == 'append':
                self.dot_body.append('\n{}'.format(self.tabs()))
                self.visit(node.args_nodes[0])
                self.dot_body.append('.append(')
                self.visit(node.args_nodes[1])
                self.dot_body.append(')')

            elif node.fun_name == 'size':
                self.dot_body.append('len(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(')')

            elif node.fun_name == 'get':
                self.visit(node.args_nodes[0])
                self.dot_body.append('[int(')
                self.visit(node.args_nodes[1])
                self.dot_body.append(')]')

        elif node.lib_name == 'Number':
            if node.fun_name == 'isInteger':
                self.dot_body.append('float.is_integer(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(')')

            elif node.fun_name == 'toString':
                self.dot_body.append('str(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(')')

        elif node.lib_name == 'FileUtil':
            if node.fun_name == 'read':
                self.dot_body.append('open(')
                self.visit(node.args_nodes[0])
                self.dot_body.append(', \'r\').read()')

        elif node.lib_name == 'This':
            if node.fun_name not in self.funcs:
                raise Exception('Function {} is not defined.\nLine: {}'.format(node.fun_name, node.line_number))

            if len(node.args_nodes) != self.fun_details[node.fun_name]['arg_count']:
                raise Exception('Function {} expects {} arguments, but {} given.\nLine: {}'
                                .format(node.fun_name, self.fun_details[node.fun_name]['arg_count'],
                                        len(node.args_nodes), node.line_number))

            self.dot_body.append('{}('.format(node.fun_name))
            for i in range(len(node.args_nodes)):
                child = node.args_nodes[i]

                expected_type = self.fun_details[node.fun_name]['arg_types'][i]
                found_type = self.scope_details[self.current_scope][child.var[1:]]
                if expected_type != found_type:
                    raise Exception('In function {} argument type {} expected, but {} given.\nLine: {}'
                                    .format(node.fun_name, expected_type, found_type, node.line_number))

                self.visit(child)
                if child != node.args_nodes[-1]:
                    self.dot_body.append(', ')
            self.dot_body.append(')\n')

    def visit_FunImpl(self, node):
        s = '{}def {}('.format(self.tabs(), node.fun_name)
        self.dot_body.append(s)
        self.current_scope = node.fun_name
        self.memory[node.fun_name] = []
        if node.fun_name in self.funcs:
            raise Exception('Function {} already defined.\nLine: {}'.format(node.fun_name, node.line_number))
        else:
            self.funcs.append(node.fun_name)
            self.add_to_fun_details(node.fun_name)
            self.add_to_scope_details(node.fun_name)

        self.visit(node.args_node)

        self.dot_body.append('):')
        self.num_tabs += 1
        self.visit(node.stmts_node)
        self.visit(node.ret_node)
        self.num_tabs -= 1

        expected_type = self.fun_details[self.current_scope]['ret_type']
        found_type = self.scope_details[self.current_scope][node.ret_node.var_node.var[1:]]
        if expected_type != found_type:
            raise Exception('In function {} expected return type {}, but {} found.\nLine: {}'
                            .format(node.fun_name, expected_type, found_type, node.ret_node.line_number))

        self.current_scope = 'main'

    def visit_Return(self, node):
        s = '\n{}return '.format(self.tabs())
        self.dot_body.append(s)
        self.visit(node.var_node)
        self.fun_details[self.current_scope]['ret_type'] = node.type_node.type
        self.dot_body.append('\n')

    def visit_Cond(self, node):
        self.dot_body.append('\n{}if '.format(self.tabs()))
        self.visit(node.bool_expr)
        self.dot_body.append(':')

        self.num_tabs += 1
        self.visit(node.stmts_node)
        self.num_tabs -= 1

    def visit_Loop(self, node):
        self.dot_body.append('\n{}while '.format(self.tabs()))
        self.visit(node.bool_expr)
        self.dot_body.append(':')

        self.num_tabs += 1
        self.visit(node.stmts_node)
        self.num_tabs -= 1

    def visit_VarDecl(self, node):
        if node.var_node.var not in self.memory[self.current_scope]:
            self.memory.setdefault(self.current_scope, []).append(node.var_node.var)
            self.scope_details[self.current_scope][node.var_node.var] = node.type_node.type
        else:
            raise Exception('Variable {} already defined in {}.\nLine: {}'
                            .format(node.var_node.var, self.current_scope, node.var_node.line_number))

        self.visit(node.type_node)

    def visit_Assign(self, node):
        self.dot_body.append('\n')
        self.dot_body.append(self.tabs())

        self.visit(node.var_node)
        self.dot_body.append(' = ')
        var_type = self.scope_details[self.current_scope][node.var_node.var[1:]]
        if var_type == INT and isinstance(node.expr, Num):
            self.dot_body.append('int(')
            self.visit(node.expr)
            self.dot_body.append(')')
        else:
            self.visit(node.expr)

    def visit_Args(self, node):
        for child in node.args:
            self.dot_body.append(child.var_node.var)
            self.memory.setdefault(self.current_scope, []).append(child.var_node.var)        # add variable to scope
            # add type and name to details and increment arg counter
            self.fun_details[self.current_scope]['arg_types'].append(child.type_node.type)
            self.fun_details[self.current_scope]['arg_names'].append(child.var_node.var)
            self.fun_details[self.current_scope]['arg_count'] += 1

            if child != node.args[-1]:
                self.dot_body.append(', ')

    def visit_Stmts(self, node):
        for child in node.stmts:
            self.dot_body.append(self.tabs())
            self.visit(child)

    def visit_Type(self, node):
        s = ''
        self.dot_body.append(s)

    def visit_Var(self, node):
        # if value starts with '#' then it is variable
        if isinstance(node.var, str) and node.var.startswith('#') and len(node.var) > 1:
            if node.var[1:] not in self.memory[self.current_scope]:
                raise Exception('Variable {} is not defined in {}.\nLine: {}'
                                .format(node.var[1:], self.current_scope, node.line_number))
            s = '{}'.format(node.var[1:])
        # value is string
        else:
            s = '\'{}\''.format(node.var)
        self.dot_body.append(s)

    def visit_String(self, node):
        s = '\'{}\''.format(node.value)
        self.dot_body.append(s)

    def visit_BinOp(self, node):
        self.dot_body.append('(')
        self.visit(node.left)
        s = ' {} '.format(node.op.value)
        self.dot_body.append(s)
        self.visit(node.right)
        self.dot_body.append(')')

    def visit_UnOp(self, node):
        if node.token.type == NOT:
            s = 'not'
        else:
            s = '-'
        self.dot_body.append(s)
        self.visit(node.bool_expr)

    def visit_Num(self, node):
        s = '{}'.format(str(node.value))
        self.dot_body.append(s)

    def genDot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_heder + self.dot_body + self.dot_footer)


def main():
    fname = './examples/test1.txt'
    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.genDot()

    print(content)
    out = open('./examples/compiled_files/sample_compiled.py', 'w')
    out.write(content)


if __name__ == '__main__':
    main()
