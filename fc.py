"""Attempt to solve a free cell deck"""

from enum import Enum

RAW_DECK = [["6s", "qd", "qc", "5c", "7h", "6h", "8d", "3d"],
            ["9s", "ks", "4c", "4s", "6d", "kd", "7c", "8h"],
            ["kc", "5s", "8c", "jd", "4h", "8s", "jc", "jh"],
            ["3s", "9d", "6c", "ad", "2d", "5h", "2s", "3h"],
            ["js", "ah", "9c", "kh", "5d", "10c", "7d", "qh"],
            ["3c", "4d", "10s", "10h", "as", "10d", "9h", "2h"],
            ["2c", "ac", "7s", "qs", None, None, None, None]]

EMPTY = [None for x in range(4)]
BUILD = [None for x in range(4)]
DECK = [[None for x in range(8)] for y in range(100)]


def print_card(pcard):
    """Return printable format for individual card"""
    prt = ""
    if pcard is None:
        prt += "    ,"
    else:
        prt += " " + pcard.print() + ","
    return prt

def print_line(line):
    line_print = ""
    idx = 0
    for card in line:
        if card is None:
            idx += 1
        line_print += print_card(card)
    if idx == 8:
        return ""
    return line_print[:-1]

def print_deck():
    for line in DECK:
        line_ptr = print_line(line)
        if line_ptr != "":
            print (print_line(line))

def print_all():
    print("--------------------------------------")
    empty_print = print_line(EMPTY)
    BUILD_print = print_line(BUILD)
    print (EMPTY_print + "|" + BUILD_print)
    print('\n')
    print_deck()

def init_deck():
    r = 0
    for row in RAW_DECK:
        c = 0
        for card in row:
            if card != None:
                DECK[r][c] = Card(card)
            c+=1
        r+=1
    
def check_deck():
    for kind in ["SPADE", "CLUB", "DIAMOND", "HEART"]:
        for val in range(1,14):
            #print("Looking for " + str(val) + " " + kind)
            r = 0
            found = False
            for row in DECK:
                c = 0
                for card in row:
                    if card is not None and card.value == val and card.kind == kind:
                        #print("Found at [" + str(r) + ", " + str(c) + "]")
                        found = True
                    c += 1
                r += 1
            if not found and card is not None:
                print("Did not find " + card.print())
                    
        
   

class Card():
    ## Expects format like '5h', '10s', 'jd' or 'ac'
    def __init__(self, card = None):
        ## print("In constructor, card = " + card)
        if card == None:
            return
        self._raw = card
        self._set_value(card)
        self._set_kind(card)
        self.print()
    def _set_value(self, s):
        if len(s) == 3:
            self.value = int(s[:2])
        else:
            v = s[:1]
            if v.isdigit():
                self.value = int(v)
            else:
                if v == 'a':
                    self.value = 1
                elif v == 'j':
                    self.value = 11
                elif v == 'q':
                    self.value = 12
                elif v == 'k':
                    self.value = 13
                else:
                    print ("ERROR! - Unkown Value:'" + v + "'")
                
    def _set_kind(self, s):
        k = s[-1]
        if k == 'c':
            self.kind = "CLUB"
            self.color = "BLACK"
        elif k == 'd':
            self.kind = "DIAMOND"
            self.color = "RED"
        elif k == 'h':
            self.kind = "HEART"
            self.color = "RED"
        elif k == 's':
            self.kind = "SPADE"
            self.color = "BLACK"
        else:
            print ("ERROR! - Unkown Kind:'" + k + "'")
            
    def print_long(self):
        return str("In:[" + self._raw + "] " + str(self.value) + ", " + self.kind + ", " + self.color)
    def print(self):
        s = ""
        if len(self._raw) == 2:
            s+= " "
        s += str(self._raw) 
        return s

# check_valid_move(Card("3h"), Card("3s"))
# check_valid_move(Card("3h"), Card("2s"))
# check_valid_move(Card("3h"), Card("2d"))        
def check_valid_move(c1, c2):
    valid = False
    p = c2.print() + " can"
    if c2.color != c1.color and c2.value == (c1.value - 1):
        valid = True
    else:
        p += "'t"
    p += " go on top of " + c1.print()
    print(p)
    return valid

def get_bottom_card(col):
    for idx in range(len(DECK)):
        #print (deck[idx][col].print())
        if (DECK[idx+1][col] == None):
            return DECK[idx][col]

def can_move_to_BUILD(card):
    for c in BUILD: # Check if first of that kind
        has_kind = False
        if c is not None and c.kind == card.kind:
            has_kind = True
            if c.value == (card.value - 1):
                return True
        if has_kind == False and card.value == 1:
            return True # First of its kind up
        return False
            
def move_to_BUILD(card):
    if can_move_to_BUILD(card) == False:
        print ("Error! Cannot move " + card.print() + " to BUILD!")
        return
    idx = 0
    found = False
    for c in BUILD: # Check if first of that kind
        if c is not None and c.kind == card.kind:
            found = True
            BUILD[idx] = card # Replace card
        idx += 1
    if found == False: # There must be some None in there
        idx = 0
        for c in BUILD: # Check if first of that kind
            if c is None and found == False:
                BUILD[idx] = card # Replace card
                found = True
            idx += 1
    if found == False:
        print ("Error! Was unable to move up " + card.print() + " in " + print_line(BUILD))
    else:
        remove_card_from_deck(card)
            
def remove_card_from_deck(card):
    r_idx = 0
    for row in DECK:
        c_idx = 0
        for c in row:
            if (c is not None and c.value == card.value
                  and c.kind == card.kind):
                DECK[r_idx][c_idx] = None
                return
            c_idx += 1
        r_idx += 1

init_deck()
check_deck()
print_all()

moved = True

while moved == True:
    moved = False
    for col in range(8):
        card = get_bottom_card(col)
        if can_move_to_build(card):
            move_to_build(card)
            moved = True

print_all()
