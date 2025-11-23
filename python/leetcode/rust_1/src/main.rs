use std::collections::HashMap;

impl Solution {
    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
        let mut map: HashMap<i32, i32> = HashMap::new();
        let mut ret: Vec<i32> = Vec::new();
        for (i as i32, num) in nums.iter().enumerate() {
            let other = &target - num;
            if map.contains_key(&other) {
                ret.push(i as i32);
                ret.push(*map.get(&other).unwrap());
            } else {
                map.insert(*num, i as i32);
            }
        }

        ret
    }
}
