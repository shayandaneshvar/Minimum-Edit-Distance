import enum

import numpy as np


class Direction(enum.Enum):
    Left = 1
    Up = 2
    UpLeft = 3

    @staticmethod
    def get_char(dir_value: int) -> str:
        if dir_value == Direction.Left.value:
            return '←'
        elif dir_value == Direction.Up.value:
            return '↑'
        elif dir_value == Direction.UpLeft.value:
            return '↖'
        else:
            return ''


class MinimumEditDistance:
    def __init__(self, x: str, y: str, substitution_cost: int = 2,
                 del_cost: int = 1, insertion_cost: int = 1) -> None:
        super().__init__()
        self.y = y
        self.x = x
        self.ins_cost = insertion_cost
        self.del_cost = del_cost
        self.sub_cost = substitution_cost
        self.rows = 1 + len(x)
        self.cols = 1 + len(y)
        self.distance_matrix = np.zeros((self.rows, self.cols))
        self.direction_matrix = np.zeros((self.rows, self.cols, 3))
        self.__calculate_distance()
        self.__calculate_direction()

    def __calculate_distance(self) -> None:
        """
            calculates Minimum Edit Distance of X to Y
            sub,del and ins costs are set in the constructor
        """
        for i in range(0, self.rows):
            self.distance_matrix[i, 0] = i

        for j in range(0, self.cols):
            self.distance_matrix[0, j] = j

        for i in range(1, self.rows):
            for j in range(1, self.cols):
                sub_cost = self.sub_cost
                if self.x[i - 1] == self.y[j - 1]:
                    sub_cost = 0
                self.distance_matrix[i, j] = min(
                    self.distance_matrix[i - 1, j] + self.del_cost,
                    self.distance_matrix[i, j - 1] + self.ins_cost,
                    self.distance_matrix[i - 1][j - 1] + sub_cost)

    def get_min_dist(self):
        return self.distance_matrix[self.rows - 1, self.cols - 1]

    def __calculate_direction(self) -> None:
        for i in range(0, self.rows):
            index = Direction.Up.value - 1
            self.direction_matrix[i, 0, index] = Direction.Up.value

        for j in range(0, self.cols):
            index = Direction.Left.value - 1
            self.direction_matrix[0, j, index] = Direction.Left.value

        for i in range(1, self.rows):
            for j in range(1, self.cols):
                dist = self.distance_matrix[i][j]
                if self.distance_matrix[i - 1, j] + self.del_cost == dist:
                    self.direction_matrix[
                        i, j, Direction.Up.value - 1] = Direction.Up.value
                if self.distance_matrix[i, j - 1] + self.ins_cost == dist:
                    self.direction_matrix[
                        i, j, Direction.Left.value - 1] = Direction.Left.value
                if (self.distance_matrix[i - 1, j - 1] == dist or self
                        .distance_matrix[i - 1, j - 1] + self.sub_cost == dist):
                    self.direction_matrix[i, j, Direction.UpLeft.value - 1] = \
                        Direction.UpLeft.value

    def get_instructions_raw(self):
        result = []
        i = self.rows - 1
        j = self.cols - 1
        while not (i == 0 and j == 0):
            dir_left = self.direction_matrix[i, j, Direction.Left.value - 1]
            dir_up = self.direction_matrix[i, j, Direction.Up.value - 1]
            dir_ul = self.direction_matrix[i, j, Direction.UpLeft.value - 1]
            if dir_left != 0:
                result.append(Direction.get_char(dir_left))
                j -= 1
            elif dir_up != 0:
                result.append(Direction.get_char(dir_up))
                i -= 1
            elif dir_ul != 0:
                result.append(Direction.get_char(dir_ul))
                i -= 1
                j -= 1

        return result

    def get_instructions(self) -> list:
        results = []
        i = self.rows - 1
        j = self.cols - 1
        while not (i == 0 and j == 0):
            dir_left = self.direction_matrix[i, j, Direction.Left.value - 1]
            dir_up = self.direction_matrix[i, j, Direction.Up.value - 1]
            dir_ul = self.direction_matrix[i, j, Direction.UpLeft.value - 1]
            if dir_left != 0:
                results.append(
                    f"{Direction.get_char(dir_left)} : Insert {self.y[j - 1]}")
                j -= 1
            elif dir_up != 0:
                results.append(
                    f"{Direction.get_char(dir_up)} : Delete {self.x[i - 1]}")
                i -= 1
            elif dir_ul != 0:
                results.append(f"{Direction.get_char(dir_ul)} :"
                               f" Replace {self.x[i - 1]} with {self.y[j - 1]}")
                j -= 1
                i -= 1

        return results

    def print_step_by_step(self):
        ins = self.get_instructions_raw()
        i = self.rows - 1
        j = self.cols - 1
        yield self.x
        for ch in ins:
            if ch == '↖':
                self.x = self.x[:i - 1] + self.y[j - 1] + self.x[i:]
                i -= 1
                j -= 1
            elif ch == '←':
                self.x = self.x[:i] + self.y[j - 1] + self.x[i:]
                j -= 1
            else:
                self.x = self.x[:i - 1] + self.x[i:]
                i -= 1
            yield self.x
