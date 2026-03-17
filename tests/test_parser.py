"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


def test_001():
    source = """
void main() {
    printString("Hello, World!");
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

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
    expected = "success"
    assert Parser(source).parse() == expected

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
    expected = "success"
    assert Parser(source).parse() == expected

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
    expected = "success"
    assert Parser(source).parse() == expected

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
    
    // Note: String concatenation is NOT supported
    // This is because + operator applies to int or float, not string
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    source ="""
struct Point {
    int x;
    int y;
};

struct Person {
    string name;
    int age;
    float height;
};

void main() {
    // Struct variable declaration without initialization
    Point p1;
    p1.x = 10;
    p1.y = 20;
    
    // Struct variable declaration with initialization
    Point p2 = {30, 40};
    
    // Access and modify struct members
    printInt(p2.x);
    printInt(p2.y);
    
    // Struct assignment
    p1 = p2;  // Copy all members
    
    // Person struct usage
    Person person1 = {"John", 25, 1.75};
    printString(person1.name);
    printInt(person1.age);
    printFloat(person1.height);
    
    // Modify struct members
    person1.age = 26;
    person1.height = 1.76;
    
    // Using struct with auto
    auto p3 = p2;  // p3: Point (inferred from assignment)
    printInt(p3.x);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_007():
    source = """
void main() {
"""
    expected = "Error on line 3 col 0: <EOF>"
    assert Parser(source).parse() == expected

def test_008():
    source = """
void main {}
"""
    expected = "Error on line 2 col 10: {"
    assert Parser(source).parse() == expected

def test_009():
    source = """
void main () {
    return 1;
    return 1.0;
    return "votien";
    return {1, 2, 1.0}; // struct lit
    return {};
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_010():
    source = """
void main () {
    return a = b = 3;
    return (a = b) + 7;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_011():
    source = """
void main () {
    return 1 || 2 || 3;
    return a = "votien" || 3;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_012():
    source = """
void main () {
    return 1 && 2 && 3;
    return 1.0 || "votien" && 3;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_013():
    source = """
void main () {
    return 1 == 2 != 3;
    return 1.0 && "votien" == 3 && 2 != 2;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_014():
    source = """
void main () {
    return 1 >= 2 < 3 <= 4 > 5;
    return 1.0 == "votien" >= 3 != 2 > 2;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_015():
    source = """
void main () {
    return 1 + 2 - 3;
    return 1 + 2 > 1 - 3;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_016():
    source = """
void main () {
    return 1 * 2 / 3 % 4;
    return 1 + 2 * 3;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_017():
    source = """
void main () {
    return a.b.c.d.g.h;
    return a * a.b.c;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_018():
    source = """
void main () {
    return !!-+!-+a;
    return !-+a.b.c;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_019():
    source = """
void main () {
    return ++--++a;
    return !++a;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_020():
    source = """
void main () {
    return ++!a;
}
"""
    expected = "Error on line 3 col 13: !"
    assert Parser(source).parse() == expected

def test_021():
    source = """
void main () {
    return +++a;
}
"""
    expected = "Error on line 3 col 13: +"
    assert Parser(source).parse() == expected

def test_022():
    source = """
void main () {
    return a++--++--;
    return ++--++--a++--++--;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_023():
    source = """
void main () {
    return ++(+a) * (a / (c));
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_024():
    source = """
void main () {
    return {1+3, "s"++};
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_025():
    source = """
void main () {
    return foo() + foo(1) + foo(1*2++, 1 && 2, foo());
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_026():
    source = """
void main () {
    foo(;
}
"""
    expected = "Error on line 3 col 8: ;"
    assert Parser(source).parse() == expected

def test_027():
    source = """
void main () {
    foo(a b);
}
"""
    expected = "Error on line 3 col 10: b"
    assert Parser(source).parse() == expected

def test_028():
    source = """
void main () {
    a.foo();
}
"""
    expected = "Error on line 3 col 9: ("
    assert Parser(source).parse() == expected

def test_029():
    source = """
void main () {
    foo.a.b;
    ++a.b;
    a.b++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_030():
    source = """
void main () {
    +a++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_031():
    source = """
void main () {
    int a = 1;
    int a;
    float b = 1;
    string b = 1 + 2 / 3;
    auto b = 1;
    auto b;
    ID b = foo();
    ID b;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_032():
    source = """
void main () {
    void a = 1;
}
"""
    expected = "Error on line 3 col 4: void"
    assert Parser(source).parse() == expected

def test_033():
    source = """
void main () {
    void a;
}
"""
    expected = "Error on line 3 col 4: void"
    assert Parser(source).parse() == expected

def test_034():
    source = """
void main () {
    int a, b;
}
"""
    expected = "Error on line 3 col 9: ,"
    assert Parser(source).parse() == expected

def test_035():
    source = """
void main () {
    int a = e = 3;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_036():
    source = """
void main () {
    int a
}
"""
    expected = "Error on line 4 col 0: }"
    assert Parser(source).parse() == expected

def test_037():
    source = """
void main () {
    a = 2;
    a.b = foo() + a.b * 3;
    a.b.c.d = 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_038():
    source = """
void main () {
    ++a = 1;
}
"""
    expected = "Error on line 3 col 8: ="
    assert Parser(source).parse() == expected

def test_039():
    source = """
void main () {
    foo() = 1;
}
"""
    expected = "Error on line 3 col 10: ="
    assert Parser(source).parse() == expected

def test_040():
    source = """
void main () {
    if (1 + 2) continue;
    else break;

    if (a.b.c) {if (c.a) return;}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_041():
    source = """
void main () {
    if (1);
}
"""
    expected = "Error on line 3 col 10: ;"
    assert Parser(source).parse() == expected

def test_042():
    source = """
void main () {
    if (1) {} else;
}
"""
    expected = "Error on line 3 col 18: ;"
    assert Parser(source).parse() == expected

def test_042():
    source = """
void main () {
    if () {}
}
"""
    expected = "Error on line 3 col 8: )"
    assert Parser(source).parse() == expected

def test_043():
    source = """
void main () {
    int if;
}
"""
    expected = "Error on line 3 col 8: if"
    assert Parser(source).parse() == expected

def test_044():
    source = """
void main () {
    if (a) {} else if (2) {} else if (2) {} else {}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_045():
    source = """
void main () {
    while(1 > 2) continue;
    while(1 > 2) {return; break;}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_046():
    source = """
void main () {
    while() continue;
}
"""
    expected = "Error on line 3 col 10: )"
    assert Parser(source).parse() == expected

def test_047():
    source = """
void main () {
    return ;
    return 1 +2 *++3;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_048():
    source = """
 return ;
"""
    expected = "Error on line 2 col 1: return"
    assert Parser(source).parse() == expected

def test_048():
    source = """
void main () {
    1 +2 -++3+a.b.c;
    ;
}
"""
    expected = "Error on line 4 col 4: ;"
    assert Parser(source).parse() == expected

def test_049():
    source = """
void main () {
    {{{}}}
    {return; {break;}}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_050():
    source = """
void main () {
   {retrun; };
}
"""
    expected = "Error on line 3 col 13: ;"
    assert Parser(source).parse() == expected

def test_051():
    source = """
void main () {
   for(int a = 1 + 2; i > 2; a++) continue;
   for(a = a.b = 1; ; --a) a++;
   for(auto a = 1; i * 2; a = 2) {return ;}
   for(; ; ) {}
   for({1,2}.a = 1; ; (a+2).b = 2) a++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_052():
    source = """
void main () {
   for(break; ; ) continue;
}
"""
    expected = "Error on line 3 col 7: break"
    assert Parser(source).parse() == expected

def test_053():
    source = """
void main () {
   for(a=2;; ; ) continue;
}
"""
    expected = "Error on line 3 col 13: ;"
    assert Parser(source).parse() == expected

def test_054():
    source = """
void main () {
   for(; break ; ) continue;
}
"""
    expected = "Error on line 3 col 9: break"
    assert Parser(source).parse() == expected

def test_055():
    source = """
void main () {
   for(; break ; ) continue;
}
"""
    expected = "Error on line 3 col 9: break"
    assert Parser(source).parse() == expected

def test_056():
    source = """
void main () {
   for(a.b=2; ; ) continue;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_057():
    source = """
void main () {
   for(; ; -a) continue;
}
"""
    expected = "Error on line 3 col 11: -"
    assert Parser(source).parse() == expected

def test_058():
    source = """
void main () {
   for(; ; a.b=a.c.c=c()) continue;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_059():
    source = """
void main () {
   for(; ;);
}
"""
    expected = "Error on line 3 col 11: ;"
    assert Parser(source).parse() == expected

def test_060():
    source = """
void main () {
   for(; ;);
}
"""
    expected = "Error on line 3 col 11: ;"
    assert Parser(source).parse() == expected

def test_061():
    source = """
void main () {
    auto x = readInt();
    switch (x) {
        case 1:
            printInt(1);
        case 2:
            printInt(2);
        default:
            printInt(0);
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_062():
    source = """
void main () {
    int x = 10;
    switch (x) {
        case 1:
            printInt(1);
        case 2:
            printInt(2);
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_063():
    source = """
void main () {
    switch (1) {
        case :
            printInt(1);
    }
}
"""
    expected = "Error on line 4 col 13: :"
    assert Parser(source).parse() == expected

def test_064():
    source = """
void main () {
    switch () {
        case 1:
            printInt(1);
    }
}
"""
    expected = "Error on line 3 col 12: )"
    assert Parser(source).parse() == expected

def test_065():
    source = """
void main () {
    switch (1) {
        default
            printInt(0);
    }
}
"""
    expected = "Error on line 5 col 12: printInt"
    assert Parser(source).parse() == expected

def test_066():
    source = """
void main () {
    switch (1) {
        case 1 + 2 * "s":
            printInt(0);
            return ;
            break;
        default:
            printInt(0);
            {if(1){}}
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_067():
    source = """
void main () {
    switch (1 *3 / 4) {
        default:
            1;
        case 2:
             2;
    }

    switch (1 *3 / 4) {
        case 3:1;
        default:1;
        case 2: 2;
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_068():
    source = """
AAAA main (int a, int b) {return;}
void main3 () {}
ID main2 (int a) {return;}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_069():
    source = """
AAAA main (int a, b) {return;}
"""
    expected = "Error on line 2 col 19: )"
    assert Parser(source).parse() == expected

def test_070():
    source = """
AAAA main (int a) continue;
"""
    expected = "Error on line 2 col 18: continue"
    assert Parser(source).parse() == expected

def test_071():
    source = """
AAAA main (int a);
"""
    expected = "Error on line 2 col 17: ;"
    assert Parser(source).parse() == expected

def test_072():
    source = """
AAAA main (auto a){}
"""
    expected = "Error on line 2 col 11: auto"
    assert Parser(source).parse() == expected

def test_073():
    source = """
AAAA main (void a){}
"""
    expected = "Error on line 2 col 11: void"
    assert Parser(source).parse() == expected

def test_074():
    source = """
AAAA main (){};
"""
    expected = "Error on line 2 col 14: ;"
    assert Parser(source).parse() == expected

def test_075():
    source = """
AAAA main (){AAAA main (){}}
"""
    expected = "Error on line 2 col 23: ("
    assert Parser(source).parse() == expected

def test_076():
    source = """
struct ID {int a; ID b;};
int main (){}
struct ID1 {};
id main (){}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_077():
    source = """
struct ID {int a; ID b;}
"""
    expected = "Error on line 3 col 0: <EOF>"
    assert Parser(source).parse() == expected

def test_078():
    source = """
struct ID {auto a;}
"""
    expected = "Error on line 2 col 11: auto"
    assert Parser(source).parse() == expected

def test_079():
    source = """
struct ID {void a;}
"""
    expected = "Error on line 2 col 11: void"
    assert Parser(source).parse() == expected

def test_080():
    source = """
struct ID {int a}
"""
    expected = "Error on line 2 col 16: }"
    assert Parser(source).parse() == expected

def test_081():
    source = """
struct ID {int a;;}
"""
    expected = "Error on line 2 col 17: ;"
    assert Parser(source).parse() == expected

def test_082():
    source = """
struct ID {int a, b;}
"""
    expected = "Error on line 2 col 16: ,"
    assert Parser(source).parse() == expected

def test_083():
    source = """
struct ID {int a; int main(){}}
"""
    expected = "Error on line 2 col 26: ("
    assert Parser(source).parse() == expected

def test_084():
    source = """
struct ID {struct ID{}}
"""
    expected = "Error on line 2 col 11: struct"
    assert Parser(source).parse() == expected

def test_085():
    source = """
int a = 2;
"""
    expected = "Error on line 2 col 6: ="
    assert Parser(source).parse() == expected

def test_086():
    source = """
    for(;;);
"""
    expected = "Error on line 2 col 4: for"
    assert Parser(source).parse() == expected

def test_087():
    source = """
void main(){for(;;)}
"""
    expected = "Error on line 2 col 19: }"
    assert Parser(source).parse() == expected


def test_088():
    source = """
void main(){
    case 1:
        printInt(1);
}
"""
    expected = "Error on line 3 col 4: case"
    assert Parser(source).parse() == expected


def test_089():
    source = """
void main(){
    T a = b;
    True a = b;
    true c = f;
    F b = T;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_090():
    source = """
void main(){
    auto a = 1 ** 3;
}
"""
    expected = "Error on line 3 col 16: *"
    assert Parser(source).parse() == expected

def test_091():
    source = """
void main(){
    auto a := 3;
}
"""
    expected = "Error on line 3 col 11: :"
    assert Parser(source).parse() == expected

def test_092():
    source = """
struct A {};
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_093():
    source = """
void main(){
    auto a := {};
}
"""
    expected = "Error on line 3 col 11: :"
    assert Parser(source).parse() == expected

def test_094():
    source = """
void main(){
    switch (x) { }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_095():
    source = """
main(){}
void main () {}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_096():
    source = """
main(){for(b=a=c; i * 2; a.bc = a = 3) {return ;}}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_097():
    source = """
main(){for(a * 3; i * 2; a++ = 2 = 3) {return ;}}
"""
    expected = "Error on line 2 col 13: *"
    assert Parser(source).parse() == expected


def test_098():
    source = """
main(){for({1,2}; i * 2; a++ = 2 = 3) {return ;}}
"""
    expected = "Error on line 2 col 16: ;"
    assert Parser(source).parse() == expected


def test_099():
    source = """
main(){; i++; a + 2) {return ;}}
"""
    expected = "Error on line 2 col 7: ;"
    assert Parser(source).parse() == expected

def test_100():
    source = """
main(){return {{}, 1 ++};}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_101():
    source = """
main(){return {{}, 1 ++};}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_102():
    source = """
auto main(){}
"""
    expected = "Error on line 2 col 0: auto"
    assert Parser(source).parse() == expected

def test_103():
    source = """
main(){;}
"""
    expected = "Error on line 2 col 7: ;"
    assert Parser(source).parse() == expected

def test_104():
    source = """
main(){};
"""
    expected = "Error on line 2 col 8: ;"
    assert Parser(source).parse() == expected

def test_105():
    source = """
main(){
    int a = .;
}
"""
    expected = "Error on line 3 col 12: ."
    assert Parser(source).parse() == expected

def test_106():
    source = """
int a = 1;
"""
    expected = "Error on line 2 col 6: ="
    assert Parser(source).parse() == expected

def test_107():
    source = """
struct A{
    main() {}
}
"""
    expected = "Error on line 3 col 8: ("
    assert Parser(source).parse() == expected

def test_108():
    source = """
void main () {
    auto x = readInt();
    switch (x) {
        default:
            printInt(0);
        default:
            printInt(0);
    }
}
"""
    expected = "Error on line 7 col 8: default"
    assert Parser(source).parse() == expected


def test_109():
    source = """
void main () {
    auto x = readInt();
    switch (x) {
        default:
            printInt(0);
        case 1:
            printInt(0);
        default:
            printInt(0);           
    }
}
"""
    expected = "Error on line 9 col 8: default"
    assert Parser(source).parse() == expected


def test_110():
    source = """
void main () {}
struct main {};
main () {}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_111():
    source = """
void main () {
   for(; ;a.b);
}
"""
    expected = "Error on line 3 col 13: )"
    assert Parser(source).parse() == expected

def test_112():
    source = """
void main () {
   for(; ;-a++);
}
"""
    expected = "Error on line 3 col 10: -"
    assert Parser(source).parse() == expected

def test_113():
    source = """
void main () {
   a + b = 2;
}
"""
    expected = "Error on line 3 col 9: ="
    assert Parser(source).parse() == expected

def test_114():
    source = """
void main () {
   a = b = c = a * 2;
   a.b.c = a = c.d.e = 1 + 2;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_115():
    source = """
void main () {
   foo().a;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_116():
    source = """
void main () {
   {1, 2}.b;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_117():
    source = """
void main () {
   a = 2 = a;
}
"""
    expected = "Error on line 3 col 9: ="
    assert Parser(source).parse() == expected

def test_118():
    source = """
void main () {
   ++!a;
}
"""
    expected = "Error on line 3 col 5: !"
    assert Parser(source).parse() == expected

def test_119():
    source = """
void main () {
   !a--;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_120():
    source = """
void main () {
   a.b.c++;
   --a.b.c;
   -a.b.c;
   ++a = 1;
}
"""
    expected = "Error on line 6 col 7: ="
    assert Parser(source).parse() == expected

def test_121():
    source = """
void main () {
    ++a.b;
    a.b = 1;
    ++(a.b) = 1;
}
"""
    expected = "Error on line 5 col 12: ="
    assert Parser(source).parse() == expected

def test_122():
    source = """
void main () {
    foo().b = 2;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_123():
    source = """
void main () {
    a = foo().a = (a).b = "string".c.d.e = 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_124():
    source = """
void main () {
    a = a + b = 1;
}
"""
    expected = "Error on line 3 col 14: ="
    assert Parser(source).parse() == expected

def test_125():
    source = """
void main () {
    ++ ! a;
}
"""
    expected = "Error on line 3 col 7: !"
    assert Parser(source).parse() == expected

def test_126():
    source = """
void main () {
    struct {};
}
"""
    expected = "Error on line 3 col 4: struct"
    assert Parser(source).parse() == expected

def test_127():
    source = """
void main () {
    ++a = 1;
}
"""
    expected = "Error on line 3 col 8: ="
    assert Parser(source).parse() == expected

def test_128():
    source = """
void main () {
   for(foo(1).c = 2; ; {1,2}.e = 2) {}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_129():
    source = """
void main () {
   for(foo(1).c = c = 2; ; a + e = 2) {}
}
"""
    expected = "Error on line 3 col 29: +"
    assert Parser(source).parse() == expected

def test_130():
    source = """
void main () {
   for(2 = 2; ; a = 2) {}
}
"""
    expected = "Error on line 3 col 9: ="
    assert Parser(source).parse() == expected

def test_131():
    source = """
void main () {
   a++.c;
}
"""
    expected = "Error on line 3 col 6: ."
    assert Parser(source).parse() == expected

def test_132():
    source = """
void main () {
   ++a.c;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_133():
    source = """
void main () {
   a.c++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_134():
    source = """
void main () {
   a.++a;
}
"""
    expected = "Error on line 3 col 5: ++"
    assert Parser(source).parse() == expected

def test_135():
    source = """
void main () {
   for(++a; ; ){}
}
"""
    expected = "Error on line 3 col 7: ++"
    assert Parser(source).parse() == expected

def test_136():
    source = """
void main () {
   for(a--; ; ){}
}
"""
    expected = "Error on line 3 col 8: --"
    assert Parser(source).parse() == expected

def test_137():
    source = """
void main () {
   for(foo().a; ; ){}
}
"""
    expected = "Error on line 3 col 14: ;"
    assert Parser(source).parse() == expected

def test_138():
    source = """
void main () {
   (1 + 2).a.d.e;
   {2,3,4}.f.g.h;
   2.3.a.b.c;
   "string".e.f.g.h;
   (1).a.b.c.d;
   foo(foo().a, a.b).c.d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_139():
    source = """
void main () {
   1 + {1,2} + -{a++}++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_140():
    source = """
void main () {
   for(int a, int b;;){}
}
"""
    expected = "Error on line 3 col 12: ,"
    assert Parser(source).parse() == expected

def test_141():
    source = """
void main () {
   for(int a;;a++,++b){}
}
"""
    expected = "Error on line 3 col 17: ,"
    assert Parser(source).parse() == expected


def test_142():
    source = """
void main () {
   for(int a;;++(a + b)){}
    for(int a;;{a,b}--){}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_143():
    source = """
void main () {
   for((a) = 2;;){}
}
"""
    expected = "Error on line 3 col 11: ="
    assert Parser(source).parse() == expected

def test_144():
    source = """
void main () {
   for(a;;){}
}
"""
    expected = "Error on line 3 col 8: ;"
    assert Parser(source).parse() == expected

def test_145():
    source = """
void main () {
   {1, 2} = 3;
}
"""
    expected = "Error on line 3 col 10: ="
    assert Parser(source).parse() == expected

def test_146():
    source = """
void main () {
   2.2.a.b.c.d;
   (a) = 2;
}
"""
    expected = "Error on line 4 col 7: ="
    assert Parser(source).parse() == expected

def test_147():
    source = """
void main () {
   for(;;++ -- a ++ -- ) {}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_148():
    source = """
void main () {
   for(int a = 1;) {}
}
"""
    expected = "Error on line 3 col 17: )"
    assert Parser(source).parse() == expected

def test_149():
    source = """
void main () {
   2.0.a.b.c = {}.a.b = foo().c.d = 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_150():
    source = """
int a;
void main () {
}
"""
    expected = "Error on line 2 col 5: ;"
    assert Parser(source).parse() == expected

def test_151():
    source = """
void main () {
    for(1; ;)
}
"""
    expected = "Error on line 3 col 9: ;"
    assert Parser(source).parse() == expected

def test_152():
    source = """
void main () {
    a(2)(3);
}
"""
    expected = "Error on line 3 col 8: ("
    assert Parser(source).parse() == expected

def test_153():
    source = """
void main () {
    ++ -- -a;
}
"""
    expected = "Error on line 3 col 10: -"
    assert Parser(source).parse() == expected

def test_154():
    source = """
void main () {
    auto x = readInt();
    switch (x) {
        case 1:
        case 2:
        default:
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_155():
    source = """
void main () {
    auto x = readInt();
    switch (x) {
        default:
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_156():
    source = """
struct ID {int a = 1;}
void main () {
}
"""
    expected = "Error on line 2 col 17: ="
    assert Parser(source).parse() == expected

def test_157():
    source = """
float main () {
    foo()++--;
    2.3 ++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_158():
    source = """
float main () {
    foo(;; foo(1, 2))
}
"""
    expected = "Error on line 3 col 8: ;"
    assert Parser(source).parse() == expected

def test_158():
    source = """
float main () {
    ID{2, 3};
}
"""
    expected = "Error on line 3 col 6: {"
    assert Parser(source).parse() == expected

def test_159():
    source = """
float main () {
    for(;;i++++--){}
    for(;;++++--{1,2}){}

}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_160():
    source = """
float main () {
    endfunc a;
    func = 1;
    return call;
    number = 2;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_161():
    source = """
float main () {
    (a) = 2;
}
"""
    expected = "Error on line 3 col 8: ="
    assert Parser(source).parse() == expected

def test_162():
    source = """
float main () {
    (a).b = 2;
    (a.b) = 3;
}
"""
    expected = "Error on line 4 col 10: ="
    assert Parser(source).parse() == expected

def test_163():
    source = """
float main () {
   for(i++;;)
}
"""
    expected = "Error on line 3 col 8: ++"
    assert Parser(source).parse() == expected

def test_164():
    source = """
float main () {
   for(++a;;)
}
"""
    expected = "Error on line 3 col 7: ++"
    assert Parser(source).parse() == expected


def test_165():
    source = """
float main () {
   for(1.2;;)
}
"""
    expected = "Error on line 3 col 10: ;"
    assert Parser(source).parse() == expected

def test_166():
    source = """
float main () {
{1, 3}.a.b.c.d = 1.2.a.b.c.d;
   {1, 3} = 2;
}
"""
    expected = "Error on line 4 col 10: ="
    assert Parser(source).parse() == expected

def test_165():
    source = """
float main () {
   for("v";;)
}
"""
    expected = "Error on line 3 col 10: ;"
    assert Parser(source).parse() == expected

def test_166():
    source = """
void main () {
    auto x = readInt();
    switch (a=b.c=a + 2 && 3 > 2 / {1,2}) {
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_167():
    source = """
void main () {
    char a = 1;
    char ++;
    bool --;
    bool = 2;
    true a;
    false a = false;
    do = 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_167():
    source = """
int ID = 1;
"""
    expected = "Error on line 2 col 7: ="
    assert Parser(source).parse() == expected


def test_168():
    source = """
void main () {
    auto x = readInt();
    switch (x) continue;
}
"""
    expected = "Error on line 4 col 15: continue"
    assert Parser(source).parse() == expected

def test_169():
    source = """
void main () {
    do {} while(1);
}
"""
    expected = "Error on line 3 col 7: {"
    assert Parser(source).parse() == expected

def test_170():
    source = """
void main () {
    while(1);
}
"""
    expected = "Error on line 3 col 12: ;"
    assert Parser(source).parse() == expected

def test_171():
    source = """
void main () {
    while(1);
}
"""
    expected = "Error on line 3 col 12: ;"
    assert Parser(source).parse() == expected

def test_172():
    source = """
// empty
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_173():
    source = """
auto foo() {return 1;}
"""
    expected = "Error on line 2 col 0: auto"
    assert Parser(source).parse() == expected

def test_174():
    source = """
auto foo() {return 1;}
"""
    expected = "Error on line 2 col 0: auto"
    assert Parser(source).parse() == expected
