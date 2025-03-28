use std::collections::HashMap;

#[derive(Debug)]
struct Trie {
    node: HashMap<char, Trie>,
}

impl Trie {
    fn new() -> Self {
        Self {
            node: HashMap::new(),
        }
    }
    fn add_word(&mut self, word: &str) {
        if let Some(char) = word.chars().next() {
            match self.node.get_mut(&char) {
                // Continue down next level since this
                // level is finite from a-z
                Some(trie) => {
                    // Continue with substring minus head
                    // in case next characters expands lookup
                    trie.add_word(&word[1..])
                }
                None => {
                    // New character entry expands lookup
                    let mut trie = Trie::new();
                    trie.add_word(&word[1..]);
                    self.node.insert(char, trie);
                }
            }
        }
    }
}

#[test]
fn trie() {
    let mut t = Trie::new();
    t.add_word("hello");
    t.add_word("help");
    t.add_word("hela");
    dbg!(t);
}
