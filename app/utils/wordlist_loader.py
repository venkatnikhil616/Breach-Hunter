from typing import Set, List, Optional


# Load a wordlist file into a set for fast lookup
def load_wordlist(file_path: str, lowercase: bool = True) -> Set[str]:
    words: Set[str] = set()

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                if lowercase:
                    word = word.lower()
                words.add(word)
    except FileNotFoundError:
        return set()

    return words


# Load multiple wordlists and merge
def load_multiple_wordlists(file_paths: List[str]) -> Set[str]:
    combined: Set[str] = set()
    for path in file_paths:
        combined.update(load_wordlist(path))
    return combined


# Check if password exists in wordlist
def is_common_password(password: str, wordlist: Set[str]) -> bool:
    return password.lower() in wordlist


# Check if password contains dictionary words
def contains_dictionary_word(password: str, wordlist: Set[str]) -> Optional[str]:
    lower_password = password.lower()
    for word in wordlist:
        if len(word) >= 4 and word in lower_password:
            return word
    return None


# Lazy loader (caches wordlist after first load)
class WordlistLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._cache: Optional[Set[str]] = None

    def load(self) -> Set[str]:
        if self._cache is None:
            self._cache = load_wordlist(self.file_path)
        return self._cache

    def reload(self) -> Set[str]:
        self._cache = load_wordlist(self.file_path)
        return self._cache
