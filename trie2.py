#!/usr/bin/env python3
"""Compressed Trie (Radix Tree / Patricia Tree)."""

class RadixNode:
    def __init__(self): self.children = {}; self.value = None; self.is_end = False

class RadixTree:
    def __init__(self): self.root = RadixNode()
    def insert(self, key, value=None):
        node = self.root; i = 0
        while i < len(key):
            found = False
            for edge, child in list(node.children.items()):
                common = 0
                while common < len(edge) and i + common < len(key) and edge[common] == key[i + common]: common += 1
                if common == 0: continue
                if common == len(edge): node = child; i += common; found = True; break
                mid = RadixNode(); mid.children[edge[common:]] = child
                node.children[key[i:i+common]] = mid; del node.children[edge]
                if i + common == len(key): mid.is_end = True; mid.value = value
                else:
                    new = RadixNode(); new.is_end = True; new.value = value
                    mid.children[key[i+common:]] = new
                return
            if not found:
                new = RadixNode(); new.is_end = True; new.value = value
                node.children[key[i:]] = new; return
        node.is_end = True; node.value = value
    def search(self, key):
        node = self.root; i = 0
        while i < len(key):
            found = False
            for edge, child in node.children.items():
                if key[i:].startswith(edge): node = child; i += len(edge); found = True; break
            if not found: return None
        return node.value if node.is_end else None
    def prefix_search(self, prefix):
        node = self.root; i = 0; results = []
        while i < len(prefix):
            found = False
            for edge, child in node.children.items():
                if prefix[i:].startswith(edge): node = child; i += len(edge); found = True; break
                if edge.startswith(prefix[i:]): node = child; i = len(prefix); found = True; break
            if not found: return results
        self._collect(node, prefix, results); return results
    def _collect(self, node, prefix, results):
        if node.is_end: results.append((prefix, node.value))
        for edge, child in node.children.items(): self._collect(child, prefix + edge, results)

if __name__ == "__main__":
    rt = RadixTree()
    for w in ["test", "testing", "tested", "team", "toast"]: rt.insert(w, w.upper())
    print(f"search 'test': {rt.search('test')}")
    print(f"prefix 'te': {rt.prefix_search('te')}")
