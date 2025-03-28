use std::collections::HashMap;

use rand::distr::Distribution;

#[derive(Debug)]
struct HashMapTrie {
    next: HashMap<char, HashMapTrie>,
}

impl HashMapTrie {
    fn new() -> Self {
        Self {
            next: HashMap::new(),
        }
    }
    fn add_word(&mut self, word: &str) {
        if let Some(char) = word.chars().next() {
            match self.next.get_mut(&char) {
                // Continue down next level since this
                // level is finite from a-z
                Some(trie) => {
                    // Continue with substring minus head
                    // in case next characters expands lookup
                    trie.add_word(&word[1..])
                }
                None => {
                    // New character entry expands lookup
                    let mut trie = HashMapTrie::new();
                    trie.add_word(&word[1..]);
                    self.next.insert(char, trie);
                }
            }
        }
    }
}

#[derive(Debug, Default)]
struct Vertex {
    next: [Option<i32>; 26],
    output: bool,
    parent: Option<i32>,
    value: Option<char>,
    link: Option<i32>,
    transitions: [Option<i32>; 26],
}
impl Vertex {
    fn new(parent: i32, value: char) -> Self {
        Self {
            next: [None; 26],
            output: false,
            parent: Some(parent),
            link: None,
            value: Some(value),
            transitions: [None; 26],
        }
    }
}
#[derive(Debug)]
struct ArrayTrie {
    pub vertices: Vec<Vertex>,
}
impl ArrayTrie {
    fn new() -> Self {
        Self {
            vertices: vec![Vertex::default()],
        }
    }
    fn add_word(&mut self, word: &str) {
        // Current character starts as root
        let mut current_parent = 0usize;
        for char in word.chars() {
            // Normalize within 0-25 range
            let char_as_int = (char as u8 - b'a') as usize;
            // Since next array is prefilled index will always
            // exist in predefined range
            if self.vertices[current_parent]
                .next
                .get(char_as_int)
                .unwrap()
                .is_none()
            {
                // Point character to new array index
                self.vertices[current_parent].next[char_as_int] = Some(self.vertices.len() as i32);
                self.vertices.push(Vertex::new(current_parent as i32, char));
            }
            current_parent = self.vertices[current_parent].next[char_as_int].unwrap() as usize;
        }
        self.vertices[current_parent].output = true;
    }
    fn get_link(&mut self, char_pointer: usize) -> i32 {
        if self.vertices[char_pointer].link.is_none() {
            if char_pointer == 0 && self.vertices[char_pointer].parent.is_none() {
                // Since we can not transition anywhere and have hit the root we
                // set suffix link to the root which is always zero
                self.vertices[char_pointer].link = Some(0);
            } else {
                // We follow the suffix links to find
                // the best route while memomizing on the way
                let link = self.get_link(self.vertices[char_pointer].parent.unwrap() as usize);
                self.vertices[char_pointer].link =
                    Some(self.go(link as usize, self.vertices[char_pointer].value.unwrap()));
            }
        };
        return self.vertices[char_pointer].link.unwrap();
    }
    fn go(&mut self, char_pointer: usize, char: char) -> i32 {
        // Normalize within 0-25 range
        let char_as_int = (char as u8 - b'a') as usize;
        if self.vertices[char_pointer].transitions[char_as_int].is_none() {
            if self.vertices[char_pointer].next[char_as_int].is_some() {
                self.vertices[char_pointer].transitions[char_as_int] = self.vertices[char_pointer].next[char_as_int];
            }
            else {
                self.vertices[char_pointer].transitions[char_as_int] = if char_pointer == 0 {
                    Some(0)
                }
                 else {
                    let link = self.get_link(char_pointer as usize) as usize;
                    Some(self.go(link, char))
                 }
            }
        }
        return self.vertices[char_pointer].transitions[char_as_int].unwrap()
    }
}

#[test]
fn trie_hashmap_impl() {
    use rand::distr::Alphanumeric;
    use rand::Rng; // Import the rand crate

    fn generate_random_string(length: usize) -> String {
        let mut rng = rand::thread_rng();
        (0..length)
            .map(|_| rng.sample(Alphanumeric) as char) // Generate random characters
            .collect() // Collect into a String
    }

    fn generate_random_strings(num_strings: usize, max_length: usize) -> Vec<String> {
        let mut rng = rand::thread_rng();
        (0..num_strings)
            .map(|_| {
                let length = rng.gen_range(1..=max_length); // Random length for each string
                generate_random_string(length)
            })
            .collect()
    }

    // Generate test patterns
    let num_strings = 1_000_000;
    let max_length = 20;
    let random_strings = generate_random_strings(num_strings, max_length);

    let mut t = HashMapTrie::new();
    for string in random_strings.iter() {
        t.add_word(string);
    }
}
#[test]
fn trie_array_impl() {
    use rand::distr::Uniform;
    use rand::Rng; // Import the rand crate

    fn generate_random_string(length: usize) -> String {
        let mut rng = rand::thread_rng();
        let alphabet = Uniform::new_inclusive(b'a', b'z').unwrap();
        (0..length)
            .map(|_| alphabet.sample(&mut rng) as char) // Generate random characters
            .collect() // Collect into a String
    }

    fn generate_random_strings(num_strings: usize, max_length: usize) -> Vec<String> {
        let mut rng = rand::thread_rng();
        (0..num_strings)
            .map(|_| {
                let length = rng.gen_range(1..=max_length); // Random length for each string
                generate_random_string(length)
            })
            .collect()
    }

    // Generate test patterns
    let num_strings = 1_000_000;
    let max_length = 20;
    let random_strings = generate_random_strings(num_strings, max_length);

    let mut t = ArrayTrie::new();
    for string in random_strings.iter() {
        t.add_word(string);
    }
    dbg!(t.vertices.len());
}

#[test]
fn trie_automation() {
    let mut t = ArrayTrie::new();
    t.add_word("a");
    t.add_word("ab");
    t.add_word("bc");
    t.add_word("bca");
    t.add_word("c");
    t.add_word("caa");
    dbg!(t);
}
