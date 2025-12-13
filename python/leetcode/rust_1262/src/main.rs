use std::{
    cmp::{Reverse, max},
    collections::BinaryHeap,
};

impl Solution {
    pub fn max_sum_div_three(nums: Vec<i32>) -> i32 {
        let sum = nums.iter().sum();

        if sum % 3 == 0 {
            return sum;
        }

        let mut mod1s = BinaryHeap::new();
        let mut mod2s = BinaryHeap::new();

        for num in nums {
            if num % 3 == 1 {
                mod1s.push(Reverse(num));
            } else if num % 3 == 2 {
                mod2s.push(Reverse(num));
            }
        }

        let mut candidate1: Option<i32> = None;
        let mut candidate2: Option<i32> = None;

        if sum % 3 == 1 {
            if mod1s.len() >= 1 {
                candidate1 = Some(&sum - mod1s.peek().unwrap().0);
            }

            if mod2s.len() >= 2 {
                let num1 = mod2s.pop().unwrap();
                let num2 = mod2s.pop().unwrap();

                candidate2 = Some(&sum - (num1.0 + num2.0));
            }
        } else {
            if mod1s.len() >= 2 {
                let num1 = mod1s.pop().unwrap();
                let num2 = mod1s.pop().unwrap();

                candidate1 = Some(&sum - (num1.0 + num2.0));
            }

            if mod2s.len() >= 1 {
                candidate2 = Some(&sum - mod2s.peek().unwrap().0);
            }
        }

        Self::max_of_options(candidate1, candidate2)
    }

    pub fn max_of_options(x: Option<i32>, y: Option<i32>) -> i32 {
        let unwrapped_x = match x {
            Some(n) => n,
            None => 0,
        };

        let unwrapped_y = match y {
            Some(n) => n,
            None => 0,
        };

        max(unwrapped_x, unwrapped_y)
    }
}
