class Node:
    heuristic_function = "manhattan"

    def __init__(self, puzzle, depth, parent, goal):
        """
        Nodeの初期化
        Node: ある時点でのパズルの状態
            goal = ゴール状態
            size = パズルのサイズ
            goal_puzzle_dic = ゴールのパズルの辞書
            puzzle = パズルの状態
            empty_space = 空きスペースの座標
            g = 現状のコスト(手数)
            h = 推定コスト(ゴールと合致していないセルの数)
            f = g + h
            parent = 親Node
        """
        self.goal = goal
        self.size = goal.size
        self.goal_puzzle_dic = goal.goal_puzzle_dic
        self.puzzle = puzzle
        self.empty_space = self.find_empty_space(self.puzzle)
        self.g = depth
        if Node.heuristic_function == "hamming":
            self.h = self.hamming_heuristic()
        elif Node.heuristic_function == "manhattan":
            self.h = self.manhattan_heuristic()
        elif Node.heuristic_function == "linear_conflict":
            self.h = self.linear_conflict_heuristic()
        self.f = self.g + self.h
        self.parent = parent

    @staticmethod
    def set_comparison_criteria(criteria):
        """
        nodeの比較基準を設定する
        """
        Node.comparison_criteria = criteria

    def __lt__(self, other):
        """
        heapqでNodeをソートするための比較関数
        f値が同じ場合は、h値が小さい方を優先する
        f値が異なる場合は、f値が小さい方を優先する
        """
        if Node.comparison_criteria == 'g':
            return self.g < other.g
        elif Node.comparison_criteria == 'h':
            return self.h < other.h
        else:
            if self.f == other.f:
                return self.h < other.h
            else:
                return self.f < other.f
            
    @staticmethod
    def set_heuristic_function(function):
        """
        ヒューリスティック関数を設定する
        """
        Node.heuristic_function = function

    def __hash__(self):
        """
        パズルをハッシュ化する
        """
        return hash(self.puzzle)

    def __eq__(self, other):
        """
        パズルの状態が等しいかどうかを判定する
        """
        return self.puzzle == other.puzzle

    def find_empty_space(self, puzzle):
        """
        パズルを動かす起点となる空白マス(0)を探す
        """
        for i, row in enumerate(puzzle):
            for j, cell in enumerate(row):
                if cell == 0:
                    return (i, j)

    def is_valid_move(self, empty_space, direction):
        """
        空白マスが動かせる方向かどうかを判定する
        """
        i, j = empty_space
        di, dj = direction
        return 0 <= i + di < len(self.puzzle) and 0 <= j + dj < len(self.puzzle[0])

    def get_child_puzzle(self, puzzle, empty_space, direction):
        """
        空白マスを動かした後のパズルを生成する
        """
        i, j = empty_space
        di, dj = direction
        child_puzzle = [list(row) for row in puzzle]
        child_puzzle[i][j], child_puzzle[i + di][j + dj] = (
            child_puzzle[i + di][j + dj],
            child_puzzle[i][j],
        )
        return tuple(tuple(row) for row in child_puzzle)

    def get_children(self):
        """
        現在のNodeから、動かせる方向の子Nodeを生成する
        1. 子Nodeのリストを初期化する
        2. ４方向でループを回す
        3. その方向に動かせるかどうかを判定する
        4. 動かせる場合は、その方向に動かしたパズルを生成し、子Nodeを生成してリストに追加する
        5. 子Nodeのリストを返す
        """
        children = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for direction in directions:
            if self.is_valid_move(self.empty_space, direction):
                child_puzzle = self.get_child_puzzle(
                    self.puzzle, self.empty_space, direction
                )
                child_node = Node(child_puzzle, self.g + 1, self, self.goal)
                children.append(child_node)
        return children

    def hamming_heuristic(self):
        """
        ヒューリスティック値（ゴールと現在のパズルの状態の差）を計算する
        1. 現状のパズルでループを回す
        2. ゴールのパズルと比較して、異なるセルの数をカウントする
        """
        heuristic = 0
        size = self.size
        for i in range(size):
            for j in range(size):
                if (i, j) != self.goal_puzzle_dic[self.puzzle[i][j]]:
                    heuristic += 1
        return heuristic

    def manhattan_heuristic(self):
        """
        マンハッタン距離を計算する
        1. 現状のパズルでループを回す
        2. 各セルの現在の位置とゴールの位置のマンハッタン距離を計算する
        """
        heuristic = 0
        size = self.size
        for i in range(size):
            for j in range(size):
                current_value = self.puzzle[i][j]
                if current_value != 0:
                    goal_i, goal_j = self.goal_puzzle_dic[current_value]
                    heuristic += abs(goal_i - i) + abs(goal_j - j)
        return heuristic

    def linear_conflict_heuristic(self):
        """
        リニアコンフリクトを考慮したヒューリスティック関数
        リニアコンフリクト: ２つのタイルが同じ行または列にあり、正しい位置に並んでいない場合
        1. マンハッタン距離を計算する
        2. リニアコンフリクトを考慮して、マンハッタン距離を修正する
        """
        heuristic = self.manhattan_heuristic()
        size = self.size
        for i in range(size):
            row = self.puzzle[i]
            for j in range(size):
                if row[j] != 0:
                    goal_i, goal_j = self.goal_puzzle_dic[row[j]]
                    if goal_i == i:
                        for k in range(j + 1, size):
                            if row[k] != 0:
                                goal_k, _ = self.goal_puzzle_dic[row[k]]
                                if goal_k == i and goal_j > goal_k:
                                    heuristic += 2
                    if goal_j == j:
                        for k in range(i + 1, size):
                            if self.puzzle[k][j] != 0:
                                goal_k, _ = self.goal_puzzle_dic[self.puzzle[k][j]]
                                if goal_k == j and goal_i > goal_k:
                                    heuristic += 2
        return heuristic