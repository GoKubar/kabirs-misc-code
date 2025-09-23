class Solution:
    def countSquares(self, matrix: List[List[int]]) -> int:
        dp = [([0] * len(matrix[0])).copy() for _ in range(len(matrix))]

        dp[0] = matrix[0]

        for j in range(1, len(matrix)):
            dp[j][0] = matrix[j][0]

        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[0])):
                dp[i][j] = (
                    0
                    if matrix[i][j] == 0
                    else min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                )

        for row in dp:
            print(row)

        return sum([sum(row) for row in dp])
