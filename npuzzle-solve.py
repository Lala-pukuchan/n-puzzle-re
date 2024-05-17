from Node import Node
import heapq
from solve import Solve
from Goal import Goal


def a_star_search(size, puzzle):
    """
    A*アルゴリズムでパズルを解く
    1. ゴールクラスを作成する。
    2. 初期位置でのNodeを作成して、openリストに入れる。(heapqを使うので、fで常にソートされる)
    3. 空のclosedリストを作成する。
    4. ループに入る。
    5. openリストから先頭のNodeを取り出す。
    6. 取り出したNodeがゴールと合致(h=0)していれば、終了。
    7. 再度同じ場所に戻らないように、現状のNodeをclosedリストに入れる。
    8. 現状のNodeから、子Node群を生成し、既に訪れていない場合は、open/closedリストに入れる。
    9. 5に戻る。
    """
    goal = Goal(size)

    start_node = Node(puzzle, 0, None, goal.goal_puzzle_dic, size)
    open_list = []
    heapq.heappush(open_list, (start_node.f, start_node))
    closed_list = set()

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node.puzzle == goal.goal_puzzle:
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
    #heuristic = 1
    #algo = 1
    #tak = Solve(tak, model.model, model.model_dic, heuristic, greedy=algo == 2, uniform_cost=algo == 3)


if __name__ == "__main__":
    main()
