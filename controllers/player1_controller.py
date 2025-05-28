# This is the Player 1 AI controller file.
# Contestants should implement their snake AI logic within this file.
# Your code will determine Player 1's next move based on the provided game state.
#
# You will need to implement two functions:
# 1. `get_next_move(board_state_data, player_state_data, opponent_state_data)`:
#    This function should return the next direction for the snake ("up", "down", "left", or "right").
# 2. `set_player_name()`:
#    This function should return a string representing the name of your AI player.
#
# For more detailed information on the expected input and output formats,
# please refer to the documentation at `docs/controller_api.md`.
# Happy Coding!

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
    head_x = player_state["head_position"]["x"]
    head_y = player_state["head_position"]["y"]
    direction = player_state["direction"]
    body = player_state["body"]

    def is_safe_move(x, y):
        """Checks if a move to (x, y) is safe (not out of bounds or self-collision)."""
        if x < 0 or x >= board_state["width"] or y < 0 or y >= board_state["height"]:
            return False
        for obstacle in board_state["obstacle_locations"]:
            # print(f"Player 1: Checking obstacle at ({obstacle[0]}, {obstacle[1]})")
            # print(f"Player 1: Checking position ({x}, {y})")
            obs_x, obs_y = obstacle
            if obs_x * GRID_SIZE == x and obs_y * GRID_SIZE == y:
                print(f"Player 1: Obstacle at ({x}, {y})")
                return False
            # print(obstacle)
        for segment in body:
            if segment["x"] == x and segment["y"] == y:
                return False
        for segment in opponent_state["body"]:
            if segment["x"] == x and segment["y"] == y:
                return False
        return True

    # List possible moves with their new positions
    moves = [
        ("right", (head_x + GRID_SIZE, head_y)),
        ("down", (head_x, head_y + GRID_SIZE)),
        ("up", (head_x, head_y - GRID_SIZE)),
        ("left", (head_x - GRID_SIZE, head_y)),
    ]

    # Avoid reversing direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    
    food_list = board_state.get("food_locations", [])

    # Sort moves by distance to food
    moves_sorted = sorted(
        moves,
        key=lambda m: get_distance_to_food(m[1][0], m[1][1], food_list)
    )
    
    print(moves_sorted)

    for move, (new_x, new_y) in moves_sorted:
        print(f"Player 1: Checking move {move} to ({new_x}, {new_y})")
        print(is_safe_move(new_x, new_y))
        if move != opposites[direction] and is_safe_move(new_x, new_y):
            print(f"Player 1: {move} is safe")
            return move

    # If no safe move, keep current direction
    return direction

def set_player_name():
    """
    Sets the player's name.

    Returns:
        str: The name of the player as a string.
    """
    return "Joshua"

def get_distance_to_food(x, y, food_list):
    if not food_list:
        return float('inf')
    return min(math.hypot(food[0] - x, food[1] - y) for food in food_list)