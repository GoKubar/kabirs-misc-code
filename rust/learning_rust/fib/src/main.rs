use num_bigint::BigUint;
use num_traits::{One, Zero};
use std::{cmp::Ordering, io};
fn main() {
    let mut arr: [BigUint; 2] = [BigUint::one(), BigUint::zero()];
    let mut curr = 1;

    let mut n = String::new();
    println!("Enter the fibonacci number that you want:");

    io::stdin().read_line(&mut n).expect("Line not read");

    let n: usize = n.trim().parse().expect("Enter a valid fib number");
    loop {
        if curr % 1000000 == 0 {
            println!("Reached {curr}nth fib number");
        }
        match curr.cmp(&n) {
            Ordering::Greater => {
                println!("{}", arr[0]);
                break;
            }
            Ordering::Less => {
                let temp = arr[1].clone();
                arr[1] += arr[0].clone();
                arr[0] = temp.clone();
            }
            Ordering::Equal => {
                println!("len of number: {}", arr[1].to_string().len());
                break;
            }
        }
        curr += 1;
    }
}
