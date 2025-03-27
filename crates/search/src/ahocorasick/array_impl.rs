use std::{
    collections::{HashMap, HashSet, VecDeque},
    sync::{Arc, RwLock},
};

const ARRAY_REPEAT_NODE: Option<Arc<RwLock<Node>>> = None;
const ALPHA_NUMERIC_SPECIAL: usize = 128;

#[derive(Debug)]
struct Node {
    /// Transitions possible from current character
    children: Vec<Option<Arc<RwLock<Node>>>>,
    /// List of pointers to full suffix words
    output: Vec<usize>,
    /// Character value
    value: Option<char>,
    /// Suffix link (failure links)
    link: Option<Arc<RwLock<Node>>>,
}
impl Node {
    fn new(value: char) -> Self {
        Self {
            children: [ARRAY_REPEAT_NODE; ALPHA_NUMERIC_SPECIAL].to_vec(),
            output: Vec::new(),
            link: None,
            value: Some(value),
        }
    }
}
impl Default for Node {
    fn default() -> Self {
        Self {
            children: [ARRAY_REPEAT_NODE; ALPHA_NUMERIC_SPECIAL].to_vec(),
            output: Vec::new(),
            link: None,
            value: None,
        }
    }
}
#[derive(Debug)]
pub(crate) struct Trie {
    root: Arc<RwLock<Node>>,
    words: Vec<String>,
}
impl Trie {
    pub(crate) fn new() -> Self {
        Self {
            root: Arc::new(Node::default().into()),
            words: Vec::new(),
        }
    }
    fn follow_suffix_links(&self, current_node: &mut Arc<RwLock<Node>>, idx: usize) {
        // Follow suffix links if no direct transition exists
        loop {
            let node = current_node.clone();
            let node = node.read().unwrap();

            // Transition found so continue in depth
            if let Some(transition) = &node.children[idx] {
                *current_node = transition.clone();
                break;
            }
            if let Some(link) = &node.link {
                *current_node = link.clone();
            } else {
                break;
            }
        }
    }
    fn search_internal<F>(&self, text: &str, mut collect: F)
    where
        F: FnMut(String),
    {
        let current_node = &mut self.root.clone();

        for ch in text.chars() {
            let char_as_idx = self.char_as_idx(ch);

            self.follow_suffix_links(current_node, char_as_idx);

            // Collect words along the suffix link chain
            let mut temp_node = Some(current_node.clone());
            while let Some(node) = temp_node.take() {
                let node = node.read().unwrap();
                for &word_idx in &node.output {
                    // Retrieve word from global list
                    let word = self.words[word_idx].clone();
                    collect(word);
                }
                // Continue following suffix links (failure links)
                temp_node = node.link.clone();
            }
        }
    }
    /// Searches for builtin substring patterns in the text
    pub(crate) fn search(&self, text: &str) -> HashSet<String> {
        let mut output = HashSet::new();

        self.search_internal(text, |word| {
            output.insert(word);
        });

        output
    }
    /// Searches for the amount of occurences of builtin substring patterns in the text
    pub(crate) fn search_occurences(&self, text: &str) -> HashMap<String, usize> {
        let mut output = HashMap::new();

        self.search_internal(text, |word| {
            *output.entry(word).or_insert(0usize) += 1usize;
        });

        output
    }
    pub(crate) fn add_word(&mut self, word: &str) {
        // Store global lookup
        self.words.push(word.to_string());

        // Current node character
        let mut current_node = self.root.clone();

        for char in word.chars() {
            let char_as_idx = self.char_as_idx(char);
            {
                let mut current_node_lock = current_node.write().unwrap();
                // Normalize within 0-127 range
                // Since next array is prefilled index will always
                // exist in predefined range
                if current_node_lock
                    .children
                    .get(char_as_idx)
                    .unwrap()
                    .is_none()
                {
                    // Extend possible transitions from current character to new character
                    current_node_lock.children[char_as_idx] =
                        Some(Arc::new(Node::new(char).into()));
                }
            }
            current_node = current_node.clone().read().unwrap().children[char_as_idx]
                .clone()
                .unwrap();
        }
        current_node
            .write()
            .unwrap()
            .output
            .push(self.words.len() - 1);
    }
    fn char_as_idx(&self, char: char) -> usize {
        char as u8 as usize
    }
    /// The suffix links are used to efficiently search for the longest suffix that matches
    /// when a mismatch occurs in the trie traversal.
    pub(crate) fn set_suffix_links(&mut self) {
        let mut queue = VecDeque::new();

        // Links at depth level one always link back to root
        let root_lock = self.root.write().unwrap();
        for transition in &root_lock.children {
            if let Some(transition) = transition {
                transition.write().unwrap().link = Some(self.root.clone());
                queue.push_back(transition.clone());
            }
        }
        drop(root_lock);

        // Find all suffix links
        while let Some(current_node) = queue.pop_front() {
            let current_node_lock = current_node.read().unwrap();
            for transition in &current_node_lock.children {
                if let Some(transition) = transition {
                    let mut current_link = current_node_lock.link.clone();
                    while let Some(link) = current_link {
                        // Find a transition to longest suffix (suffix_link) from current transition
                        let link_lock = link.read().unwrap();
                        let found = link_lock.children.iter().find(|child| {
                            child.as_ref().is_some_and(|c| {
                                c.read().unwrap().value == transition.read().unwrap().value
                            })
                        });
                        if let Some(found) = found {
                            transition.write().unwrap().link = found.clone();
                            break;
                        }
                        // Follow the suffix links trail
                        current_link = link_lock.link.clone();
                    }
                    // Sometimes suffix links can't be created
                    // so we must fallback to root so traveling the
                    // suffix links is always completed
                    if transition.read().unwrap().link.is_none() {
                        transition.write().unwrap().link = Some(self.root.clone())
                    }

                    queue.push_back(transition.clone());
                }
            }
        }
    }
}

#[cfg(test)]
mod unit_tests {
    use crate::ahocorasick::array_impl::{Node, Trie};
    use rand::distr::Distribution as _;
    use std::sync::{Arc, RwLock};

    #[test]
    fn trie_search_test() {
        // Generate trie with suffix links
        let mut trie = Trie::new();
        trie.add_word("hasfailed");
        trie.add_word("ed");
        trie.add_word("failed");
        trie.add_word("atabase");
        trie.set_suffix_links();
        let res = trie.search("abasehasfailed");
        assert!(res.get("hasfailed").is_some());
        assert!(res.get("ed").is_some());
        assert!(res.get("failed").is_some());
    }

    #[test]
    fn trie_benchmark() {
        use rand::distr::Uniform;
        use rand::Rng; // Import the rand crate

        fn generate_random_string(length: usize) -> String {
            let mut rng = rand::rng();
            let alphabet = Uniform::new_inclusive(b'a', b'z').unwrap();
            (0..length)
                .map(|_| alphabet.sample(&mut rng) as char) // Generate random characters
                .collect() // Collect into a String
        }

        fn generate_random_strings(num_strings: usize, max_length: usize) -> Vec<String> {
            let mut rng = rand::rng();
            (0..num_strings)
                .map(|_| {
                    let length = rng.random_range(1..=max_length); // Random length for each string
                    generate_random_string(length)
                })
                .collect()
        }

        // Generate test patterns
        let num_strings = 1_000_000;
        let max_length = 20;
        let random_strings = generate_random_strings(num_strings, max_length);

        let mut t = Trie::new();
        for string in random_strings.iter() {
            t.add_word(string);
        }
    }

    #[test]
    fn trie_char_set_depth_one_test() {
        // Generate trie with max depth
        let mut trie = Trie::new();
        for c in 'a'..='z' {
            trie.add_word(&c.to_string());
        }

        // Verify depth 1
        let root_lock = trie.root.read().unwrap();
        for (index, expected_char) in ('a'..='z').enumerate() {
            let node = root_lock.children[index]
                .clone()
                .expect("Node should exist");
            let node_lock = node.read().unwrap();
            assert_eq!(
                node_lock.value,
                Some(expected_char),
                "Mismatch at index {}",
                index
            );
        }
    }

    #[test]
    fn trie_char_set_depth_max_test() {
        // Generate trie with max depth
        let mut trie = Trie::new();
        let mut word = String::new();
        for c in 'a'..='z' {
            word.push(c);
            trie.add_word(&word);
        }

        // Verify depth characters
        let mut current_node = trie.root.clone();
        for (index, expected_char) in ('a'..='z').enumerate() {
            {
                let current_node_lock = current_node.read().unwrap();
                let node = current_node_lock.children[index]
                    .clone()
                    .expect("Node should exist");
                let node_lock = node.read().unwrap();
                assert_eq!(
                    node_lock.value.unwrap(),
                    expected_char,
                    "Mismatch at index {} found: {}",
                    index,
                    node_lock.value.unwrap()
                );
            }

            // Move to the next level for the next iteration
            current_node = current_node.clone().read().unwrap().children[index]
                .clone()
                .unwrap();
        }
    }

    #[test]
    fn trie_suffix_links_test() {
        // Generate trie with suffix links
        let mut trie = Trie::new();
        trie.add_word("bab");
        trie.add_word("a");
        trie.add_word("ab");
        trie.add_word("bc");
        trie.add_word("bca");
        trie.add_word("caa");
        trie.set_suffix_links();

        // Helper function to check suffix links
        fn assert_suffix_link(
            node: Arc<RwLock<Node>>,
            expected_link: Option<Arc<RwLock<Node>>>,
            message: &str,
        ) {
            let actual_link = node.read().unwrap().link.clone();
            assert_eq!(
                actual_link.as_ref().map(|n| Arc::as_ptr(n)),
                expected_link.as_ref().map(|n| Arc::as_ptr(n)),
                "{}",
                message
            );
        }

        // Get references to key nodes
        let root = trie.root.clone();
        let root_lock = root.read().unwrap();
        let a = root_lock.children[0].as_ref().unwrap().clone(); // 'a'
        let b = root_lock.children[1].as_ref().unwrap().clone(); // 'b'
        let c = root_lock.children[2].as_ref().unwrap().clone(); // 'c'
        let ba = b.read().unwrap().children[0].as_ref().unwrap().clone(); // "ba"
        let ab = a.read().unwrap().children[1].as_ref().unwrap().clone(); // "ab"
        let bab = ba.read().unwrap().children[1].as_ref().unwrap().clone(); // "bab"
        let bc = b.read().unwrap().children[2].as_ref().unwrap().clone(); // "bc"
        let bca = bc.read().unwrap().children[0].as_ref().unwrap().clone(); // "bca"
        let ca = c.read().unwrap().children[0].as_ref().unwrap().clone(); // "ca"
        let caa = c.read().unwrap().children[0].as_ref().unwrap().clone(); // "caa"

        // Root links to itself (implicitly)
        assert_suffix_link(root.clone(), None, "Root should have no suffix link.");
        // 'a', 'b', and 'c' should all link back to root
        assert_suffix_link(a.clone(), Some(root.clone()), "'a' should link to root.");
        assert_suffix_link(b.clone(), Some(root.clone()), "'b' should link to root.");
        assert_suffix_link(c.clone(), Some(root.clone()), "'c' should link to root.");
        // "ab" should link to "b"
        assert_suffix_link(ab.clone(), Some(b.clone()), "'ab' should link to 'b'.");
        // "bab" should link to "ab"
        assert_suffix_link(bab.clone(), Some(ab.clone()), "'bab' should link to 'ab'.");
        // "bc" should link to "c"
        assert_suffix_link(bc.clone(), Some(c.clone()), "'bc' should link to 'c'.");
        // "bca" should link to "ca"
        assert_suffix_link(bca.clone(), Some(ca.clone()), "'bca' should link to 'ca'.");
        // "caa" should link to "a"
        assert_suffix_link(caa.clone(), Some(a.clone()), "'caa' should link to 'a'.");
    }
}
