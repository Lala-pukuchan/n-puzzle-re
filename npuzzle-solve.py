from Node import Node
import heapq
from Goal import Goal


def a_star_search(puzzle, goal):
    """
    A*アルゴリズムでパズルを解く
    1. 初期Node作成
    2. f値で常にソートされるheapqを使い、openリストを作成する。
    3. 空のclosedリストを作成する。
    4. ループに入る。
    4. openリストから先頭のNodeを取り出す。
    5. 取り出したNodeがゴールと合致(h=0)していれば、終了。
    6. 再度同じ場所に戻らないように、現状のNodeをclosedリストに入れる。
    7. 現状のNodeから、子Node群を生成し、既に訪れていない場合は、open/closedリストに入れる。
    8. 5に戻る。
    """
    start_node = Node(puzzle, 0, None, goal)
    open_list = []
    heapq.heappush(open_list, start_node)
    open_dict = {}
    open_dict[start_node.puzzle] = start_node.f
    closed_dict = {}

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.puzzle == goal.goal_puzzle:
            print("Goal!")
            print(current_node.g)
            for row in current_node.puzzle:
                print(row)
            return

        open_dict.pop(current_node.puzzle, None)
        closed_dict[current_node.puzzle] = current_node

        for child in current_node.get_children():
            if child.puzzle in closed_dict:
                continue
            if child.puzzle in open_dict:
                if open_dict[child.puzzle] < child.f:
                    heapq.heappush(open_list, child)
                    open_dict[child.puzzle] = child.f
            else:
                heapq.heappush(open_list, child)
                open_dict[child.puzzle] = child.f


def read_puzzle(file_path):
    """
    ファイルを読み込み、パズルをtupleに変換する
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    size = int(lines[0].strip())
    puzzle = []
    for line in lines[1:]:
        puzzle.append(tuple(map(int, line.strip().split())))

    return size, tuple(puzzle)


def main():
    """
    ファイルを読み込んで、A*アルゴリズムでパズルを解く
    """
    file_path = "puzzle_4.txt"
    size, puzzle = read_puzzle(file_path)
    a_star_search(puzzle, Goal(size))


if __name__ == "__main__":
    main()
