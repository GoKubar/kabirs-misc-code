class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        ret = target[0]
        last = target[0]

        for num in target[1:]:
            if num > last:
                ret += num - last
            last = num

        return ret
