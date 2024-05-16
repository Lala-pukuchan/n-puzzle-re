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
        self.h = self.calc_heuristic(goal_puzzle)
        self.f = self.g + self.h
        self.parent = parent
        self.goal_puzzle = goal_puzzle

    def __lt__(self, other):
        """
        heapqでNodeをソートするための比較関数
        """
        return self.f < other.f

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
        child_puzzle = [row[:] for row in puzzle]
        child_puzzle[i][j], child_puzzle[i + di][j + dj] = (
            child_puzzle[i + di][j + dj],
            child_puzzle[i][j],
        )
        return child_puzzle

    def get_children(self, closed_list):
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
                print("valid move")
                for row in self.puzzle:
                    print(row)
                print(direction)
                child_puzzle = self.get_child_puzzle(
                    self.puzzle, self.empty_space, direction
                )
                already_visited = False
                for node in closed_list:
                    if node.puzzle == child_puzzle:
                        print("closed")
                        already_visited = True
                        break
                if not already_visited:
                    child_node = Node(child_puzzle, self.g + 1, self, self.goal_puzzle)
                    children.append(child_node)
        return children

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
