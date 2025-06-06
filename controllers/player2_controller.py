# This is the Player 2 AI controller file.
# You can implement your snake AI logic here to test playing against an opponent.
# This is useful for developing and debugging your Player 1 AI.
#
# Similar to Player 1, you will need to implement:
# 1. `get_next_move(board_state_data, player_state_data, opponent_state_data)`
# 2. `set_player_name()`
#
# Refer to `docs/controller_api.md` for more details.
# Good Luck!

# controllers/example_controller.py

from config import config
import math

GRID_SIZE = config.GRID_SIZE

def get_next_move(board_state, player_state, opponent_state):
    """
    A very basic snake controller. It always tries to move right, unless
    that's not a safe move, in which case it tries down, then up, then left.
    If none of those are safe, it returns the current direction.

    This example uses the game's GRID_SIZE for all moves and checks, ensuring
    compatibility regardless of the configured grid.

    Args:
        board_state (dict): Information about the game board.
        player_state (dict): Information about the current player's snake.
        opponent_state (dict): Information about the opponent's snake.

    Returns:
        str: The next direction ("left", "right", "up", "down").
    """
     
    head_row = player_state["head_position"]["row"]
    head_col = player_state["head_position"]["col"]
    direction = player_state["direction"]
    body = player_state["body"]

    def is_safe_move(row, col):
        if row < 0 or row >= board_state["rows"] or col < 0 or col >= board_state["cols"]:
            return False
        for obstacle in board_state["obstacle_locations"]:
            obs_row, obs_col = obstacle
            if obs_row == row and obs_col == col:
                return False
        for segment in body[1:]:
            if segment["row"] == row and segment["col"] == col:
                return False
        for segment in opponent_state["body"]:
            if segment["row"] == row and segment["col"] == col:
                return False
        return True

    moves = [
        ("up", (head_row - 1, head_col)),
        ("down", (head_row + 1, head_col)),
        ("left", (head_row, head_col - 1)),
        ("right", (head_row, head_col + 1)),
    ]

    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    food_list = board_state.get("food_locations", [])

    moves_sorted = sorted(
        moves,
        key=lambda m: get_distance_to_food(m[1][0], m[1][1], food_list)
    )

    for move, (new_row, new_col) in moves_sorted:
        if move != opposites[direction] and is_safe_move(new_row, new_col):
            return move

    return direction

def get_distance_to_food(row, col, food_list):
    if not food_list:
        return float('inf')
    return min(math.hypot(food[0] - row, food[1] - col) for food in food_list)

def set_player_name():
    """
    Sets the player's name.

    Returns:
        str: The name of the player as a string.
    """
    return "Opponent"