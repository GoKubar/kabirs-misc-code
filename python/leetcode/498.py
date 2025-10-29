class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        ret = [[].copy() for i in range(len(mat) + len(mat[0]))]

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if (i + j) % 2 == 0:
                    ret[i + j].insert(0, mat[i][j])
                else:
                    ret[i + j].append(mat[i][j])

        actual_ret = []

        for li in ret:
            actual_ret += li

        return actual_ret
