grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: (struct_decl | function_decl)* EOF;

// Struct
struct_decl: STRUCT ID LBRACE list_attribute? RBRACE SEMI;
list_attribute: attribute list_attribute | attribute;
attribute: type ID SEMI;
type: INT | FLOAT | STRING | ID; // primitive and struct type

// Function
function_decl: return_type? ID LPAREN list_parameter? RPAREN block_statement;
return_type: VOID | INT | FLOAT | STRING | ID; // void, primitive and struct type
list_parameter: parameter COMMA list_parameter | parameter;
parameter: type ID; // primitive and struct type

// Member Access
member_access: expression10 DOT member;
member: member DOT ID | ID;

// Expression
list_expression: expression COMMA list_expression | expression;
expression: (ID | member_access) ASSIGN expression | expression1; // assign expression
expression1: expression1 (OR) expression2 | expression2;
expression2: expression2 (AND) expression3 | expression3;
expression3: expression3 (EQ | NE) expression4 | expression4;
expression4: expression4 (LT | GT | LE | GE) expression5 | expression5;
expression5: expression5 (ADD | SUB) expression6 | expression6;
expression6: expression6 (MUL | DIV | MODULE) expression7 | expression7;
expression7: (NOT | ADD | SUB) expression7 | expression8;
expression8: (INCREMENT | DECREMENT) expression8 | expression9;
expression9: expression9 (INCREMENT | DECREMENT) | expression10;
expression10: expression10 (DOT) ID | expression11;
expression11: INT_LIT
            | FLOAT_LIT
            | STRING_LIT
            | ID (LPAREN list_expression? RPAREN)? // id or call function
            | LBRACE list_expression? RBRACE // struct
            | LPAREN list_expression RPAREN; // add ( ) increase priority

// Statement
list_statement: statement list_statement | statement;
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

var_statement: var_type ID (ASSIGN expression)?;
var_type: AUTO | INT | FLOAT | STRING | ID;

if_statement: IF LPAREN expression RPAREN statement (ELSE statement)?;

while_statement: WHILE LPAREN expression RPAREN statement;

for_statement: FOR LPAREN init? SEMI expression? SEMI update? RPAREN statement;
init: var_statement | (ID | member_access) ASSIGN expression;
update: (ID | member_access) ASSIGN expression | (INCREMENT | DECREMENT) expression8 | expression9 (INCREMENT | DECREMENT);

switch_statement: SWITCH LPAREN expression RPAREN LBRACE list_case? default_case? list_case? RBRACE;
list_case: case list_case | case;
case: CASE expression COLON list_statement?;
default_case: DEFAULT COLON list_statement?;

break_statement: BREAK;

continue_statement: CONTINUE;

block_statement: LBRACE list_statement? RBRACE;

expression_statement: expression;

return_statement: RETURN expression?;

// --- LEXER --- //
// Whitespace and comment
WS              : [ \f\r\n\t]+ -> skip;
LINE_COMMENT    : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT   : '/*' .*? '*/' -> skip; // None greedy

// Assign
ASSIGN      : '=';
INCREMENT   : '++';
DECREMENT   : '--';

// Operator
ADD     : '+';
SUB     : '-';
MUL     : '*';
DIV     : '/';
MODULE  : '%';

// Comparision
EQ  : '==';
NE  : '!=';
LT  : '<';
GT  : '>';
LE  : '<=';
GE  : '>=';

// Logic
OR  : '||';
AND : '&&';
NOT : '!';

// Separator
LBRACE  : '{';
RBRACE  : '}';
LPAREN  : '(';
RPAREN  : ')';
SEMI    : ';';
COLON   : ':';
COMMA   : ',';
DOT     : '.';

// Keyword
AUTO        : 'auto';
BREAK       : 'break';
CASE        : 'case';
CONTINUE    : 'continue';
DEFAULT     : 'default';
ELSE        : 'else';
FLOAT       : 'float';
FOR         : 'for';
IF          : 'if';
INT         : 'int';
RETURN      : 'return';
STRING      : 'string';
SWITCH      : 'switch';
STRUCT      : 'struct';
VOID        : 'void';
WHILE       : 'while';

// Literal
ID          : [a-zA-Z_] [a-zA-Z0-9_]*;
INT_LIT     : [0-9]+;
FLOAT_LIT   : [0-9]+ [eE] [+-]? [0-9]+
            | [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)?
            | [0-9]* '.' [0-9]+ ([eE] [+-]? [0-9]+)?;
STRING_LIT  : '"' (NORMAL_CHAR | LEGAL_ESCAPE_CHAR)* '"' { self.text = self.text[1:-1]};

// Error
ILLEGAL_ESCAPE: '"' (NORMAL_CHAR | LEGAL_ESCAPE_CHAR)* ILLEGAL_ESCAPE_CHAR { self.text = self.text[1:] };
UNCLOSE_STRING: '"' (NORMAL_CHAR | LEGAL_ESCAPE_CHAR)*  '\\'? ([\r\n]* | EOF) { self.text = self.text.rstrip('\r\n')[1:] };
ERROR_CHAR: .;

fragment NORMAL_CHAR: ~[\r\n\\"];
fragment LEGAL_ESCAPE_CHAR: '\\' [bfrnt\\"];
fragment ILLEGAL_ESCAPE_CHAR: '\\' ~[\r\nbfrnt\\"];