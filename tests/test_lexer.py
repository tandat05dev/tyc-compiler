"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer

def test_001():
    source = """\t\r\n
    /* This is a block comment so // has no meaning here */
    // VOTIEN
"""
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002():
    source = "@"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token @"

def test_003():
    source = "auto auto1"
    expected = "auto,auto1,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    source = "+ ++"
    expected = "+,++,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    source = "votien123"
    expected = "votien123,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    source = "0   100   255   2500   -45"
    expected = "0,100,255,2500,-,45,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    source = "0.0   3.14   -2.5   1.23e4   5.67E-2   1.   .5"
    expected = "0.0,3.14,-,2.5,1.23e4,5.67E-2,1.,.5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    source = """
    "This is a string containing tab \\t"
    "He asked me: \\"Where is John?\\""
"""
    expected = "This is a string containing tab \\t,He asked me: \\\"Where is John?\\\",<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    source = """
    "This is a string \n containing tab \\t"
"""
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: This is a string "
    
def test_010():
    source = """
    "This is a string \\z containing tab \\t"
"""
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: This is a string \\z"


def test_011():
    source = """
    auto break case continue default else float for if int
    return string struct switch void while
    """
    expected = (
        "auto,break,case,continue,default,else,float,for,if,int,"
        "return,string,struct,switch,void,while,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    source = """
    + - * / % == != < > <= >= || && ! ++ -- = .
    """
    expected = (
        "+,-,*,/,%,==,!=,<,>,<=,>=,||,&&,!,++,--,=,.,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    source = """
    { } ( ) ; , :
    """
    expected = "{,},(,),;,,,:,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    source = """
    a A _ _a a1 a_1 A123 _ABC abc_DEF123
    """
    expected = (
        "a,A,_,_a,a1,a_1,A123,_ABC,abc_DEF123,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    source = """
   ++ +- -+ + + - - +++
    """
    expected = (
        "++,+,-,-,+,+,+,-,-,++,+,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    source = "^"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token ^"

def test_017():
    source = "&"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token &"

def test_018():
    source = "\\"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token \\"

def test_019():
    source = "autoauto"
    expected = (
        "autoauto,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    source = "12ab34 a-b"
    expected = (
        "12,ab34,a,-,b,<EOF>"
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    source = "~"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token ~"

def test_022():
    source = "0 5 123 -0 -45 99999"
    expected = "0,5,123,-,0,-,45,99999,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    source = "000 -000 0123 -00502"
    expected = "000,-,000,0123,-,00502,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    source = "+000 +123 +-025"
    expected = "+,000,+,123,+,-,025,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    source = "12_3"
    expected = "12,_3,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    source = "0x123"
    expected = "0,x123,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """skip"""
    source = "\t \n \r \n \t   "
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """skip"""
    source = "\f  "
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """skip"""
    source = "\t \n \r \n \t   "
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    source = "//include <iostream>"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    source = "// this is a comment\nint x"
    expected = "int,x,<EOF>" 
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    source = "/* multi line \n comment */ float y"
    expected = "float,y,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    source = "int a // comment here\nfloat b"
    expected = "int,a,float,b,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    source = "/* outer /* inner */ still comment */ boolean c"
    expected = "still,comment,*,/,boolean,c,<EOF>" 
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    source = "   \t\r\n\f // just comment\n   /* another */   "
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    source = "// Python comment\nint x"
    expected = "int,x,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    source = "// C++ style comment\nfloat y"
    expected = "float,y,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    source = "/* multi-line comment */ boolean z"
    expected = "boolean,z,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    source = "// Rust or Go comment\nstring s"
    expected = "string,s,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    source = "<!-- HTML style comment --> int a"
    expected = "<,!,--,HTML,style,comment,--,>,int,a,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    source = "## python"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token #"


def test_042():
    source = "# python"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token #"

def test_043():
    source = "int &a := 10;"
    assert Tokenizer(source).get_tokens_as_string() == "int,Error Token &"

def test_044():
    source = ">> **"
    expected = ">,>,*,*,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    source = '"Hello\\nWorld! \\"test\\" \\\\"'
    expected = 'Hello\\nWorld! \\"test\\" \\\\,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    """Test Unclosed string with newline"""
    source = '"Unclosed string line\nlet x = 5;'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Unclosed string line"


def test_047():
    source = '"Missing end quote'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Missing end quote"


def test_048():
    source = '"Escape with \\x invalid"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: Escape with \\x"


def test_049():
    source = '"abc\\\\ \\ "'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: abc\\\\ \\ "

def test_050():
    source = (
        '"abc" '
        '"\\n" '
        '"\\t" '
        '"\\r" '
        '"\\\"" '
        '"\\\\" '
        '"" '
        '"Hello\\nWorld\\tTabbed\\rCarriage\\"Quote\\\\"'
    )
    expected = (
        'abc,\\n,\\t,\\r,\\",\\\\,,'
        'Hello\\nWorld\\tTabbed\\rCarriage\\"Quote\\\\,<EOF>'
    )
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    source = '"This is a string\r\nlet x = 1;'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: This is a string"


def test_052():
    source = '"Another line\nlet x = 2;'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Another line"


def test_053():
    source = '"End with <EOF>'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: End with <EOF>"

def test_054():
    source = '"Escape with \\f valid"'
    expected = 'Escape with \\f valid,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    source = '"Escape with \\b valid"'
    expected = 'Escape with \\b valid,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

# def test_056():
#     source = '"Escape with \'" invalid"'
#     assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: "


def test_057():
    source = '"Escape with \\z"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: Escape with \\z"


def test_058():
    source = '"Escape with \\*"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: Escape with \\*"

def test_059():
    source = "let x := 0; /* outer /* inner */ still outer */ x := 1;"
    expected = "let,x,:,=,0,;,still,outer,*,/,x,:,=,1,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Valid simple string"""
    source = '"Hello World"'
    expected = "Hello World,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    """Valid string with escape sequences"""
    source = '"Line1\\nLine2\\tTabbed\\rCarriage\\\\"'
    expected = "Line1\\nLine2\\tTabbed\\rCarriage\\\\,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    source = '"He said: \\"Hello\\" "'
    expected = 'He said: \\"Hello\\" ,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    source = '""'
    expected = ",<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    source = '"Unclosed string\nlet x = 1;'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Unclosed string"


def test_065():
    source = '"Another unclosed string'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: Another unclosed string"


def test_066():
    source = '"Escape with \\x invalid"'
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: Escape with \\x"

def test_067():
    source = '"This is invalid: \'"'
    expected = 'This is invalid: \',<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    source = '"Ends with backslash\\\\"'
    expected = 'Ends with backslash\\\\,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    source = '"\\b\\f\\r\\n\\t\\\""'
    expected = '\\b\\f\\r\\n\\t\\",<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    source = '"Hello\\nWorld! \\"Quote\\" and \\\\Backslash"'
    expected = 'Hello\\nWorld! \\"Quote\\" and \\\\Backslash,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_071():
    source = '0. 0.9 0e2 0.e-2 '
    expected = '0.,0.9,0e2,0.e-2,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    source = '123.45E-6'
    expected = '123.45E-6,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    source = '123.456'
    expected = '123.456,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    source = '123e10'
    expected = '123e10,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    source = '0.33E+3'
    expected = '0.33E+3,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    source = "1. 0.5 123.456 42e3 7E+2 9e-10 3.14e10 6.022E23 0.1E-3 10.0e+5"
    expected = "1.,0.5,123.456,42e3,7E+2,9e-10,3.14e10,6.022E23,0.1E-3,10.0e+5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """Test invalid float: missing integer part before dot"""
    source = '.5 -.055'
    expected = '.5,-,.055,<EOF>' 
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Test invalid float: incomplete exponent part"""
    source = '1e'
    expected = '1,e,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    source = 'e10'
    expected = 'e10,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    source = '4.5.6 12a.3'
    expected = '4.5,.6,12,a,.3,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_081():
    source = '001e+02 -1. -2.0e-02'
    expected = '001e+02,-,1.,-,2.0e-02,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    source = '.e-2'
    expected = '.,e,-,2,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    source = '0.0 3.14 1.23e4 5.67E-2 1. .5 1e4 2E-3'
    expected = '0.0,3.14,1.23e4,5.67E-2,1.,.5,1e4,2E-3,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    source = '.010e-0.5'
    expected = '.010e-0,.5,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    source = '-12e-5'
    expected = '-,12e-5,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    source = "["
    assert Tokenizer(source).get_tokens_as_string() == "Error Token ["

def test_087():
    source = "]"
    assert Tokenizer(source).get_tokens_as_string() == "Error Token ]"

def test_088():
    source = '"Extended ASCII: \x80\xFF" '
    expected = 'Extended ASCII: \x80\xFF,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    source = '-12.1e-2'
    expected = '-,12.1e-2,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    source = '"a\r\n"'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: a"

def test_091():
    source = '"a\\r\\n"'
    expected = 'a\\r\\n,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    source = """ "a\\\n """
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: a\\"


def test_093():
    source = '"a'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: a"


def test_094():
    source = '"a'
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: a"

def test_095():
    source = " \"ab\\'ab \"   "
    assert Tokenizer(source).get_tokens_as_string() == "Illegal Escape In String: ab\\'"

def test_096():
    source = '123.e'
    expected = '123.,e,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    source = '-.a'
    expected = '-,.,a,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_098():
    source = '-10 -1.0'
    expected = '-,10,-,1.0,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    source = '"abc\n\n"'
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False, "Expected ErrorToken but no exception was raised"
    except Exception as e:
        assert str(e) == "Unclosed String: abc"


def test_099():
    source = '-.'
    expected = '-,.,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    source = '@ab'
    assert Tokenizer(source).get_tokens_as_string() == "Error Token @"

def test_101():
    source = '.e12'
    expected = '.,e12,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_102():
    source = '.e12'
    expected = '.,e12,<EOF>'  
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_103():
    source = """ "a\\\n"""
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: a\\"

def test_104():
    source = """ "'a\\"""
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: 'a\\"


def test_105():
    source = """\""""
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: "


def test_106():
    source = """\"\n"""
    assert Tokenizer(source).get_tokens_as_string() == "Unclosed String: "