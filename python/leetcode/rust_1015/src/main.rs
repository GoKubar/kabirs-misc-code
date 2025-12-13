impl Solution {
    pub fn smallest_repunit_div_by_k(k: i32) -> i32 {
        if k % 2 == 0 || k % 5 == 0 {
            return -1;
        }

        let mut curr: i32 = 1 % k;

        for i in 1..=k {
            if curr == 0 {
                return i;
            }

            curr = (curr * 10 + 1) % k;
        }

        0
    }
}
