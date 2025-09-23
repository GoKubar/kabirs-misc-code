import heapq as hq


def top(pos):
    return (pos[0] - 1, pos[1])


def bottom(pos):
    return (pos[0] + 1, pos[1])


def right(pos):
    return (pos[0], pos[1] + 1)


def left(pos):
    return (pos[0], pos[1] - 1)


class Solution:
    def minCost(self, startPos, homePos, rowCosts, colCosts) -> int:
        m, n = len(rowCosts), len(colCosts)

        def is_valid(pos):
            return (0 <= pos[0] < m) and (0 <= pos[1] < n)

        startPos = tuple(startPos)
        homePos = tuple(homePos)

        visited = set()
        visited.add(startPos)

        pq = []

        hq.heapify(pq)

        curr = (0, startPos)

        while curr[1] != homePos:
            if is_valid(top(curr[1])) and top(curr[1]) not in visited:
                hq.heappush(pq, (curr[0] + rowCosts[top(curr[1])[0]], top(curr[1])))
            elif is_valid(bottom(curr[1])) and bottom(curr[1]) not in visited:
                hq.heappush(
                    pq, (curr[0] + rowCosts[bottom(curr[1])[0]], bottom(curr[1]))
                )
            elif is_valid(right(curr[1])) and right(curr[1]) not in visited:
                hq.heappush(pq, (curr[0] + colCosts[right(curr[1])[1]], right(curr[1])))
            elif is_valid(left(curr[1])) and left(curr[1]) not in visited:
                hq.heappush(pq, (curr[0] + colCosts[left(curr[1])[1]], left(curr[1])))

            curr = hq.heappop(pq)

            visited.add(curr[1])

        return curr[0]
