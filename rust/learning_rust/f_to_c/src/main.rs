use std::io;

fn main() {
    let mut fahreinheit = String::new();
    println!("Enter the temperature in fahreinheit:");
    io::stdin()
        .read_line(&mut fahreinheit)
        .expect("Line not read");

    let fahreinheit: f64 = fahreinheit
        .trim()
        .parse()
        .expect("Please enter a valid number");

    println!("{}", convert(fahreinheit));
}

fn convert(fahreinheit: f64) -> f64 {
    (fahreinheit - 32.0) / 1.8
}

fn foo() {
    println!("This is a function foo");
}

fn bar() {
    println!("This is a function bar");
    println!("");
}
