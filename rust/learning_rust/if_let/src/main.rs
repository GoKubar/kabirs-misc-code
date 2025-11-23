#[derive(Debug)]
#[allow(unused)]
enum UsState {
    Alabama,
    Alaska,
    Arizona,
    Arkansas,
    California,
    Colorado,
    Connecticut,
    Delaware,
    Florida,
    Georgia,
    Hawaii,
    Idaho,
    Illinois,
    Indiana,
    Iowa,
    Kansas,
    Kentucky,
    Louisiana,
    Maine,
    Maryland,
    Massachusetts,
    Michigan,
    Minnesota,
    Mississippi,
    Missouri,
    Montana,
    Nebraska,
    Nevada,
    NewHampshire,
    NewJersey,
    NewMexico,
    NewYork,
    NorthCarolina,
    NorthDakota,
    Ohio,
    Oklahoma,
    Oregon,
    Pennsylvania,
    RhodeIsland,
    SouthCarolina,
    SouthDakota,
    Tennessee,
    Texas,
    Utah,
    Vermont,
    Virginia,
    Washington,
    WestVirginia,
    Wisconsin,
    Wyoming,
}

#[allow(unused)]
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}

#[allow(unused)]
impl UsState {
    fn created_in(&self) -> u16 {
        match self {
            UsState::Delaware => 1789,
            _ => 2025, //the year of our lord and savior DJT
        }
    }

    fn existed_in(&self, year: u16) -> bool {
        self.created_in() <= year
    }
}

fn main() {
    // let coin = Coin::Quarter(UsState::Alaska);
    let coin = Coin::Penny;

    let msg: Option<String> = describe_state_quarter(coin);

    if let Some(str) = msg {
        println!("The quarter is {str}");
    } else {
        println!("Not a quarter");
    }
}

fn describe_state_quarter(coin: Coin) -> Option<String> {
    let Coin::Quarter(state) = coin else {
        return None;
    };

    if state.existed_in(1900) {
        Some(String::from("OLDDDDD"))
    } else {
        Some(String::from("BORRRINGGGG"))
    }
}
