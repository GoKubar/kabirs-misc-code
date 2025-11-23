// Definition for singly-linked list.
// #[derive(PartialEq, Eq, Clone, Debug)]
// pub struct ListNode {
//   pub val: i32,
//   pub next: Option<Box<ListNode>>
// }
//
// impl ListNode {
//   #[inline]
//   fn new(val: i32) -> Self {
//     ListNode {
//       next: None,
//       val
//     }
//   }
// }
impl Solution {
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        let mut carry = 0;
        let mut curr1 = &l1;
        let mut curr2 = &l2;

        let mut res = Box::new(ListNode { val: 0, next: None });

        let mut curr = &mut res;

        while curr1 != None && curr2 != None {
            let mut curr_val: i32 = curr1.val + curr2.val + carry;

            carry = &curr_val / 10;
            curr_val %= 10;

            curr.val = &curr_val;

            curr.next = Box::new(ListNode { val: 0, next: None });
            curr = curr.next.as_mut().unwrap();

            curr1 = curr1.next;
            curr2 = curr2.next;
        }

        while curr1 != None {
            let mut curr_val: i32 = curr1.val + carry;

            carry = &curr_val / 10;
            curr_val %= 10;

            curr.val = &curr_val;

            curr.next = Box::new(ListNode { val: 0, next: None });
            curr = curr.next.as_mut().unwrap();

            curr1 = curr1.next;
        }

        while curr2 != None {
            let mut curr_val: i32 = curr2.val + carry;

            carry = &curr_val / 10;
            curr_val %= 10;

            curr.val = &curr_val;

            curr.next = Box::new(ListNode { val: 0, next: None });
            curr = curr.next.as_mut().unwrap();

            curr2 = curr2.next;
        }

        Some(res)
    }
}
