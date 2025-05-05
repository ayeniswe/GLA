use crate::ahocorasick::array_impl;
use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};

/// The `TrieType` enum is used to switch between different `Trie` implementations based on memory constraints.
enum TrieType {
    ArrayTrie(array_impl::Trie),
}
impl TrieType {
    fn add_word(&mut self, word: &str) {
        match self {
            TrieType::ArrayTrie(trie) => trie.add_word(word),
        }
    }
    fn set_suffix_links(&mut self) {
        match self {
            TrieType::ArrayTrie(trie) => trie.set_suffix_links(),
        }
    }
    fn search(&self, text: &str) -> HashSet<String> {
        match self {
            TrieType::ArrayTrie(trie) => trie.search(text),
        }
    }
    fn search_occurences(&self, text: &str) -> HashMap<String, usize> {
        match self {
            TrieType::ArrayTrie(trie) => trie.search_occurences(text),
        }
    }
}

/// The `StrMatch` represents a substring matcher using the ahocorasick-based automaton.
#[pyclass]
pub(crate) struct StrMatch {
    trie: TrieType,
}
#[pymethods]
impl StrMatch {
    #[new]
    fn new(patterns: Vec<String>) -> Self {
        let mut trie = TrieType::ArrayTrie(array_impl::Trie::new());
        for p in &patterns {
            trie.add_word(p);
        }
        trie.set_suffix_links();
        Self { trie }
    }
    /// Searches for substring patterns in the text
    fn search_substr(&self, text: &str) -> HashSet<String> {
        self.trie.search(text)
    }
    /// Searches for the amount of occurences of substring patterns in the text
    fn search_substr_count(&self, text: &str) -> HashMap<String, usize> {
        self.trie.search_occurences(text)
    }
}
