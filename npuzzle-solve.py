from Node import Node
import heapq


def get_goal_puzzle(size):
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


def a_star_search(size, puzzle):
    """
    A*アルゴリズムでパズルを解く
    1. ゴールとなるパズルを生成する。
    2. 初期位置でのNodeを作成して、openリストに入れる。(heapqを使うので、fで常にソートされる)
    3. 空のclosedリストを作成する。
    4. ループに入る。
    5. openリストから先頭のNodeを取り出す。
    6. 取り出したNodeがゴールと合致(h=0)していれば、終了。
    7. 再度同じ場所に戻らないように、現状のNodeをclosedリストに入れる。
    8. 現状のNodeから、子Node群を生成し、既に訪れていない場合は、open/closedリストに入れる。
    9. 5に戻る。
    """
    goal_puzzle = get_goal_puzzle(size)
    goal_puzzle_dic = {}
    for i in range(size):
        for j in range(size):
            goal_puzzle_dic[goal_puzzle[i][j]] = (i, j)
    start_node = Node(puzzle, 0, None, goal_puzzle_dic, size)
    open_list = []
    heapq.heappush(open_list, (start_node.f, start_node))
    closed_list = set()

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node.puzzle == goal_puzzle:
            print("Goal!")
            print(current_node.g)
            for row in current_node.puzzle:
                print(row)
            return

        closed_list.add(hash(current_node.puzzle))

        for child in current_node.get_children():
            if hash(child.puzzle) not in closed_list:
                heapq.heappush(open_list, (child.f, child))
                closed_list.add(hash(child.puzzle))


def read_puzzle(file_path):
    """
    ファイルを読み込み、パズルを二次元配列に変換する
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    size = int(lines[0].strip())
    puzzle = []
    for line in lines[1:]:
        puzzle.append(tuple(map(int, line.strip().split())))

    return size, tuple(puzzle)


def read_puzzle_from_file(file_path):
    """
    ファイルを読み込み、パズルを二次元配列に変換する
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    dim = int(lines[0].strip())
    puzzle = []
    for line in lines[1:]:
        puzzle.append([int(x) for x in line.split()])

    return dim, puzzle


def create_puzzle_from_file(file_path):
    dim, puzzle = read_puzzle_from_file(file_path)

    flat_puzzle = [item for sublist in puzzle for item in sublist]

    shuffled_puzzle = []
    for i in range(dim):
        shuffled_puzzle.append(flat_puzzle[i * dim : (i + 1) * dim])

    return shuffled_puzzle


def main():
    file_path = "puzzle_4.txt"
    size, puzzle = read_puzzle(file_path)
    a_star_search(size, puzzle)


if __name__ == "__main__":
    main()
