#!/usr/bin/env python3
"""Trie - Prefix tree with autocomplete, count, and fuzzy matching."""
import sys

class TrieNode:
    def __init__(self):
        self.children = {}; self.end = False; self.count = 0; self.word = None

class Trie:
    def __init__(self): self.root = TrieNode(); self.size = 0
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]; node.count += 1
        node.end = True; node.word = word; self.size += 1
    def search(self, word):
        node = self._find(word)
        return node.end if node else False
    def starts_with(self, prefix):
        node = self._find(prefix)
        return node is not None
    def _find(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children: return None
            node = node.children[c]
        return node
    def autocomplete(self, prefix, limit=10):
        node = self._find(prefix)
        if not node: return []
        results = []; self._collect(node, results, limit)
        return results
    def _collect(self, node, results, limit):
        if len(results) >= limit: return
        if node.end: results.append(node.word)
        for c in sorted(node.children):
            self._collect(node.children[c], results, limit)
    def fuzzy(self, word, max_dist=1):
        results = []
        def dfs(node, i, dist, path):
            if dist > max_dist: return
            if i == len(word):
                if node.end: results.append(("".join(path), dist))
                for c, child in node.children.items():
                    dfs(child, i, dist + 1, path + [c])
                return
            for c, child in node.children.items():
                d = 0 if c == word[i] else 1
                dfs(child, i + 1, dist + d, path + [c])
                dfs(child, i, dist + 1, path + [c])
            dfs(node, i + 1, dist + 1, path)
        dfs(self.root, 0, 0, [])
        return sorted(set(results), key=lambda x: x[1])
    def count_prefix(self, prefix):
        node = self._find(prefix)
        return node.count if node else 0

def main():
    t = Trie()
    words = ["apple", "app", "application", "apply", "apt", "banana", "band", "bar", "bat"]
    for w in words: t.insert(w)
    print(f"=== Trie ({t.size} words) ===\n")
    print(f"Search 'app': {t.search('app')}")
    print(f"Search 'ap': {t.search('ap')}")
    print(f"Prefix 'app': {t.autocomplete('app')}")
    print(f"Count 'ap*': {t.count_prefix('ap')}")
    print(f"Fuzzy 'aple' (dist≤1): {t.fuzzy('aple', 1)}")

if __name__ == "__main__":
    main()
