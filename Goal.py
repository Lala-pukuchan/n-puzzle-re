class Goal:
    def __init__(self, size):
        """
        ゴールとなるパズルを生成する
        goal_puzzle: ゴールとなるパズル
        goal_puzzle_dic: ゴールとなるパズルの辞書形式（キー: マス目の数字, 値: マス目の座標）
        """
        self.size = size
        self.goal_puzzle = self.get_goal_puzzle(size)
        self.goal_puzzle_dic = self.get_puzzle_dic(self.goal_puzzle)

    def get_goal_puzzle(self, size):
        """
        ゴールとなるパズルを生成する
        1. 左上から、螺旋状に、マス目を埋めていく。
        2. 一番大きい数のあるマスを0に変換する。
        """
        puzzle = [[0] * size for _ in range(size)]
        num = 1
        left, right, top, bottom = 0, size - 1, 0, size - 1

        while left <= right and top <= bottom:
            for j in range(left, right + 1):
                puzzle[top][j] = num
                num += 1
            top += 1

            for i in range(top, bottom + 1):
                puzzle[i][right] = num
                num += 1
            right -= 1

            if top <= bottom:
                for j in range(right, left - 1, -1):
                    puzzle[bottom][j] = num
                    num += 1
                bottom -= 1

            if left <= right:
                for i in range(bottom, top - 1, -1):
                    puzzle[i][left] = num
                    num += 1
                left += 1

        for i in range(size):
            for j in range(size):
                if puzzle[i][j] == size**2:
                    puzzle[i][j] = 0

        return tuple(tuple(row) for row in puzzle)

    def get_puzzle_dic(self, puzzle):
        goal_puzzle_dic = {}
        for i in range(self.size):
            for j in range(self.size):
                goal_puzzle_dic[puzzle[i][j]] = (i, j)
        return goal_puzzle_dic
