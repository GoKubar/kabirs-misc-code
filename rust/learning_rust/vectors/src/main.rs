fn main() {
    let mut v = vec![100, 32, 57];

    print_vec(&mut v);
}

fn print_vec(v: &mut Vec<i32>) {
    let mut s = String::new();

    s.push_str("[");

    for i in &mut *v {
        *i += 1;
    }

    for (i, val) in v.iter().enumerate() {
        s.push_str(format!("{val}").as_str());

        if i != v.len() - 1 {
            s.push_str(", ");
        }
    }

    s.push_str("]");

    println!("{s}");
}
