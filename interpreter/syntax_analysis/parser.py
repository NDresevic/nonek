from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import *
from interpreter.syntax_analysis.util import restorable


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected, found):
        raise Exception('Error parsing: expected {}, but found {}.\nLine: {}'
                        .format(expected, found, self.lexer.line_count))

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(type, self.current_token.type)

    def program(self):
        """
        program                     : sections

        sections                	: (libraries | functions | execution)*
        """
        sections = []

        while self.current_token.type in [LIBRARIES, FUNCTIONS, EXECUTION]:
            if self.current_token.type == LIBRARIES:
                self.eat(LIBRARIES)
                sections.extend(self.libraries())
            elif self.current_token.type == FUNCTIONS:
                self.eat(FUNCTIONS)
                sections.extend(self.functions())
            elif self.current_token.type == EXECUTION:
                self.eat(EXECUTION)
                sections.extend(self.execution())

        return Program(sections, self.lexer.line_count)

    @restorable
    def check_function(self):
        self.eat(TYPE)
        self.eat(ID)
        return self.current_token.type == LPAREN

    def libraries(self):
        """
        libraries					: LBRACKET (empty | include_library*) RBRACKET
        """
        libs = []
        self.eat(LBRACKET)
        while self.current_token.type == ARROW:
            libs.append(self.include_library())
        self.eat(RBRACKET)
        return libs

    def include_library(self):
        """
        include_library 			: ARROW ID
        """
        self.eat(ARROW)
        library = self.current_token
        self.eat(ID)

        return Library(library.value, self.lexer.line_count)

    def functions(self):
        """
        functions 					: LBRACKET (empty | function_implementation*) RBRACKET
        """
        self.eat(LBRACKET)
        functions = []

        while self.current_token.type is not RBRACKET:
            functions.append(self.function_implementation())
        self.eat(RBRACKET)
        return functions

    def execution(self):
        """
        execution					: LBRACKET statement_list RBRACKET
        """
        self.eat(LBRACKET)
        statements = []

        while self.current_token.type is not RBRACKET:
            statements.extend(self.statement_list())
        self.eat(RBRACKET)
        return statements

    def function_implementation(self):
        """
        function_implementation 	: MONKEY ID COLON LPAREN parameters_list RPAREN ARROW (type_spec | void)
                                                                    LBRACKET function_body RBRACKET return_statement?

        return_statement            : RETURN variable
        """
        self.eat(MONKEY)
        fun_name = self.current_token.value
        self.eat(ID)
        self.eat(COLON)
        self.eat(LPAREN)
        args_list = Args(self.argument_list(), self.lexer.line_count)
        self.eat(RPAREN)
        self.eat(ARROW)

        ret_type = Type(self.current_token.value, self.lexer.line_count)
        self.eat(TYPE)

        self.eat(LBRACKET)
        stmts_list = []
        while self.current_token.type not in [RETURN, RBRACKET]:
            stmts_list.extend(self.statement_list())

        ret_val = Var('', self.lexer.line_count)
        ret_line = -1
        if self.current_token.type == RETURN:
            ret_line = self.lexer.line_count
            self.eat(RETURN)
            ret_val = Var(self.current_token.value, self.lexer.line_count)
            self.eat(ID)
        self.eat(RBRACKET)

        return FunImpl(fun_name, args_list, Stmts(stmts_list, self.lexer.line_count),
                       Return(ret_type, ret_val, ret_line), self.lexer.line_count)

    def argument_list(self):
        """
        parameters_list				: empty | param (COMMA param)*
        """
        params = []

        while self.current_token.type != RPAREN:
            type_node = Type(self.current_token.value, self.lexer.line_count)
            self.eat(TYPE)
            var_node = Var(self.current_token.value, self.lexer.line_count)
            self.eat(ID)

            params.append(VarDecl(type_node, var_node, self.lexer.line_count))

            if self.current_token.type == COMMA:
                self.eat(COMMA)

        return params

    def statement_list(self):
        """
        statement_list              : var_declaration
                                    | assignment_statement
                                    | function_call
                                    | condition_statement
                                    | loop_statement
                                    | return_statement
                                    | empty
        """
        statements = []

        if self.current_token.type == TYPE:
            statements.extend(self.var_declaration_list())
        elif self.current_token.type == ID:
            var_node = Var(self.current_token.value, self.lexer.line_count)
            self.eat(ID)
            while self.current_token.type == ASSIGN:
                statements.append(self.var_assignment_statement(var_node))
        elif self.current_token.type == COND:
            statements.append(self.condition_statement())
        elif self.current_token.type == LOOP:
            statements.append(self.loop_statement())
        elif self.current_token.type == MONKEY:
            statements.append(self.function_call())

        return statements

    def var_declaration_list(self):
        """
        var_declaration_list        : var_declaration*
        var_declaration 	       	: type_spec var
        """
        declarations = []

        while self.current_token.type == TYPE:
            type_node = Type(self.current_token.value, self.lexer.line_count)
            self.eat(TYPE)
            var_node = Var(self.current_token.value, self.lexer.line_count)
            self.eat(ID)

            declarations.extend(self.var_declaration(type_node, var_node))

        return declarations

    def var_assignment_statement(self, var_node):
        """
        assignment_statement        : variable ASSIGN (expr | bool_expr | function_call | STRING)
        """
        self.eat(ASSIGN)

        if self.is_bool_expr():
            return Assign(var_node, self.bool_expr(), self.lexer.line_count)
        elif self.current_token.type == STRING:
            return Assign(var_node, self.string_expr(), self.lexer.line_count)
        elif self.current_token.type == MONKEY:
            return Assign(var_node, self.function_call(), self.lexer.line_count)
        else:
            return Assign(var_node, self.expr(), self.lexer.line_count)

    def condition_statement(self):
        """
        condition_statement    : COND COLON LPAREN (bool_expr | func_call) RPAREN ARROW LBRACKET statement_list RBRACKET
        """
        self.eat(COND)
        self.eat(COLON)
        self.eat(LPAREN)
        if self.current_token.type == MONKEY:
            cond = self.function_call()
        else:
            cond = self.bool_expr()
        self.eat(RPAREN)
        self.eat(ARROW)

        self.eat(LBRACKET)
        statement_list = []
        while self.current_token.type != RBRACKET:
            statement_list.extend(self.statement_list())

        if len(statement_list) == 0:
            raise Exception('Error: Expected block in condition statement.\nLine: {}'.format(self.lexer.line_count))

        node = Cond(cond, Stmts(statement_list, self.lexer.line_count), self.lexer.line_count)
        self.eat(RBRACKET)

        return node

    def loop_statement(self):
        """
        loop_statement 				: LOOP COLON LPAREN bool_expr RPAREN ARROW LBRACKET statement_list RBRACKET
        """
        self.eat(LOOP)
        self.eat(COLON)
        self.eat(LPAREN)
        cond = self.bool_expr()
        self.eat(RPAREN)
        self.eat(ARROW)

        self.eat(LBRACKET)
        statement_list = []
        while self.current_token.type != RBRACKET:
            statement_list.extend(self.statement_list())

        if len(statement_list) == 0:
            raise Exception('Error: Expected block in loop statement.\nLine: {}'.format(self.lexer.line_count))

        node = Loop(cond, Stmts(statement_list, self.lexer.line_count), self.lexer.line_count)
        self.eat(RBRACKET)

        return node

    def function_call(self):
        """
        function_call: MONKEY ID DOT ID LPAREN (variable | INTEGER | STRING)?
                                                                        (COMMA (variable | INTEGER | STRING))* RPAREN
        """
        self.eat(MONKEY)
        lib_name = self.current_token.value
        self.eat(ID)
        self.eat(DOT)
        func_name = self.current_token.value
        self.eat(ID)

        self.eat(LPAREN)
        args = []
        while self.current_token.type != RPAREN:
            if self.current_token.type == STRING:
                var_node = Var(self.current_token.value, self.lexer.line_count)
                self.eat(STRING)
            elif self.current_token.type == INTEGER:
                var_node = Var(self.current_token.value, self.lexer.line_count)
                self.eat(INTEGER)
            else:
                var_node = Var(self.current_token.value, self.lexer.line_count)
                self.eat(ID)
            args.append(var_node)
            if self.current_token.type == COMMA:
                self.eat(COMMA)

        line_cnt = self.lexer.line_count
        self.eat(RPAREN)
        return FunCall(lib_name, func_name, args, line_cnt)

    def var_declaration(self, type_node, var_node):
        """
        var_declaration 	       	: type_spec var
        """
        declarations = []

        declarations.append(VarDecl(type_node, var_node, self.lexer.line_count))
        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)
            declarations.append(Assign(var_node, self.expr(), self.lexer.line_count))

        return declarations

    def factor(self):
        """
        factor                      : PLUS factor
                                    | MINUS factor
                                    | INTEGER
                                    | INT
                                    | FLOAT
                                    | LPAREN expr RPAREN
                                    | variable
                                    | function_call
        """
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token, self.lexer.line_count)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == MONKEY:
            return self.function_call()
        elif token.type == ID:
            self.eat(ID)
            return Var(token.value, self.lexer.line_count)

    def term(self):
        """
        term                        : factor ((MUL | NDIV | DIV | MOD) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MUL, NDIV, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == NDIV:
                self.eat(NDIV)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)
            else:
                self.error('*, /, // or %', token.type)

            node = BinOp(left=node, op=token, right=self.factor(), line_number=self.lexer.line_count)

        return node

    def expr(self):
        """
        expr                        : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error('+ or -', self.current_token.type)

            node = BinOp(left=node, op=token, right=self.expr(), line_number=self.lexer.line_count)

        return node

    def string_expr(self):
        """
        STRING ''
        """
        string_value = self.current_token.value
        self.eat(STRING)

        return String(string_value, self.lexer.line_count)

    def bool_expr(self):
        """
        bool 						: expr ((comparison_operator | (unar_operator? logical_operator)) expr))*

        bool_expr 					: unar_operator? bool
        """
        if self.current_token.type == INTEGER or self.current_token.type == ID:
            return self.bool_comparison_expr()
        else:
            return self.bool_logical_expr()

    def bool_comparison_expr(self):
        """
        comparison_operator			: LT | GT | LE | GE | EQ | NEQ
        """
        left = self.expr()
        op = self.current_token
        if op.type in (LESS, LESS_EQ, GREATER, GREATER_EQ, EQUAL, NOT_EQUAL):
            self.eat(op.type)
        else:
            self.error('comparison operator', op.type)

        return BinOp(left, op, self.expr(), self.lexer.line_count)

    def bool_logical_expr(self):
        """
        logical_operator			: AND | OR
        """
        if self.current_token.type == NOT:
            node = self.unar_expr()
        else:
            self.eat(LPAREN)
            node = self.bool_comparison_expr()
            self.eat(RPAREN)

        while self.current_token.type in (AND, OR):
            token = self.current_token
            self.eat(self.current_token.type)

            if self.current_token.type == NOT:
                un_token = self.current_token
                self.eat(NOT)
                self.eat(LPAREN)
                node = BinOp(node, token, UnOp(un_token, self.bool_comparison_expr(), self.lexer.line_count),
                             self.lexer.line_count)
                self.eat(RPAREN)

            else:
                self.eat(LPAREN)
                node = BinOp(node, token, self.bool_comparison_expr(), self.lexer.line_count)
                self.eat(RPAREN)

        return node

    def unar_expr(self):
        """
        unar_operator bool_expr
        """
        token = self.current_token
        self.eat(NOT)
        self.eat(LPAREN)
        node = self.bool_expr()
        self.eat(RPAREN)

        return UnOp(token, node, self.lexer.line_count)

    @restorable
    def is_bool_expr(self):
        """
        Checks if the following expression is boolean (has logical, comparison or unar operators).
        It is restorable, therefore does not remember the state.
        """
        res = False
        while self.current_token.type not in [ASSIGN, MONKEY, EOF, RBRACKET, COND, LOOP]:
            if self.current_token.type in (LESS, LESS_EQ, GREATER, GREATER_EQ, EQUAL, NOT_EQUAL, AND, OR, NOT):
                res = True
                self.eat(self.current_token.type)
                break
            self.eat(self.current_token.type)

        return res

    def parse(self):
        return self.program()
