// #[derive(Debug)]
// enum UsState {
//     Alabama,
//     Alaska,
//     Delaware,
//     //more
// }
//
// enum Coin {
//     Penny,
//     Nickel,
//     Dime,
//     Quarter(UsState),
// }

// impl Coin {
//     fn value(&self) -> usize {
//         match self {
//             Coin::Penny => {
//                 println!("Lucky Penny!");
//                 1
//             }
//             Coin::Nickel => 5,
//             Coin::Dime => 10,
//             Coin::Quarter(state) => {
//                 println!("Quarter from {state:?}!");
//                 25
//             }
//         }
//     }
// }

fn main() {
    let dice_roll: u8 = 5;
}

fn process_roll(roll: u8) {
    match roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        _ => move_player(),
    }
}

fn add_fancy_hat() {}
fn remove_fancy_hat() {}
fn move_player() {}
fn move_player(num_spaces: u8) {}
