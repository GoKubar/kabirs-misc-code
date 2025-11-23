use std::collections::HashMap;

fn main() {
    let text = "the quick brown fox jumped over the lazy dog";

    let mut counts = HashMap::new();

    for word in text.split_whitespace() {
        let count = counts.entry(word).or_insert(0);
        *count += 1;
    }

    println!("{counts:?}");
}
