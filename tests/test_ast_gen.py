"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation
"""

import pytest
from tests.utils import ASTGenerator

def test_001():
    source = """
void main() {
    printString("Hello, World!");
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(FuncCall(printString, [StringLiteral('Hello, World!')]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_002():
    source = """
int add(int x, int y) {
    return x + y;
}

int multiply(int x, int y) {
    return x * y;
}

void main() {
    auto a = readInt();
    auto b = readInt();
    
    auto sum = add(a, b);
    auto product = multiply(a, b);
    
    printInt(sum);
    printInt(product);
}
"""
    expected = "Program([FuncDecl(IntType(), add, [Param(IntType(), x), Param(IntType(), y)], [ReturnStmt(return BinaryOp(Identifier(x), +, Identifier(y)))]), FuncDecl(IntType(), multiply, [Param(IntType(), x), Param(IntType(), y)], [ReturnStmt(return BinaryOp(Identifier(x), *, Identifier(y)))]), FuncDecl(VoidType(), main, [], [VarDecl(auto, a = FuncCall(readInt, [])), VarDecl(auto, b = FuncCall(readInt, [])), VarDecl(auto, sum = FuncCall(add, [Identifier(a), Identifier(b)])), VarDecl(auto, product = FuncCall(multiply, [Identifier(a), Identifier(b)])), ExprStmt(FuncCall(printInt, [Identifier(sum)])), ExprStmt(FuncCall(printInt, [Identifier(product)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_003():
    source = """
void main() {
    auto n = readInt();
    auto i = 0;
    
    while (i < n) {
        printInt(i);
        ++i;
    }
    
    for (auto j = 0; j < n; ++j) {
        if (j % 2 == 0) {
            printInt(j);
        }
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(auto, n = FuncCall(readInt, [])), VarDecl(auto, i = IntLiteral(0)), WhileStmt(while BinaryOp(Identifier(i), <, Identifier(n)) do BlockStmt([ExprStmt(FuncCall(printInt, [Identifier(i)])), ExprStmt(PrefixOp(++Identifier(i)))])), ForStmt(for VarDecl(auto, j = IntLiteral(0)); BinaryOp(Identifier(j), <, Identifier(n)); PrefixOp(++Identifier(j)) do BlockStmt([IfStmt(if BinaryOp(BinaryOp(Identifier(j), %, IntLiteral(2)), ==, IntLiteral(0)) then BlockStmt([ExprStmt(FuncCall(printInt, [Identifier(j)]))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_004():
    source = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main() {
    auto num = readInt();
    auto result = factorial(num);
    printInt(result);
}
"""
    expected = "Program([FuncDecl(IntType(), factorial, [Param(IntType(), n)], [IfStmt(if BinaryOp(Identifier(n), <=, IntLiteral(1)) then BlockStmt([ReturnStmt(return IntLiteral(1))]), else BlockStmt([ReturnStmt(return BinaryOp(Identifier(n), *, FuncCall(factorial, [BinaryOp(Identifier(n), -, IntLiteral(1))])))]))]), FuncDecl(VoidType(), main, [], [VarDecl(auto, num = FuncCall(readInt, [])), VarDecl(auto, result = FuncCall(factorial, [Identifier(num)])), ExprStmt(FuncCall(printInt, [Identifier(result)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_005():
    source = """
void main() {
    // With auto and initialization
    auto x = readInt();
    auto y = readFloat();
    auto name = readString();
    
    // With auto without initialization
    auto sum;
    sum = x + y;              // sum: float (inferred from first usage - assignment)
    
    // With explicit type and initialization
    int count = 0;
    float total = 0.0;
    string greeting = "Hello, ";
    
    // With explicit type without initialization
    int i;
    float f;
    i = readInt();            // assignment to int
    f = readFloat();          // assignment to float
    
    printFloat(sum);
    printString(greeting);
    printString(name);
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(auto, x = FuncCall(readInt, [])), VarDecl(auto, y = FuncCall(readFloat, [])), VarDecl(auto, name = FuncCall(readString, [])), VarDecl(auto, sum), ExprStmt(AssignExpr(Identifier(sum) = BinaryOp(Identifier(x), +, Identifier(y)))), VarDecl(IntType(), count = IntLiteral(0)), VarDecl(FloatType(), total = FloatLiteral(0.0)), VarDecl(StringType(), greeting = StringLiteral('Hello, ')), VarDecl(IntType(), i), VarDecl(FloatType(), f), ExprStmt(AssignExpr(Identifier(i) = FuncCall(readInt, []))), ExprStmt(AssignExpr(Identifier(f) = FuncCall(readFloat, []))), ExprStmt(FuncCall(printFloat, [Identifier(sum)])), ExprStmt(FuncCall(printString, [Identifier(greeting)])), ExprStmt(FuncCall(printString, [Identifier(name)]))])])"
    assert str(ASTGenerator(source).generate()) == expected
    
def test_006():
    source = """
void main() {
    switch(1) {
        default: d = 4; b = 2; c = 3;
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch IntLiteral(1) cases [], default DefaultStmt(default: [ExprStmt(AssignExpr(Identifier(d) = IntLiteral(4))), ExprStmt(AssignExpr(Identifier(b) = IntLiteral(2))), ExprStmt(AssignExpr(Identifier(c) = IntLiteral(3)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_007():
    source = """
void main() {}
main(int a) {}
int main(int a, ID b) {}
float main(float b) {}
string main(string b, int a, Z b) {}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], []), FuncDecl(auto, main, [Param(IntType(), a)], []), FuncDecl(IntType(), main, [Param(IntType(), a), Param(StructType(ID), b)], []), FuncDecl(FloatType(), main, [Param(FloatType(), b)], []), FuncDecl(StringType(), main, [Param(StringType(), b), Param(IntType(), a), Param(StructType(Z), b)], [])])"
    assert str(ASTGenerator(source).generate()) == expected
    
def test_008():
    source = """
void main() {
    a = 1;
    a = b = c;
    a.b.d = c = e;
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(AssignExpr(Identifier(a) = IntLiteral(1))), ExprStmt(AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = Identifier(c)))), ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier(a).b).d) = AssignExpr(Identifier(c) = Identifier(e))))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_009():
    source = """
void main() {
    switch(a) {
        case 1: b = 2;
        default: d = 4;
        case 2: c = 3;
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(a) cases [CaseStmt(case IntLiteral(1): [ExprStmt(AssignExpr(Identifier(b) = IntLiteral(2)))]), CaseStmt(case IntLiteral(2): [ExprStmt(AssignExpr(Identifier(c) = IntLiteral(3)))])], default DefaultStmt(default: [ExprStmt(AssignExpr(Identifier(d) = IntLiteral(4)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected
    
def test_010():
    source = """
void main() {
    switch(x) {
        case 1: d = 4; b = 2; c = 3;
        case 2: y = 3;
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(AssignExpr(Identifier(d) = IntLiteral(4))), ExprStmt(AssignExpr(Identifier(b) = IntLiteral(2))), ExprStmt(AssignExpr(Identifier(c) = IntLiteral(3)))]), CaseStmt(case IntLiteral(2): [ExprStmt(AssignExpr(Identifier(y) = IntLiteral(3)))])])])])"
    assert str(ASTGenerator(source).generate()) == expected
    
def test_011():
    source = """
void main() {
    for (;;) continue;
    for (a.b=1;a.b;) {}
    for (auto a = 1; ; ) {return;}
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; None; None do ContinueStmt()), ForStmt(for ExprStmt(AssignExpr(MemberAccess(Identifier(a).b) = IntLiteral(1))); MemberAccess(Identifier(a).b); None do BlockStmt([])), ForStmt(for VarDecl(auto, a = IntLiteral(1)); None; None do BlockStmt([ReturnStmt(return)]))])])"
    assert str(ASTGenerator(source).generate()) == str(expected)
    
    
def test_012():
    source = """
void main() {
    for(;;a++) {}
    for (;;++a) {}
    for (;;a.b=2) {}
    for (a=1;;a.b=2) {}
}
""" 
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; None; PostfixOp(Identifier(a)++) do BlockStmt([])), ForStmt(for None; None; PrefixOp(++Identifier(a)) do BlockStmt([])), ForStmt(for None; None; AssignExpr(MemberAccess(Identifier(a).b) = IntLiteral(2)) do BlockStmt([])), ForStmt(for ExprStmt(AssignExpr(Identifier(a) = IntLiteral(1))); None; AssignExpr(MemberAccess(Identifier(a).b) = IntLiteral(2)) do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected