"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """
        program: (struct_decl | function_decl)* EOF;
    """
    def visitProgram(self, ctx: TyCParser.ProgramContext):
        return Program([self.visit(child) for child in ctx.children if isinstance(child, TyCParser.Struct_declContext) or isinstance(child, TyCParser.Function_declContext)])
    
    """
        struct_decl: STRUCT ID LBRACE list_attribute? RBRACE SEMI;
        list_attribute: attribute list_attribute | attribute;
        attribute: type ID SEMI;
        type: INT | FLOAT | STRING | ID; // primitive and struct type
    """
    def visitStruct_decl(self, ctx: TyCParser.Struct_declContext):
        name = ctx.ID().getText()
        members = self.visit(ctx.list_attribute()) if ctx.list_attribute() else []
        return StructDecl(name, members)

    def visitList_attribute(self, ctx: TyCParser.List_attributeContext):
        return [self.visit(ctx.attribute())] + (self.visit(ctx.list_attribute()) if ctx.list_attribute() else [])

    def visitAttribute(self, ctx: TyCParser.AttributeContext):
        return MemberDecl(self.visit(ctx.type_()), ctx.ID().getText())
    
    def visitType(self, ctx: TyCParser.TypeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return StructType(ctx.ID().getText())

    """
        function_decl: return_type? ID LPAREN list_parameter? RPAREN block_statement;
        return_type: VOID | INT | FLOAT | STRING | ID; // void, primitive and struct type
        list_parameter: parameter COMMA list_parameter | parameter;
        parameter: type ID; // primitive and struct type
    """
    def visitFunction_decl(self, ctx: TyCParser.Function_declContext):
        return_type = self.visit(ctx.return_type()) if ctx.return_type() else None
        name = ctx.ID().getText()
        params = self.visit(ctx.list_parameter()) if ctx.list_parameter() else []
        body = self.visit(ctx.block_statement())
        return FuncDecl(return_type, name, params, body)
    
    def visitReturn_type(self, ctx: TyCParser.Return_typeContext):
        if ctx.VOID():
            return VoidType()
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return StructType(ctx.ID().getText())

    def visitList_parameter(self, ctx: TyCParser.List_parameterContext):
        return [self.visit(ctx.parameter())] + (self.visit(ctx.list_parameter()) if ctx.list_parameter() else [])

    def visitParameter(self, ctx: TyCParser.ParameterContext):
        return Param(self.visit(ctx.type_()), ctx.ID().getText())
    
    """
        member_access: expression10 DOT member;
        member: member DOT ID | ID;
    """
    def visitMember_access(self, ctx: TyCParser.Member_accessContext):
        obj = self.visit(ctx.expression10())
        member = self.visit(ctx.member())
        for name in member:
            obj = MemberAccess(obj, name)
        return obj

    def visitMember(self, ctx: TyCParser.MemberContext):
        return self.visit(ctx.member()) + [ctx.ID().getText()] if ctx.DOT() else [ctx.ID().getText()]

    """
        list_expression: expression COMMA list_expression | expression;
    """
    def visitList_expression(self, ctx: TyCParser.List_expressionContext):
        return [self.visit(ctx.expression())] + (self.visit(ctx.list_expression()) if ctx.list_expression() else [])

    """
        expression: (ID | member_access) ASSIGN expression | expression1; // assign expression
    """
    def visitExpression(self, ctx: TyCParser.ExpressionContext):
        if ctx.ASSIGN():
            return AssignExpr(Identifier(ctx.ID().getText()), self.visit(ctx.expression())) if ctx.ID() else AssignExpr(self.visit(ctx.member_access()), self.visit(ctx.expression()))
        return self.visit(ctx.expression1())
    
    """
        expression1: expression1 (OR) expression2 | expression2;
    """
    def visitExpression1(self, ctx: TyCParser.Expression1Context):
        return BinaryOp(self.visit(ctx.expression1()), ctx.OR(), self.visit(ctx.expression2())) if ctx.OR() else self.visit(ctx.expression2())
    
    """
        expression2: expression2 (AND) expression3 | expression3;
    """
    def visitExpression2(self, ctx: TyCParser.Expression2Context):
        return BinaryOp(self.visit(ctx.expression2()), ctx.AND(), self.visit(ctx.expression3())) if ctx.AND() else self.visit(ctx.expression3())
    
    """
        expression3: expression3 (EQ | NE) expression4 | expression4;
    """
    def visitExpression3(self, ctx: TyCParser.Expression3Context):
        return BinaryOp(self.visit(ctx.expression3()), ctx.getChild(1).getText(), self.visit(ctx.expression4())) if ctx.getChildCount() == 3 else self.visit(ctx.expression4())
    
    """
        expression4: expression4 (LT | GT | LE | GE) expression5 | expression5;
    """
    def visitExpression4(self, ctx: TyCParser.Expression4Context):
        return BinaryOp(self.visit(ctx.expression4()), ctx.getChild(1).getText(), self.visit(ctx.expression5())) if ctx.getChildCount() == 3 else self.visit(ctx.expression5())
    
    """
        expression5: expression5 (ADD | SUB) expression6 | expression6;
    """
    def visitExpression5(self, ctx: TyCParser.Expression5Context):
        return BinaryOp(self.visit(ctx.expression5()), ctx.getChild(1).getText(), self.visit(ctx.expression6())) if ctx.getChildCount() == 3 else self.visit(ctx.expression6())

    """
        expression6: expression6 (MUL | DIV | MODULE) expression7 | expression7;
    """
    def visitExpression6(self, ctx: TyCParser.Expression6Context):
        return BinaryOp(self.visit(ctx.expression6()), ctx.getChild(1).getText(), self.visit(ctx.expression7())) if ctx.getChildCount() == 3 else self.visit(ctx.expression7())
    
    """
        expression7: (NOT | ADD | SUB) expression7 | expression8;
    """
    def visitExpression7(self, ctx: TyCParser.Expression7Context):
        return PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.expression7())) if ctx.getChildCount() == 2 else self.visit(ctx.expression8())
    
    """
        expression8: (INCREMENT | DECREMENT) expression8 | expression9;
    """
    def visitExpression8(self, ctx: TyCParser.Expression8Context):
        return PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.expression8())) if ctx.getChildCount() == 2 else self.visit(ctx.expression9())
    
    """
        expression9: expression9 (INCREMENT | DECREMENT) | expression10;
    """
    def visitExpression9(self, ctx: TyCParser.Expression9Context):
        return PostfixOp(ctx.getChild(1).getText(), self.visit(ctx.expression9())) if ctx.getChildCount() == 2 else self.visit(ctx.expression10())
    
    """
        expression10: expression10 (DOT) ID | expression11;
    """
    def visitExpression10(self, ctx: TyCParser.Expression10Context):
        return MemberAccess(self.visit(ctx.expression10()), ctx.ID().getText()) if ctx.DOT() else self.visit(ctx.expression11())
    
    """
        expression11: INT_LIT
                    | FLOAT_LIT
                    | STRING_LIT
                    | ID (LPAREN list_expression? RPAREN)? // id or call function
                    | LBRACE list_expression? RBRACE // struct
                    | LPAREN list_expression RPAREN; // add ( ) increase priority
    """
    def visitExpression11(self, ctx: TyCParser.Expression11Context):
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.ID() and ctx.LPAREN() and ctx.RPAREN():
            return FuncCall(ctx.ID().getText(), self.visit(ctx.list_expression()) if ctx.list_expression() else [])
        elif ctx.ID() and not ctx.LPAREN() and not ctx.RPAREN():
            return Identifier(ctx.ID().getText())
        elif ctx.LBRACE() and ctx.RBRACE():
            return StructLiteral(self.visit(ctx.list_expression()) if ctx.list_expression() else [])
        else:
            return self.visit(ctx.list_expression())[0] if len(self.visit(ctx.list_expression())) > 0 else None

    """
        list_statement: statement list_statement | statement;
    """
    def visitList_statement(self, ctx: TyCParser.List_statementContext):
        return [self.visit(ctx.statement())] + (self.visit(ctx.list_statement()) if ctx.list_statement() else [])

    """
        statement: var_statement SEMI
                 | if_statement
                 | while_statement
                 | for_statement
                 | switch_statement
                 | break_statement SEMI
                 | continue_statement SEMI
                 | block_statement
                 | expression_statement SEMI
                 | return_statement SEMI;
    """
    def visitStatement(self, ctx: TyCParser.StatementContext):
        return self.visit(ctx.getChild(0))

    """
        var_statement: var_type ID (ASSIGN expression)?;
        var_type: AUTO | INT | FLOAT | STRING | ID;
    """
    def visitVar_statement(self, ctx: TyCParser.Var_statementContext):
        var_type = self.visit(ctx.var_type())
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expression()) if ctx.expression() else None
        return VarDecl(var_type, name, init_value)
    
    def visitVar_type(self, ctx: TyCParser.Var_typeContext):
        if ctx.AUTO():
            return None
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return StructType(ctx.ID().getText())

    """
        if_statement: IF LPAREN expression RPAREN statement (ELSE statement)?;
    """
    def visitIf_statement(self, ctx: TyCParser.If_statementContext):
        condition = self.visit(ctx.expression())
        then_stmt = self.visit(ctx.statement(0))
        else_stmt = self.visit(ctx.statement(1)) if ctx.ELSE() else None
        return IfStmt(condition, then_stmt, else_stmt)

    """
        while_statement: WHILE LPAREN expression RPAREN statement;
    """
    def visitWhile_statement(self, ctx: TyCParser.While_statementContext):
        return WhileStmt(self.visit(ctx.expression()), self.visit(ctx.statement()))
    
    """
        for_statement: FOR LPAREN init? SEMI expression? SEMI update? RPAREN statement;
        init: var_statement | (ID | member_access) ASSIGN expression;
        update: (ID | member_access) ASSIGN expression | (INCREMENT | DECREMENT) expression8 | expression9 (INCREMENT | DECREMENT);
    """
    def visitFor_statement(self, ctx: TyCParser.For_statementContext):
        init = self.visit(ctx.init()) if ctx.init() else None
        condition = self.visit(ctx.expression()) if ctx.expression() else None
        update = self.visit(ctx.update()) if ctx.update() else None
        body = self.visit(ctx.statement())
        return ForStmt(init, condition, update, body)

    def visitInit(self, ctx: TyCParser.InitContext):
        if ctx.var_statement():
            return self.visit(ctx.var_statement())
        return ExprStmt(AssignExpr(Identifier(ctx.ID().getText()), self.visit(ctx.expression()))) if ctx.ID() else ExprStmt(AssignExpr(self.visit(ctx.member_access()), self.visit(ctx.expression())))
    
    def visitUpdate(self, ctx: TyCParser.UpdateContext):
        if ctx.ASSIGN():
            return AssignExpr(Identifier(ctx.ID().getText()), self.visit(ctx.expression())) if ctx.ID() else AssignExpr(self.visit(ctx.member_access()), self.visit(ctx.expression()))
        else:
            operator = ctx.INCREMENT().getText() if ctx.INCREMENT() else ctx.DECREMENT().getText()
            return PrefixOp(operator, self.visit(ctx.expression8())) if ctx.expression8() else PostfixOp(operator, self.visit(ctx.expression9()))

    """
        switch_statement: SWITCH LPAREN expression RPAREN LBRACE list_case? default_case? list_case? RBRACE;
        list_case: case list_case | case;
        case: CASE expression COLON list_statement?;
        default_case: DEFAULT COLON list_statement?;
    """
    def visitSwitch_statement(self, ctx: TyCParser.Switch_statementContext):
        expr = self.visit(ctx.expression())
        first_list_case = self.visit(ctx.list_case()[0]) if len(ctx.list_case()) >= 1 else []
        default_case = self.visit(ctx.default_case()) if ctx.default_case() else None
        second_list_case = self.visit(ctx.list_case()[1]) if len(ctx.list_case()) >= 2 else []
        cases = first_list_case + second_list_case
        return SwitchStmt(expr, cases, default_case)

    def visitList_case(self, ctx: TyCParser.List_caseContext):
        return [self.visit(ctx.case())] + (self.visit(ctx.list_case()) if ctx.list_case() else [])

    def visitCase(self, ctx: TyCParser.CaseContext):
        return CaseStmt(self.visit(ctx.expression()), self.visit(ctx.list_statement()) if ctx.list_statement() else [])
    
    def visitDefault_case(self, ctx: TyCParser.Default_caseContext):
        return DefaultStmt(self.visit(ctx.list_statement()) if ctx.list_statement() else [])
    
    """
        break_statement: BREAK;
    """
    def visitBreak_statement(self, ctx: TyCParser.Break_statementContext):
        return BreakStmt()

    """
        continue_statement: CONTINUE;
    """
    def visitContinue_statement(self, ctx: TyCParser.Continue_statementContext):
        return ContinueStmt()

    """
        block_statement: LBRACE list_statement? RBRACE;
    """
    def visitBlock_statement(self, ctx: TyCParser.Block_statementContext):
        return BlockStmt(self.visit(ctx.list_statement()) if ctx.list_statement() else [])

    """
        expression_statement: expression;
    """
    def visitExpression_statement(self, ctx: TyCParser.Expression_statementContext):
        return ExprStmt(self.visit(ctx.expression()))
    
    """
        return_statement: RETURN expression?;
    """
    def visitReturn_statement(self, ctx: TyCParser.Return_statementContext):
        return ReturnStmt(self.visit(ctx.expression()) if ctx.expression() else None)