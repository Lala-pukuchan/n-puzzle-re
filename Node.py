class Node:
    def __init__(self, puzzle, depth, parent, goal_puzzle):
        """
        Nodeの初期化
        Node: ある時点でのパズルの状態
            puzzle: パズルの状態
            empty_space: 空きスペースの座標
            depth: ノードの深さ
            parent: 親ノード
            heuristic: ヒューリスティック値
        """
        self.puzzle = puzzle
        self.empty_space = self.find_empty_space(puzzle)
        print(self.empty_space)
        self.g = depth
        self.h = self.calc_heuristic(goal_puzzle)
        self.parent = parent
        self.goal_puzzle = goal_puzzle

    def find_empty_space(self, puzzle):
        """
        パズルを動かす起点となる空白マス(0)を探す
        """
        for i, row in enumerate(puzzle):
            for j, cell in enumerate(row):
                if cell == 0:
                    return (i, j)

    def calc_heuristic(self, goal_puzzle):
        """
        ヒューリスティック値（ゴールと現在のパズルの状態の差）を計算する
        1. 現状のパズルでループを回す
        2. ゴールのパズルと比較して、異なるセルの数をカウントする
        """
        heuristic = 0
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] != goal_puzzle[i][j]:
                    heuristic += 1
        return heuristic
