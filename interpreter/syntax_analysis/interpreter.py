class AST(object):
    def __init__(self, line_number):
        self.line_number = line_number


class Program(AST):
    def __init__(self, sections, line_number):
        super().__init__(line_number)
        self.children = sections


class Library(AST):
    def __init__(self, library, line_number):
        super().__init__(line_number)
        self.library = library


class FunImpl(AST):
    def __init__(self, fun_name, args_node, stmts_node, ret_node, line_number):
        super().__init__(line_number)
        self.fun_name = fun_name
        self.args_node = args_node
        self.stmts_node = stmts_node
        self.ret_node = ret_node


class Return(AST):
    def __init__(self, type_node, var_node, line_number):
        super().__init__(line_number)
        self.type_node = type_node
        self.var_node = var_node


class FunCall(AST):
    def __init__(self, lib_name, fun_name, args_nodes, line_number):
        super().__init__(line_number)
        self.lib_name = lib_name
        self.fun_name = fun_name
        self.args_nodes = args_nodes


class Cond(AST):
    def __init__(self, bool_expr, stmts_node, line_number):
        super().__init__(line_number)
        self.bool_expr = bool_expr
        self.stmts_node = stmts_node


class Loop(AST):
    def __init__(self, bool_expr, stmts_node, line_number):
        super().__init__(line_number)
        self.bool_expr = bool_expr
        self.stmts_node = stmts_node


class Type(AST):
    def __init__(self, type, line_number):
        super().__init__(line_number)
        self.type = type


class Var(AST):
    def __init__(self, var, line_number):
        super().__init__(line_number)
        self.var = var


class String(AST):

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class VarDecl(AST):
    def __init__(self, type_node, var_node, line_number):
        super().__init__(line_number)
        self.type_node = type_node
        self.var_node = var_node


class Assign(AST):
    def __init__(self, var_node, expr, line_number):
        super().__init__(line_number)
        self.var_node = var_node
        self.expr = expr


class Args(AST):
    def __init__(self, args, line_number):
        super().__init__(line_number)
        self.args = args


class Stmts(AST):
    def __init__(self, stmts, line_number):
        super().__init__(line_number)
        self.stmts = stmts


class BinOp(AST):
    def __init__(self, left, op, right, line_number):
        super().__init__(line_number)
        self.left = left
        self.token = self.op = op
        self.right = right


class UnOp(AST):
    def __init__(self, token, bool_expr, line_number):
        super().__init__(line_number)
        self.token = token
        self.bool_expr = bool_expr


class Num(AST):
    def __init__(self, token, line_number):
        super().__init__(line_number)
        self.token = token
        self.value = token.value


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.error)
        return visitor(node)

    def error(self, node):
        raise Exception('Not found {}'.format(type(node).__name__))
