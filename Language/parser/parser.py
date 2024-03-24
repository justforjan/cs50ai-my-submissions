import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """

S -> SP | SP Conj SP
SP -> NP VP | VP

PP -> P NP

AdjP -> Adj NP | Adj Adj NP | Adj Adj Adj NP

DetP -> Det AdjP | Det NP

NP -> N | N PP | AdjP | DetP



AdvP -> Adv | Adv VP | VP Adv

VP -> V | V NP | V PP | V NP PP | AdvP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    tokenized = nltk.tokenize.word_tokenize(sentence.lower())

    for token in tokenized.copy():
        
        alphabetic = any([c.isalpha() for c in token])

        if not alphabetic:
            tokenized.remove(token)

    return tokenized



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    nps = []

    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            if not any([subsubtree.label() == 'NP' for subsubtree in subtree.subtrees() if subtree is not subsubtree]):
                nps.append(subtree)

    return nps


if __name__ == "__main__":
    main()
