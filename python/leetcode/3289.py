class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        seen = set()

        ret = []

        for num in nums:
            if num in seen:
                ret.append(num)

                if len(ret) == 2:
                    return ret

            else:
                seen.add(num)
