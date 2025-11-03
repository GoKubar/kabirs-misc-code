class Solution:
    def numberOfBeams(self, bank: List[str]) -> int:

        last = 0

        ret = 0

        for i, row in enumerate(bank):
            num_objs = row.count("1")

            if not num_objs:
                continue

            if not last:
                last = num_objs
                continue

            ret += num_objs * last

            last = num_objs

        return ret
