import argparse, json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
            node.count += 1
        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children: return False
            node = node.children[c]
        return node.is_end

    def autocomplete(self, prefix, limit=10):
        node = self.root
        for c in prefix:
            if c not in node.children: return []
            node = node.children[c]
        results = []
        def dfs(n, path):
            if len(results) >= limit: return
            if n.is_end: results.append(prefix + path)
            for c in sorted(n.children):
                dfs(n.children[c], path + c)
        dfs(node, "")
        return results

    def count_prefix(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children: return 0
            node = node.children[c]
        return node.count

def main():
    p = argparse.ArgumentParser(description="Trie with autocomplete")
    p.add_argument("--words", nargs="+")
    p.add_argument("--search")
    p.add_argument("--complete")
    p.add_argument("--count")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    t = Trie()
    if args.demo:
        words = ["apple","app","application","apply","apt","ape","banana","band","ban"]
        for w in words: t.insert(w)
        print(f"Complete 'app': {t.autocomplete('app')}")
        print(f"Complete 'ban': {t.autocomplete('ban')}")
        print(f"Search 'apple': {t.search('apple')}")
        print(f"Search 'appl': {t.search('appl')}")
        print(f"Count 'app': {t.count_prefix('app')}")
    elif args.words:
        for w in args.words: t.insert(w)
        if args.search: print(t.search(args.search))
        if args.complete: print(t.autocomplete(args.complete))
        if args.count: print(t.count_prefix(args.count))
    else: p.print_help()

if __name__ == "__main__":
    main()
