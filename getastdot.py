import textwrap

from interpreter.lexical_analysis.lexer import Lexer
from interpreter.syntax_analysis.interpreter import NodeVisitor
from interpreter.syntax_analysis.parser import Parser


class ASTVisualizer(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.nodecount = 1
        self.dot_heder = [textwrap.dedent("""
            digraph astgraph {
                node [shape=box, fontsize=12, fontname="Courier", height=.1];
                ranksep=.3;   
                edge [arrowsize=.5]
        """)]
        self.dot_body = []
        self.dot_footer = ['}']

    def visit_Program(self, node):
        s = 'node{} [label="Program"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.children:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

    def visit_Library(self, node):
        s = 'node{} [label="Library: {}"]\n'.format(self.nodecount, node.library)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_FunCall(self, node):
        s = 'node{} [label="FunCall: {} {}"]\n'.format(self.nodecount, node.lib_name, node.fun_name)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.args_nodes:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

    def visit_FunImpl(self, node):
        s = 'node{} [label="FunImpl: {}"]\n'.format(self.nodecount, node.fun_name)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.args_node)
        s = 'node{} -> node{}\n'.format(node.num, node.args_node.num)
        self.dot_body.append(s)

        self.visit(node.stmts_node)
        s = 'node{} -> node{}\n'.format(node.num, node.stmts_node.num)
        self.dot_body.append(s)

        self.visit(node.ret_node)
        s = 'node{} -> node{}\n'.format(node.num, node.ret_node.num)
        self.dot_body.append(s)

    def visit_Return(self, node):
        s = 'node{} [label="Return"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.type_node)
        s = 'node{} -> node{}\n'.format(node.num, node.type_node.num)
        self.dot_body.append(s)

        self.visit(node.var_node)
        s = 'node{} -> node{}\n'.format(node.num, node.var_node.num)
        self.dot_body.append(s)

    def visit_Cond(self, node):
        s = 'node{} [label="Cond"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.bool_expr)
        s = 'node{} -> node{}\n'.format(node.num, node.bool_expr.num)
        self.dot_body.append(s)

        self.visit(node.stmts_node)
        s = 'node{} -> node{}\n'.format(node.num, node.stmts_node.num)
        self.dot_body.append(s)

    def visit_Loop(self, node):
        s = 'node{} [label="Loop"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.bool_expr)
        s = 'node{} -> node{}\n'.format(node.num, node.bool_expr.num)
        self.dot_body.append(s)

        self.visit(node.stmts_node)
        s = 'node{} -> node{}\n'.format(node.num, node.stmts_node.num)
        self.dot_body.append(s)

    def visit_VarDecl(self, node):
        s = 'node{} [label="VarDecl"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.type_node)
        s = 'node{} -> node{}\n'.format(node.num, node.type_node.num)
        self.dot_body.append(s)

        self.visit(node.var_node)
        s = 'node{} -> node{}\n'.format(node.num, node.var_node.num)
        self.dot_body.append(s)

    def visit_Assign(self, node):
        s = 'node{} [label="Assign"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.var_node)
        s = 'node{} -> node{}\n'.format(node.num, node.var_node.num)
        self.dot_body.append(s)

        self.visit(node.expr)
        s = 'node{} -> node{}\n'.format(node.num, node.expr.num)
        self.dot_body.append(s)

    def visit_FunDecl(self, node):
        s = 'node{} [label="FunDecl: {}"]\n'.format(self.nodecount, node.fun_name)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.type_node)
        s = 'node{} -> node{}\n'.format(node.num, node.type_node.num)
        self.dot_body.append(s)

        self.visit(node.args_node)
        s = 'node{} -> node{}\n'.format(node.num, node.args_node.num)
        self.dot_body.append(s)

        self.visit(node.stmts_node)
        s = 'node{} -> node{}\n'.format(node.num, node.stmts_node.num)
        self.dot_body.append(s)

    def visit_Args(self, node):
        s = 'node{} [label="Args"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.args:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

    def visit_Stmts(self, node):
        s = 'node{} [label="Stmts"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.stmts:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

    def visit_Type(self, node):
        s = 'node{} [label="Type: {}"]\n'.format(self.nodecount, node.type)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_Var(self, node):
        s = 'node{} [label="Var: {}"]\n'.format(self.nodecount, node.var)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_String(self, node):
        s = 'node{} [label="String: {}"]\n'.format(self.nodecount, node.value)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_BinOp(self, node):
        s = 'node{} [label="{}"]\n'.format(self.nodecount, node.op)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.left)
        s = 'node{} -> node{}\n'.format(node.num, node.left.num)
        self.dot_body.append(s)

        self.visit(node.right)
        s = 'node{} -> node{}\n'.format(node.num, node.right.num)
        self.dot_body.append(s)

    def visit_UnOp(self, node):
        s = 'node{} [label="{}"]\n'.format(self.nodecount, node.token.type)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.bool_expr)
        s = 'node{} -> node{}\n'.format(node.num, node.bool_expr.num)
        self.dot_body.append(s)

    def visit_Num(self, node):
        s = 'node{} [label="{}"]\n'.format(self.nodecount, node.value)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def genDot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_heder + self.dot_body + self.dot_footer)


def main():
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('fname')
    #
    # args = argparser.parse_args()
    fname = './examples/test1.txt'  # args.fname
    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.genDot()

    print(content)


if __name__ == '__main__':
    main()
