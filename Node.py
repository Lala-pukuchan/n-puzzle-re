class Node:
    def __init__(self, puzzle, depth, parent, goal_puzzle):
        """
        Nodeの初期化
        Node: ある時点でのパズルの状態
            puzzle: パズルの状態
            empty_space: 空きスペースの座標
            g: 現状のコスト(手数)
            h: 推定コスト(ゴールと合致していないセルの数)
            f: f = g + h
            parent: 親Node
            goal_puzzle: ゴールのパズルの状態
        """
        self.puzzle = puzzle
        self.empty_space = self.find_empty_space(puzzle)
        self.g = depth
        self.h = self.calculate_heuristic(goal_puzzle)
        self.f = self.g + self.h
        self.parent = parent
        self.goal_puzzle = goal_puzzle

    def __lt__(self, other):
        """
        heapqでNodeをソートするための比較関数
        """
        return self.f < other.f

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
                child_node = Node(child_puzzle, self.g + 1, self, self.goal_puzzle)
                children.append(child_node)
        return children

    def calculate_heuristic(self, goal_puzzle):
        """
        ヒューリスティック値（ゴールと現在のパズルの状態の差）を計算する
        1. 現状のパズルでループを回す
        2. ゴールのパズルと比較して、異なるセルの数をカウントする
        """
        heuristic = 0
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] != 0:
                    goal_i, goal_j = divmod(goal_puzzle[i][j] - 1, len(self.puzzle))
                    heuristic += abs(i - goal_i) + abs(j - goal_j)
        return heuristic
