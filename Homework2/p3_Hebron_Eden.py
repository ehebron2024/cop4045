"""
Simplified Social Network data structure.

The social network is represented as a dictionary:
    {
        username: (full_name, [friend_username1, friend_username2, ...]),
        ...
    }

This module provides functions to add users, add mutual friend links,
find friends up to a given link distance, and save/load the network
to and from a CSV file.
"""

import csv
from typing import Dict, List, Tuple


# Type alias for readability
SocialNetwork = Dict[str, Tuple[str, List[str]]]


def add_user(sn: SocialNetwork, username: str, fullname: str) -> bool:
    """
    Add a new user to the social network.

    Args:
        sn: The social network dictionary.
        username: The unique username of the new user.
        fullname: The full name of the new user.

    Returns:
        True if the user was added successfully.
        False if a user with that username already exists.

    Raises:
        TypeError: If sn is not a dictionary or username/fullname are not strings.
    """
    try:
        if not isinstance(sn, dict):
            raise TypeError("sn must be a dictionary")
        if not isinstance(username, str) or not isinstance(fullname, str):
            raise TypeError("username and fullname must be strings")

        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as e:
        print(f"Error: could not add user '{username}': {e}")
        raise


def add_friend(sn: SocialNetwork, user1: str, user2: str) -> bool:
    """
    Add a mutual friend link between two users in the social network.

    Args:
        sn: The social network dictionary.
        user1: Username of the first user.
        user2: Username of the second user.

    Returns:
        True if the friend link was added successfully.
        False if either username is not found in sn, or if user1 == user2.

    Raises:
        TypeError: If sn is not a dictionary or user1/user2 are not strings.
    """
    try:
        if not isinstance(sn, dict):
            raise TypeError("sn must be a dictionary")
        if not isinstance(user1, str) or not isinstance(user2, str):
            raise TypeError("user1 and user2 must be strings")

        if user1 == user2:
            return False

        if user1 not in sn or user2 not in sn:
            return False

        name1, friends1 = sn[user1]
        name2, friends2 = sn[user2]

        if user2 not in friends1:
            friends1.append(user2)
        if user1 not in friends2:
            friends2.append(user1)

        return True

    except Exception as e:
        print(f"Error: could not add friend link between '{user1}' and '{user2}': {e}")
        raise


def get_friends(sn: SocialNetwork, user1: str, distance: int) -> List[str]:
    """
    Get all friends of a user up to a given link distance (breadth-first search).

    Args:
        sn: The social network dictionary.
        user1: The username to start from.
        distance: A positive integer indicating the maximum link distance.

    Returns:
        A list of usernames reachable from user1 within the given distance
        (excluding user1 itself). Returns an empty list if user1 is not in
        sn, if distance is not a positive integer, or if there are no
        friends to return.

    Raises:
        TypeError: If sn is not a dictionary or user1 is not a string.
    """
    try:
        if not isinstance(sn, dict):
            raise TypeError("sn must be a dictionary")
        if not isinstance(user1, str):
            raise TypeError("user1 must be a string")

        if user1 not in sn or not isinstance(distance, int) or distance <= 0:
            return []

        visited = {user1}
        result: List[str] = []
        current_level = [user1]

        for _ in range(distance):
            next_level = []
            for user in current_level:
                _, friends = sn.get(user, (None, []))
                for friend in friends:
                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_level.append(friend)
            current_level = next_level
            if not current_level:
                break

        return result

    except Exception as e:
        print(f"Error: could not get friends for '{user1}': {e}")
        raise


def save_network(filename: str, sn: SocialNetwork) -> None:
    """
    Save a social network dictionary to a CSV file.

    Each row of the CSV file has the format:
        username, full_name, friend1;friend2;...

    Args:
        filename: The path of the CSV file to write to.
        sn: The social network dictionary to save.

    Raises:
        TypeError: If sn is not a dictionary.
        FileNotFoundError: If the directory in filename does not exist.
        OSError: For other I/O related errors.
    """
    try:
        if not isinstance(sn, dict):
            raise TypeError("sn must be a dictionary")

        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            for username, (fullname, friends) in sn.items():
                friends_str = ";".join(friends)
                writer.writerow([username, fullname, friends_str])

    except FileNotFoundError as e:
        print(f"Error: could not save network — directory not found for '{filename}': {e}")
        raise
    except OSError as e:
        print(f"Error: could not save network to '{filename}': {e}")
        raise
    except Exception as e:
        print(f"Error: unexpected error while saving network to '{filename}': {e}")
        raise


def load_network(filename: str) -> SocialNetwork:
    """
    Load a social network dictionary from a CSV file saved by save_network().

    Args:
        filename: The path of the CSV file to read from.

    Returns:
        The reconstructed social network dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: For other I/O related errors.
        ValueError: If a row in the file is malformed.
    """
    sn: SocialNetwork = {}
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) != 3:
                    raise ValueError(f"Malformed row in '{filename}': {row}")
                username, fullname, friends_str = row
                friends = friends_str.split(";") if friends_str else []
                sn[username] = (fullname, friends)

        return sn

    except FileNotFoundError as e:
        print(f"Error: could not load network — file not found: '{filename}': {e}")
        raise
    except ValueError as e:
        print(f"Error: could not load network — malformed data: {e}")
        raise
    except OSError as e:
        print(f"Error: could not load network from '{filename}': {e}")
        raise
    except Exception as e:
        print(f"Error: unexpected error while loading network from '{filename}': {e}")
        raise


def main() -> None:
    """
    Test all the social network functions defined in this module.
    """
    sn: SocialNetwork = {}
    print("fau id: Ehebron2024")
    print("Testing add_user")
    print(add_user(sn, "alice", "Alice Smith"))   # True
    print(add_user(sn, "maria", "Maria Cortez"))  # True
    print(add_user(sn, "joe", "Joseph Adams"))    # True
    print(add_user(sn, "eve", "Evelyn Cooper"))   # True
    print(add_user(sn, "david", "David Benson"))  # True
    print(add_user(sn, "alice", "Alice Again"))   # False (already exists)

    print("\nTesting add_friend")
    print(add_friend(sn, "alice", "maria"))  # True
    print(add_friend(sn, "maria", "joe"))    # True
    print(add_friend(sn, "maria", "david"))  # True
    print(add_friend(sn, "joe", "eve"))      # True
    print(add_friend(sn, "alice", "nobody"))  # False (nobody doesn't exist)
    print(add_friend(sn, "alice", "alice"))   # False (same user)

    print("\nCurrent network:")
    for username, (fullname, friends) in sn.items():
        print(f"  {username}: {fullname}, friends={friends}")

    print("\nTesting get_friends")
    print(get_friends(sn, "alice", 1))  # ['maria']
    print(get_friends(sn, "alice", 2))  # ['maria', 'joe', 'david']
    print(get_friends(sn, "alice", 3))  # ['maria', 'joe', 'david', 'eve']
    print(get_friends(sn, "eve", 5))    # ['joe', 'maria', 'alice', 'david']
    print(get_friends(sn, "ghost", 2))  # [] (user doesn't exist)
    print(get_friends(sn, "alice", 0))  # [] (invalid distance)

    print("\n=== Testing save_network / load_network ===")
    filename = "social_network.csv"
    try:
        save_network(filename, sn)
        print(f"Network saved to '{filename}'.")

        loaded_sn = load_network(filename)
        print("Network loaded successfully:")
        for username, (fullname, friends) in loaded_sn.items():
            print(f"  {username}: {fullname}, friends={friends}")

        # Verify the loaded network matches the original
        assert loaded_sn == sn, "Loaded network does not match saved network!"
        print("Verification passed: loaded network matches original.")

    except Exception as e:
        print(f"An error occurred during save/load testing: {e}")

    print("\n=== Testing load_network with missing file ===")
    try:
        load_network("this_file_does_not_exist.csv")
    except FileNotFoundError:
        print("Correctly raised FileNotFoundError for missing file.")


if __name__ == "__main__":
    main()