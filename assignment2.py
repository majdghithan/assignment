
symbol_table = {"if":"IF_TOKEN","while":"WHILE_TOKEN","for":"FOR_TOKEN"}
keywords = ["if","for","while"]

class Token():
    def __init__(self,type_,value):
        self.type = type_
        self.value = value
    def __str__(self):
        return f"Token : {self.type}\nLexeme: {self.value} \n"

class Lexer():
    def __init__(self,code):
        self.code = code
        self.index = 0
        self.c = code[self.index]
        self.tokens = []

    def advance(self):
        self.index += 1
        self.c = self.code[self.index]

    def lex_id(self):
        id = ""
        while str.isalnum(self.c) or self.c == '_':
            id = f"{id}{self.c}"
            self.advance()
        if id in keywords:
            return Token(f"{id.upper()}_TOKEN",id)
        return Token("ID",id)

    def lex_error(self):
        er = ""
        while self.c not in ['\t',' ','\n','\0']:
            er += self.c
            self.advance()
        return Token("ERROR",er)

    def lex_numerical(self,is_negative = False):
        val = "-" if is_negative else ""
        dots = 0
        is_float = False
        is_error = False

        while self.c not in ['\t',' ','\n','\0']: #str.isdigit(self.c) or self.c == '.':
            if self.c == '.':
                if dots !=0:
                    is_error = True
                if len(val) - int(is_negative) < 1:
                    is_error = True
                dots += 1
                is_float = True
            elif not str.isdigit(self.c):
                is_error = True

            val = f"{val}{self.c}"
            self.advance()

        if is_float and not is_error:
            return Token("FLOAT",float(val))
        if is_error:
            return Token("ERROR",val)
        else:
            return Token("INTEGER",int(val))

    def lex_lessthan(self):
        if self.c == '=':
            self.advance()
            return Token("RELOP","<=")
        return Token("RELOP","<")

    def lex_greaterthan(self):
        if self.c == '=':
            self.advance()
            return Token("RELOP",">=")
        return Token("RELOP",">")

    def lex_equals(self):
        if self.c == '=':
            self.advance()
            return Token("RELOP","==")
        return Token("ERROR","Unexpected token '='")

    def lex(self):
        while (self.index+1) != len(self.code) :#and self.c != '\0':

            # if the current charecter is in the alphabet
            if str.isalpha(self.c):
                # check if ID is a keyword
                tkn = self.lex_id()
                self.tokens.append(tkn)
                if tkn.value not in keywords:
                    symbol_table[tkn.value] = "ID"

            # if the current charecter is digit, lex a numerical value
            elif str.isdigit(self.c):
                tkn = self.lex_numerical()
                self.tokens.append(tkn)

            # if the current charecter is a - then we have a negative number
            elif self.c == '-':
                self.advance()
                tkn = self.lex_numerical(is_negative=True)
                self.tokens.append(tkn)

            elif self.c == '<':
                self.advance()
                tkn = self.lex_lessthan()
                self.tokens.append(tkn)

            elif self.c == '>':
                self.advance()
                tkn = self.lex_greaterthan()
                self.tokens.append(tkn)

            elif self.c == '=':
                self.advance()
                tkn = self.lex_equals()
                self.tokens.append(tkn)

            #skip whitespace
            elif self.c in ['\t',' ','\n']:
                self.advance()

            else:
                self.tokens.append(self.lex_error())


def read_file(filename):
    file = open(filename,'r')
    txt = file.read()
    file.close()
    return txt

def show_symbol_table(symbol_table):
    print("\n.......... SYMBOL TABLE ............")
    for i in symbol_table.items():
        print(i[0]," "*(30-len(i[0]) - len(i[1])),i[1])
    print()

def print_menu():
    print("................................")
    print("Choose:\n1- Call Lex()\n2- Show the Symbol Table\n3- Exit")
    print("................................")

if __name__ == "__main__":
    code = read_file(input("filename :: "))
    lexer = Lexer(code)
    while True:
        print_menu()
        c = int(input("Choice :: "))
        if c == 1:
            lexer.lex()
            for tkn in lexer.tokens:
                print(tkn)
        elif c==2:
            show_symbol_table(symbol_table)
        elif c==3:
            exit()
        else:
            print("That was a wrong choice")


