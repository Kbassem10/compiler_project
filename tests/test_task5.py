import sys
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.symbol_table import SymbolTable
from src.token import Token
from src.token_type import TokenType


def ident(name, line=1, column=1):
    return Token(TokenType.IDENTIFIER, name, line, column)


def test_insert_and_lookup():
    table = SymbolTable()
    entry = table.insert(ident("count", 3, 13), type="int", scope="main")
    assert entry.index == 0
    assert table.lookup("count") is entry
    assert entry.type == "int"
    assert entry.scope == "main"
    assert entry.occurrences == [(3, 13)]
    assert table.lookup("missing") is None


def test_repeated_name_adds_occurrence():
    table = SymbolTable()
    first = table.insert(ident("i", 2, 5))
    again = table.insert(ident("i", 4, 9))
    assert first is again
    assert len(table) == 1
    assert first.occurrences == [(2, 5), (4, 9)]


def test_collisions_are_chained():
    # size=1 forces every name into the same bucket
    table = SymbolTable(size=1)
    for name in ("a", "b", "c"):
        table.insert(ident(name))
    assert len(table.buckets[0]) == 3
    assert [table.lookup(n).name for n in ("a", "b", "c")] == ["a", "b", "c"]


def test_entries_in_first_seen_order():
    table = SymbolTable()
    for name in ("zeta", "alpha", "zeta", "mid"):
        table.insert(ident(name))
    assert [e.name for e in table.entries()] == ["zeta", "alpha", "mid"]
    assert [e.index for e in table.entries()] == [0, 1, 2]


def test_hash_is_case_sensitive():
    table = SymbolTable()
    table.insert(ident("Count"))
    table.insert(ident("count"))
    assert len(table) == 2


def run_all():
    test_insert_and_lookup()
    print("✅ PASS: test_insert_and_lookup")
    test_repeated_name_adds_occurrence()
    print("✅ PASS: test_repeated_name_adds_occurrence")
    test_collisions_are_chained()
    print("✅ PASS: test_collisions_are_chained")
    test_entries_in_first_seen_order()
    print("✅ PASS: test_entries_in_first_seen_order")
    test_hash_is_case_sensitive()
    print("✅ PASS: test_hash_is_case_sensitive")
    print("All Task 5 tests passed successfully!")


if __name__ == "__main__":
    run_all()
