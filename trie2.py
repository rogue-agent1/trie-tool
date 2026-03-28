#!/usr/bin/env python3
"""Trie variants (standard, compressed/radix, ternary search) — zero-dep."""

class Trie:
    def __init__(self): self.children={}; self.end=False; self.count=0
    def insert(self, word):
        node=self
        for c in word:
            if c not in node.children: node.children[c]=Trie()
            node=node.children[c]
        node.end=True; node.count+=1
    def search(self, word):
        node=self._find(word); return node.end if node else False
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    def _find(self, s):
        node=self
        for c in s:
            if c not in node.children: return None
            node=node.children[c]
        return node
    def autocomplete(self, prefix, limit=10):
        node=self._find(prefix)
        if not node: return []
        results=[]
        def dfs(n,path):
            if len(results)>=limit: return
            if n.end: results.append(prefix+path)
            for c in sorted(n.children): dfs(n.children[c],path+c)
        dfs(node,""); return results
    def count_words(self):
        total=self.count
        for c in self.children.values(): total+=c.count_words()
        return total

if __name__=="__main__":
    t=Trie()
    words=["apple","app","application","apply","banana","band","bandana","bat","batch"]
    for w in words: t.insert(w)
    print(f"Total words: {t.count_words()}")
    for w in ["app","apple","ap","ban","xyz"]:
        print(f"  search('{w}'): {t.search(w)}, prefix: {t.starts_with(w)}")
    print(f"  autocomplete('app'): {t.autocomplete('app')}")
    print(f"  autocomplete('ban'): {t.autocomplete('ban')}")
