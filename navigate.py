from random import randint, choice


class Board:
    def __init__(self, size, value=0):
        self.size = size
        self.mat = [[value] * size for _ in range(size)]
        return

    def drop_apple(self):
        new_apple = (randint(0, self.size-1), randint(0, self.size-1))
        while self.is_blocked(new_apple):
            new_apple = (randint(0, self.size-1), randint(0, self.size-1))
        return new_apple

    def set(self, *positions, value=-1):
        for position in positions:
            self.mat[position[0]][position[1]] = value
        return

    def minus(self, *positions):
        for position in positions:
            self.mat[position[0]][position[1]] -= 1
        return

    def is_blocked(self, position, distance=0):
        return False if 0 <= self.mat[position[0]][position[1]] <= distance else True
        # return self.mat[position[0]][position[1]]

    def __repr__(self):
        for _ in range(self.size):
            return ('\n'.join(["".join(
                [f"{self.mat[i][j]: 3}" for j in range(self.size)]) for i in range(self.size)]))

    # Classic
    def neighbors(self, pos, visited=None, distance=0):
        if not visited:
            visited = self

        def fix(n):
            if 0 <= n < self.size:
                return n
            elif n < 0:
                return n + self.size
            else:
                return n % self.size

        positions = [(fix(pos[0]+1), pos[1]), (fix(pos[0]-1), pos[1]),
                     (pos[0], fix(pos[1]+1)), (pos[0], fix(pos[1]-1))]
        return [position for position in positions if not (self.is_blocked(position, distance) or visited.is_blocked(position))]

    def find_path(self, start, target):
        path = {}
        queue = Heap()
        visited = Board(self.size)
        distances = {
            start: 0
        }
        for neighbor in self.neighbors(start, distance=1):
            queue.push((neighbor, 1))
            path[neighbor] = start
        visited.set(start)
        while queue.data:
            pos, distance = queue.pop()

            if pos == target:
                break
            if visited.is_blocked(pos):
                continue
            visited.set(pos)
            distances[pos] = distance
            for neighbor in self.neighbors(pos, visited, distance):
                queue.push((neighbor, distance + 1))
                path[neighbor] = pos

        try:
            try:
                step = target
                steps = [step]
                while path[step] != start:
                    step = path[step]
                    steps.append(step)
                return steps
            except KeyError:
                return [choice(self.neighbors(start, Board(self.size), distance=1))]
        except:
            return None


class Heap:
    def __init__(self):
        self.data = []
        return

    def push(self, *pairs):
        for pair in pairs:
            self.data.append(pair)
        self.data.sort(key=lambda a: a[1])
        return

    def pop(self):
        return self.data.pop(0)


# board = Board(20)
# board.set(*[(8, i) for i in range(17)], value=1)
# board.set(*[(16, i) for i in range(5, 20)], value=1)
# board.set(*[(0, i) for i in range(20)], value=1)
# board.set(*[(i, 0) for i in range(20)], value=1)
# board.set(*[(20-1, i) for i in range(20)], value=1)
# board.set(*[(i, 20-1) for i in range(20)], value=1)
# board.set(*board.find_path((1, 1), (18, 18)))
# print(board)
