from dataclasses import dataclass, field

from .token import Token


# STEP 1: one record per identifier.
# Fields: index, name, type, scope, occurrences
@dataclass
class SymbolEntry:
    index: int #the index of the identifier in the symbol table. it reads from left to right so first appearance of an identifier will be 0 and so on. if an identifier repeats it will not increment the index
    name: str #the name of the identifier
    type: str | None = None # type of identifier it is a string like int , char , float , etc OR none if it is not yet known
    scope: str | None = None # scope of identifier it is a string like global , local , etc OR none if it is not yet known 
    occurrences: list[tuple[int, int]] = field(default_factory=list) # list of (line, column) pairs where the identifier occurs 

    #occurrences: list[Token] = field(default_factory=list) # stores the whole token every time the identifier appears not just the new position.

    def add_occurrence(self, token: Token):
        self.occurrences.append((token.line, token.column))


class SymbolTable:
    """Hash table of identifiers using separate chaining for collisions."""

    def __init__(self, size: int = 101):
        self.size = size
        self.buckets : list[list[SymbolEntry]] = [[] for _ in range(size)] # the outer list is the buckets, and each inner list holds entries.
        self.count = 0

    def _hash(self, name: str) -> int: # hashing function
        h = 0
        for ch in name:
            h = (h * 31 + ord(ch)) % self.size # ord is a built-in Python function. It gives a character’s number code. The name comes from “ordinal”, meaning “position number”.
        return h

    def insert(self, token: Token, type: str | None = None, scope: str | None = None) -> SymbolEntry:
        h = self._hash(token.lexeme)
        bucket = self.buckets[h]
        for entry in bucket:
            if entry.name == token.lexeme:
                entry.add_occurrence(token)
                return entry
        entry = SymbolEntry(self.count, token.lexeme, type, scope)
        entry.add_occurrence(token)
        bucket.append(entry)
        self.count += 1
        return entry
        
    def lookup(self, name: str) -> SymbolEntry | None:
        bucket = self.buckets[self._hash(name)]
        for entry in bucket:
            if entry.name == name:
                return entry
        return None
    
    def entries(self) -> list[SymbolEntry]:
        all_entries = []
        for bucket in self.buckets:
            for entry in bucket:
                all_entries.append(entry)
        return sorted(all_entries, key=lambda entry: entry.index)

    def __len__(self) -> int:
        return self.count
