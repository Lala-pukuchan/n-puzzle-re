from Node import Node


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

    return puzzle


def a_star_search(size, puzzle):
    """
    A*アルゴリズムでパズルを解く
    1. ゴールとなるパズルを生成する。
    2. 初期位置でのノードをスタートノードとする。
    3.
    """
    goal_puzzle = get_goal_puzzle(size)
    start_node = Node(puzzle, 0, None, goal_puzzle)
    print(start_node.puzzle)


def read_puzzle(file_path):
    """
    ファイルを読み込み、パズルを二次元配列に変換する
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    size = int(lines[0].strip())
    puzzle = []

    for line in lines[1:]:
        row = line.strip().split()
        row = [int(cell) for cell in row]
        puzzle.append(row)

    return size, puzzle


def main():
    file_path = "puzzle.txt"
    size, puzzle = read_puzzle(file_path)
    a_star_search(size, puzzle)


if __name__ == "__main__":
    main()
