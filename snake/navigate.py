from random import randint, choices


class Board:
    def __init__(self, size, value=0):
        self.size = size
        self.mat = [[value] * size for _ in range(size)]
        return

    def drop_apple(self):
        new_apple = (randint(0, self.size-1), randint(0, self.size-1))
        while self.is_blocked(new_apple, distance=0):
            new_apple = (randint(0, self.size-1), randint(0, self.size-1))
        return new_apple, choices([1, 2, 3, 4, 5], weights=[0.26, 0.25, 0.25, 0.12, 0.12], k=1)[0]

    def set(self, *positions, value=-1):
        for position in positions:
            self.mat[position[0]][position[1]] = value
        return

    def minus(self, *positions):
        for position in positions:
            self.mat[position[0]][position[1]] -= 1
        return

    def is_blocked(self, position, distance=1):
        return False if 0 <= self.mat[position[0]][position[1]] <= distance else True
        # return self.mat[position[0]][position[1]]

    def __repr__(self):
        for _ in range(self.size):
            return ('\n'.join(["".join(
                [f"{self.mat[i][j]: 3}" for j in range(self.size)]) for i in range(self.size)]))

    def fix(self, n):
        if 0 <= n < self.size:
            return n
        elif n < 0:
            return n + self.size
        else:
            return n % self.size

    # Classic
    def neighbors(self, pos, visited=None, distance=1):
        if not visited:
            visited = self

        positions = [(self.fix(pos[0]+1), pos[1]), (self.fix(pos[0]-1), pos[1]),
                     (pos[0], self.fix(pos[1]+1)), (pos[0], self.fix(pos[1]-1))]
        return [position for position in positions if not (self.is_blocked(position, distance) or visited.is_blocked(position))]

    def find_path(self, start, targets):
        path = self.dijkstra(start, targets)
        if not path:
            return self.alternative_path(start)
        return path

    def dijkstra(self, start, targets):
        path = {}
        queue = Heap()
        visited = Board(self.size)
        distances = {
            start: 0
        }
        for neighbor in self.neighbors(start):
            queue.push((neighbor, 1))
            path[neighbor] = start
        visited.set(start)
        pos = None
        while queue.data:
            pos, distance = queue.pop()

            if pos in targets:
                if self.neighbors(pos, distance=distance) == [path[pos]] or not self.neighbors(pos, distance=distance):
                    return []
                # print(self.neighbors(target, distance=distance))
                break
            if visited.is_blocked(pos):
                continue
            visited.set(pos)
            distances[pos] = distance
            for neighbor in self.neighbors(pos, visited, distance):
                queue.push((neighbor, distance+1))
                path[neighbor] = pos

        try:
            if pos in targets:
                step = pos
                steps = [step]
                while path[step] != start:
                    step = path[step]
                    steps.append(step)
                return steps
            else:
                return []
        except KeyError:
            return []

    def alternative_path(self, start):
        possible_moves = self.neighbors(start, distance=1)
        priority = []

        for pos in possible_moves:
            direction = (pos[0]-start[0], pos[1]-start[1])

            # forward = (pos[0]+direction[0], pos[1]+direction[1])
            # turn1 = (pos[0]+direction[1], pos[1]+direction[0])
            # turn2 = (pos[0]-direction[1], pos[1]-direction[0])
            # print(pos, direction, forward, self.is_blocked(forward),
            #       turn1, self.is_blocked(turn1), turn2, self.is_blocked(turn2))

            forward = self.is_blocked(
                (self.fix(pos[0]+direction[0]), self.fix(pos[1]+direction[1])))
            turn1 = self.is_blocked(
                (self.fix(pos[0]+direction[1]), self.fix(pos[1]+direction[0])))
            turn2 = self.is_blocked(
                (self.fix(pos[0]-direction[1]), self.fix(pos[1]-direction[0])))

            if turn1 and turn2:
                if not forward:
                    priority.append((pos, -1))
                else:
                    priority.append((pos, -2))
            elif turn1 or turn2:
                if forward:
                    priority.append((pos, 3))
                else:
                    priority.append((pos, 2))
            elif forward:
                priority.append((pos, 1))
            else:
                priority.append((pos, 0))

        # print([item[1] for item in priority])
        priority.sort(key=lambda a: a[1])

        if priority:
            return [item[0] for item in priority]
        return []


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
