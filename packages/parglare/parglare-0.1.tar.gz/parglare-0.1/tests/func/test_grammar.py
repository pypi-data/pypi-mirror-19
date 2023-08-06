import pytest
from parglare.grammar import Grammar, Terminal, NonTerminal, ASSOC_LEFT, \
    ASSOC_RIGHT, DEFAULT_PRIORITY
from parglare.exceptions import GrammarError


def test_undefined_grammar_symbol():
    "Tests that undefined grammar symbols raises errors."
    grammar = """
    S = A B;
    A = "a" | B;
    B = id;
    """
    with pytest.raises(GrammarError) as e:
        Grammar.from_string(grammar)

    assert 'Undefined grammar symbol' in str(e)
    assert 'B = id' in str(e)


def test_terminal_nonterminal():

    # Production A is a terminal ("a") and non-terminal at the same time.
    # Thus, it must be recognized as non-terminal.
    grammar = """
    S = A B;
    A = "a" | B;
    B = "b";
    """
    g = Grammar.from_string(grammar)
    assert NonTerminal("A") in g.nonterminals
    assert Terminal("A") not in g.terminals
    assert Terminal("B") in g.terminals
    assert NonTerminal("B") not in g.nonterminals

    # Here A shoud be non-terminal while B will be terminal.
    grammar = """
    S = A B;
    A = B;
    B = "b";
    """

    g = Grammar.from_string(grammar)
    assert NonTerminal("A") in g.nonterminals
    assert Terminal("A") not in g.terminals
    assert Terminal("B") in g.terminals
    assert NonTerminal("B") not in g.nonterminals


def test_multiple_terminal_definition():

    # A is defined multiple times as terminal thus it must be recognized
    # as non-terminal with alternative expansions.
    grammar = """
    S = A A;
    A = "a";
    A = "b";
    """

    g = Grammar.from_string(grammar)

    assert NonTerminal("A") in g.nonterminals
    assert Terminal("A") not in g.terminals


def test_assoc_prior():
    """Test that associativity and priority can be defined for productions and
    terminals.
    """

    grammar = """
    E = E '+' E {left, 1};
    E = E '*' E {2, left};
    E = E '^' E {right};
    E = id;
    id = /\d+/;
    """

    g = Grammar.from_string(grammar)

    assert g.productions[1].prior == 1
    assert g.productions[1].assoc == ASSOC_LEFT
    assert g.productions[3].assoc == ASSOC_RIGHT
    assert g.productions[3].prior == DEFAULT_PRIORITY

    assert g.productions[3].prior == DEFAULT_PRIORITY


def test_terminal_priority():
    "Terminals might define priority which is used for lexical disambiguation."

    grammar = """
    S = A | B;
    A = 'a' {15};
    B = 'b';
    """

    g = Grammar.from_string(grammar)

    for t in g.terminals:
        if t.name == 'A':
            assert t.prior == 15
        else:
            assert t.prior == DEFAULT_PRIORITY


def test_no_terminal_associavitity():
    "Tests that terminals can't have associativity defined."
    grammar = """
    S = A | B;
    A = 'a' {15, left};
    B = 'b';
    """

    with pytest.raises(GrammarError) as e:
        Grammar.from_string(grammar)

    assert 'associativity' in str(e)
