import numpy as np
import random

random.seed(160716)

def create_board(size):
    return np.zeros((size, size), dtype=int)

def random_start(board, size):
    position_one = [random.randint(0, size-1), random.randint(0, size-1)]
    position_two = [random.randint(0, size-1), random.randint(0, size-1)]

    if position_one == position_two:
        position_two[0], position_two[1] = position_two[1], position_two[0]

    board[position_two[0], position_two[1]] = 2
    board[position_one[0], position_one[1]] = 2

    return board

def merge_elements_and_score(line, score):
    new_line = np.zeros_like(line)
    index = 0

    for i in range(len(line)):
        if line[i] != 0:
            if index > 0 and new_line[index - 1] == line[i]:
                # Merge tiles
                new_line[index - 1] *= 2
                # Update score
                score += new_line[index - 1]
            else:
                new_line[index] = line[i]
                index += 1

    return new_line, score

def random_add_tile(board):
    tile_value = 2 if random.random() < 0.9 else 4
    available_positions = np.argwhere(board == 0)

    if len(available_positions) > 0:
        random_position = random.choice(available_positions)
        board[random_position[0], random_position[1]] = tile_value

def swipe_and_score(board, direction, score):
    size = len(board)

    if direction == "down":
        for col in range(size):
            column = board[:, col]
            new_column, score = merge_elements_and_score(column, score)
            board[:, col] = np.concatenate((np.zeros(size - len(new_column), dtype=int), new_column))

    elif direction == "up":
        for col in range(size):
            column = board[:, col]
            reversed_column = column[::-1]
            new_column, score = merge_elements_and_score(reversed_column, score)
            board[:, col] = np.concatenate((new_column[::-1], np.zeros(size - len(new_column), dtype=int)))

    elif direction == "left":
        for row in range(size):
            current_row = board[row, :]
            new_row, score = merge_elements_and_score(current_row, score)
            board[row, :] = np.concatenate((new_row, np.zeros(size - len(new_row), dtype=int)))

    elif direction == "right":
        for row in range(size):
            current_row = board[row, ::-1]
            new_row, score = merge_elements_and_score(current_row, score)
            board[row, :] = np.concatenate((np.zeros(size - len(new_row), dtype=int), new_row[::-1]))

    random_add_tile(board)

    return score

# Example usage
board = create_board(4)
board = random_start(board, len(board))
score = 0

print("Original Board:")
print(board)

score = swipe_and_score(board, "down", score)
print("\nBoard After Swipe Down:")
print(board)
print("Score:", score)

score = swipe_and_score(board, "up", score)
print("\nBoard After Swipe Up:")
print(board)
print("Score:", score)

score = swipe_and_score(board, "left", score)
print("\nBoard After Swipe Left:")
print(board)
print("Score:", score)

score = swipe_and_score(board, "right", score)
print("\nBoard After Swipe Right:")
print(board)
print("Score:", score)
