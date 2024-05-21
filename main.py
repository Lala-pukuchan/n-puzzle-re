import argparse
import random
import os
import sys
from Node import Node
from Goal import Goal
import heapq


def print_result(current_node, total_opened_states, max_states_in_memory):
    """
    結果を表示する
    1. 時間計算量
    2. 空間計算量
    3. 移動回数
    4. 解のシーケンス
    """
    print(f"complexity in time: {total_opened_states}")
    print(f"complexity in size: {max_states_in_memory}")
    print(f"number of moves: {current_node.g}")
    solution_path = []
    while current_node:
        solution_path.append(current_node.puzzle)
        current_node = current_node.parent
    solution_path.reverse()
    for state in solution_path:
        for row in state:
            print(row)
        print()


def generate_random_puzzle(n=3):
    numbers = list(range(n * n))
    random.shuffle(numbers)
    puzzle = []
    for i in range(n):
        puzzle.append(numbers[i * n : (i + 1) * n])
    return puzzle


def generate_random_puzzle_file():
    directory = "puzzles"
    os.makedirs(directory, exist_ok=True)

    max_num = 0
    for file in os.listdir(directory):
        if file.startswith("temp_puzzle_") and file.endswith(".txt"):
            num_part = file[len("temp_puzzle_") : -len(".txt")]
            if num_part.isdigit():
                num = int(num_part)
                if num > max_num:
                    max_num = num

    new_filename = f"temp_puzzle_{max_num + 1}.txt"
    full_path = os.path.join(directory, new_filename)

    puzzle = generate_random_puzzle()
    with open(full_path, "w") as f:
        f.write(f"3\n")
        for row in puzzle:
            f.write(" ".join(map(str, row)) + "\n")
    return full_path


def read_puzzle(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    size = int(lines[0].strip())
    puzzle = []
    for line in lines[1:]:
        puzzle.append(tuple(map(int, line.strip().split())))
    return size, tuple(puzzle)


def uniform_cost_search(puzzle, goal):
    Node.set_comparison_criteria("g")
    start_node = Node(puzzle, 0, None, goal)
    open_list = []
    heapq.heappush(open_list, (start_node.g, start_node))
    open_dict = {start_node.puzzle: start_node.g}
    closed_dict = {}
    total_opened_states = 0
    max_states_in_memory = 0

    while open_list:
        _, current_node = heapq.heappop(open_list)
        total_opened_states += 1

        if current_node.puzzle == goal.goal_puzzle:
            print_result(current_node, total_opened_states, max_states_in_memory)
            return

        open_dict.pop(current_node.puzzle, None)
        closed_dict[current_node.puzzle] = current_node

        for child in current_node.get_children():
            if child.puzzle in closed_dict:
                continue
            if child.puzzle in open_dict:
                if open_dict[child.puzzle] > child.g:
                    open_dict[child.puzzle] = child.g
                    heapq.heappush(open_list, (child.g, child))
            else:
                open_dict[child.puzzle] = child.g
                heapq.heappush(open_list, (child.g, child))

        max_states_in_memory = max(
            max_states_in_memory, len(open_dict) + len(closed_dict)
        )


def greedy_best_first_search(puzzle, goal):
    Node.set_comparison_criteria("h")
    start_node = Node(puzzle, 0, None, goal)
    open_list = []
    heapq.heappush(open_list, (start_node.h, start_node))
    open_dict = {start_node.puzzle: start_node.h}
    closed_dict = {}
    total_opened_states = 0
    max_states_in_memory = 0

    while open_list:
        _, current_node = heapq.heappop(open_list)
        total_opened_states += 1

        if current_node.puzzle == goal.goal_puzzle:
            print_result(current_node, total_opened_states, max_states_in_memory)
            return

        open_dict.pop(current_node.puzzle, None)
        closed_dict[current_node.puzzle] = current_node

        for child in current_node.get_children():
            if child.puzzle in closed_dict:
                continue
            if child.puzzle in open_dict:
                if open_dict[child.puzzle] > child.h:
                    open_dict[child.puzzle] = child.h
                    heapq.heappush(open_list, (child.h, child))
            else:
                open_dict[child.puzzle] = child.h
                heapq.heappush(open_list, (child.h, child))

        max_states_in_memory = max(
            max_states_in_memory, len(open_dict) + len(closed_dict)
        )


def a_star_search(puzzle, goal):
    Node.set_comparison_criteria("f")
    start_node = Node(puzzle, 0, None, goal)
    open_list = []
    heapq.heappush(open_list, start_node)
    open_dict = {}
    open_dict[start_node.puzzle] = start_node.f
    closed_dict = {}
    total_opened_states = 0
    max_states_in_memory = 0

    while open_list:
        current_node = heapq.heappop(open_list)
        total_opened_states += 1

        if current_node.puzzle == goal.goal_puzzle:
            print_result(current_node, total_opened_states, max_states_in_memory)
            return

        open_dict.pop(current_node.puzzle, None)
        closed_dict[current_node.puzzle] = current_node

        for child in current_node.get_children():
            if child.puzzle in closed_dict:
                continue
            if child.puzzle in open_dict:
                if open_dict[child.puzzle] > child.f:
                    heapq.heappush(open_list, child)
                    open_dict[child.puzzle] = child.f
            else:
                heapq.heappush(open_list, child)
                open_dict[child.puzzle] = child.f

        max_states_in_memory = max(
            max_states_in_memory, len(open_dict) + len(closed_dict)
        )


def check_solvable(puzzle, goal):
    """
    下記の二つの偶奇が一致するかで、パズルが解けるかどうかを判定する
    ①パズル内の各マス目位置を交換する回数の偶奇
    ②空白マスの位置とゴールの空白マスの位置のマンハッタン距離の偶奇
    """
    n = Node(puzzle, 0, None, goal)
        
    diff_all = 0
    puzzle_list = []
    goal_list = []

    for line in puzzle:
        puzzle_list += line
    for line in goal.goal_puzzle:
        goal_list += line

    for i in range(len(puzzle_list)):
        for j in range(i, len(puzzle_list)):
            if goal_list.index(puzzle_list[i]) > goal_list.index(puzzle_list[j]):
                puzzle_list[j], puzzle_list[i] = puzzle_list[i], puzzle_list[j]
                diff_all += 1

    empty_row, empty_col = n.find_empty_space(puzzle)
    diff_empty = abs(empty_row - goal.goal_empty_row) + abs(empty_col - goal.goal_empty_col)

    if diff_all % 2 == diff_empty % 2:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description="Solve N-Puzzle problem.")

    # Question 1
    print("\033[95m" + 
          "Do you want to use an existing map file or a randomly generated map?\n" +
          "Please enter\n'\033[1m\033[95m1\033[0m\033[95m': for file\n'\033[1m\033[95m2\033[0m\033[95m': for random generate" + 
          "\033[0m")
    choice = input().strip().lower()

    if choice == "1":
        print("\033[95m" + "Please enter the file name:" + "\033[0m")
        file_path = input().strip()
        if not os.path.isfile(file_path):
            print("Error: Invalid file name.")
            return
    elif choice == "2":
        print("\033[95m" + "\033[1mRandom choice\033[0m" + "\033[0m")
        file_path = generate_random_puzzle_file()
    else:
        print(
            "Error: Invalid choice. Please enter '\033[1m\033[95mf\033[0m\033[95m' or '\033[1m\033[95mr\033[0m\033[95m'."
        )
        return

    size, puzzle = read_puzzle(file_path)

    goal = Goal(size)

    if not check_solvable(puzzle, goal):
        print("Error: Invalid puzzle. Please enter a solvable puzzle.")
        return

    # Question 2
    print(
        "\033[93m"
        + "\nWhich algorithm would you like to use?\n"
        + "'\033[1m\033[93m1\033[0m\033[93m': A* Search\n'\033[1m\033[93m2\033[0m\033[93m': Greedy Best-First Search\n'\033[1m\033[93m3\033[0m\033[93m': Uniform Cost Search\n'\033[1m\033[93m4\033[0m\033[93m': Random"
        + "\033[0m"
    )
    algorithm_choice = input().strip().lower()

    if algorithm_choice == "4":
        algorithm_choice = random.choice(["1", "2", "3"])

    if algorithm_choice == "1":
        print("\033[93m" + "\033[1mA* Search\033[0m" + "\033[0m")
        Node.set_comparison_criteria("f")
    elif algorithm_choice == "2":
        print("\033[93m" + "\033[1mGreedy Search\033[0m" + "\033[0m")
        Node.set_comparison_criteria("h")
    elif algorithm_choice == "3":
        print("\033[93m" + "\033[1mUniform Cost Search\033[0m" + "\033[0m")
        Node.set_comparison_criteria("g")
    else:
        print("Error: Invalid algorithm choice.")
        return

    if algorithm_choice in ["1", "2"]:
        # Question 3
        print(
            "\033[96m"
            + "\nWhich heuristic function would you like to use?\n"
            + "'\033[1m\033[96m1\033[0m\033[96m': Manhattan\n'\033[1m\033[96m2\033[0m\033[96m': Hamming\n'\033[1m\033[96m3\033[0m\033[96m': Linear Conflict\n'\033[1m\033[96m4\033[0m\033[96m': Random"
            + "\033[0m"
        )
        heuristic_choice = input().strip().lower()

        if heuristic_choice == "4":
            heuristic_choice = random.choice(["1", "2", "3"])

        if heuristic_choice == "1":
            print("\033[96m" + "\033[1mManhattan\033[0m" + "\033[0m")
            Node.set_heuristic_function("manhattan")
        elif heuristic_choice == "2":
            print("\033[96m" + "\033[1mHamming\033[0m" + "\033[0m")
            Node.set_heuristic_function("hamming")
        elif heuristic_choice == "3":
            print("\033[96m" + "\033[1mLinear_conflict\033[0m" + "\033[0m")
            Node.set_heuristic_function("linear_conflict")
        else:
            print("Error: Invalid heuristic choice.")
            return

    if algorithm_choice == "1":
        a_star_search(puzzle, goal)
    elif algorithm_choice == "2":
        greedy_best_first_search(puzzle, goal)
    elif algorithm_choice == "3":
        uniform_cost_search(puzzle, goal)
    else:
        print("Error: Invalid algorithm choice.")
        return


if __name__ == "__main__":
    main()
