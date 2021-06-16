from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And( #Considering A is either a knave or a knight 
 Or(And(Not(AKnight),AKnave), And(AKnight,Not(AKnave))), 
 # A is a knight --> A is both knight and knave
 Biconditional(AKnight, And(AKnight,AKnave))
    # TODO
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A, B either knight or knave
    Or(And(Not(AKnight),AKnave), And(AKnight,Not(AKnave))),
    Or(And(Not(BKnight),BKnave), And(BKnight,Not(BKnave))),
    # A is a knight --> A, B both are knaves
    Biconditional(AKnight, And(AKnave,BKnave))
    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #A,B either knight or knave
    Or(And(Not(AKnight),AKnave), And(AKnight,Not(AKnave))),
    Or(And(Not(BKnight),BKnave), And(BKnight,Not(BKnave))),
    
    Biconditional(AKnight,Or(And(AKnight,BKnight), And(AKnave,BKnave))),
    Biconditional(BKnight,Or(And(AKnight,BKnave), And(AKnave,BKnight)))

    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(And(Not(AKnight),AKnave), And(AKnight,Not(AKnave))),
    Or(And(Not(BKnight),BKnave), And(BKnight,Not(BKnave))),
    Or(And(Not(CKnight),CKnave), And(CKnight,Not(CKnave))),

    Implication(Or(AKnave,AKnight), Or(AKnight,AKnave)),
    Biconditional(BKnight,Biconditional(AKnight,AKnave)),
    Biconditional(BKnight,CKnave),
    Biconditional(CKnight,AKnight)
    

    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
