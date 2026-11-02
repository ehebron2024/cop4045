# Based on program13-14.py
# Copyright 2017, 2013, 2011 Pearson Education, Inc., W.F. Punch & R.J.Enbody
"""Predator-Prey-Human Simulation
   Five classes are defined: Animal, Prey, Predator, Human and Island
   where Island is where the simulation is taking place,
   i.e. where the prey, predators and humans interact (live).
   Lists of prey, predators and humans are instantiated, and
   then their breeding, eating, and dying are simulated.
   Humans eat predators (never prey), and starve if they do not.
"""
from __future__ import annotations

import random
from typing import List, Tuple, Union

import matplotlib.pyplot as plt


class Island(object):
    """Island
       n X n grid where zero value indicates not occupied."""

    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0,
                 human_count: int = 0) -> None:
        """Initialize grid to all 0's, then fill with animals.

        Precondition: the animal counts sum to at most n*n (ValueError otherwise).
        """
        if prey_count + predator_count + human_count > n * n:
            raise ValueError("more animals than grid cells")
        self.grid_size: int = n
        self.grid: List[List[Union[int, Animal]]] = []
        for i in range(n):
            row = [0] * n    # row is a list of n zeros
            self.grid.append(row)
        self.init_animals(prey_count, predator_count, human_count)

    def init_animals(self, prey_count: int, predator_count: int,
                     human_count: int) -> None:
        """Put some initial animals on the island, at random unoccupied positions.

        Postcondition: the island holds prey_count Prey, predator_count
        Predators and human_count Humans.
        """
        for animal_class, count in ((Prey, prey_count),
                                    (Predator, predator_count),
                                    (Human, human_count)):
            placed = 0
            # loop continues until count unoccupied positions are found
            while placed < count:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if not self.animal(x, y):
                    self.register(animal_class(island=self, x=x, y=y))
                    placed += 1

    def clear_all_moved_flags(self) -> None:
        """Animals have a moved flag to indicate they moved this turn.
        Clear that so we can do the next turn.
        """
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Return size of the island: one dimension."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Register animal with island, i.e. put it at the animal's coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove animal from island."""
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Union[Animal, int]:
        """Return animal at location (x,y): 0 if empty, -1 if outside the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        else:
            return -1  # outside island boundary

    def __str__(self) -> str:
        """String representation for printing.
        (0,0) will be in the lower left corner.
        """
        s = ""
        for j in range(self.grid_size - 1, -1, -1):  # print row size-1 first
            for i in range(self.grid_size):          # each row starts at 0
                if not self.grid[i][j]:
                    # print a '.' for an empty space
                    s += "{:<2s}".format('.' + "  ")
                else:
                    s += "{:<2s}".format((str(self.grid[i][j])) + "  ")
            s += "\n"
        return s

    def count(self, animal_class: type) -> int:
        """Count all the animals on the island that are instances of animal_class."""
        total = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if isinstance(self.animal(x, y), animal_class):
                    total += 1
        return total

    def count_prey(self) -> int:
        """Count all the prey on the island."""
        return self.count(Prey)

    def count_predators(self) -> int:
        """Count all the predators on the island."""
        return self.count(Predator)

    def count_humans(self) -> int:
        """Count all the humans on the island."""
        return self.count(Human)


class Animal(object):
    """An animal living on an island. Subclasses must define the class
    attribute breed_time and an instance attribute breed_clock, and a
    clock_tick() method.
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "A") -> None:
        """Initialize the animal's island, position and display character."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> Tuple[int, int]:
        """Return coordinates of current position."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the character displayed on the island grid."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> Union[Tuple[int, int], int]:
        """Look in the 8 directions from the animal's location
        and return the first location that presently has an object
        of exactly the specified type. Return 0 if no such location exists.
        """
        # neighbor offsets
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        result = 0
        for i in range(len(offset)):
            x = self.x + offset[i][0]  # neighboring coordinates
            y = self.y + offset[i][1]
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                result = (x, y)
                break
        return result

    def move_to(self, location: Tuple[int, int]) -> None:
        """Move to location (which must be on the island), re-registering
        with the island and setting the moved flag. Any animal that was at
        location is removed from the island first.
        """
        victim = self.island.animal(location[0], location[1])
        if victim:
            self.island.remove(victim)
        self.island.remove(self)   # remove from current spot
        self.x = location[0]       # new coordinates
        self.y = location[1]
        self.island.register(self) # register new coordinates
        self.moved = True

    def eat(self) -> None:
        """Look for food. By default animals do not eat; subclasses override."""

    def move(self) -> None:
        """Move to an open, neighboring position."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.move_to(location)

    def breed(self) -> None:
        """Breed a new animal of the same class. If there is room in one of
        the 8 locations place the new animal there. Otherwise you have to wait.
        """
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                the_class = self.__class__
                new_animal = the_class(self.island, x=location[0], y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        """Clear the moved flag so the animal can move on the next turn."""
        self.moved = False


class Prey(Animal):
    """Prey: moves, breeds every Prey.breed_time ticks, gets eaten by predators."""

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "O") -> None:
        """Create prey; Prey.breed_time must be set before instantiation."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Prey only updates its local breed clock."""
        self.breed_clock -= 1


class Predator(Animal):
    """Predator: eats prey, starves after Predator.starve_time ticks without eating."""

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "X") -> None:
        """Create a predator; Predator.breed_time and starve_time must be set first."""
        Animal.__init__(self, island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Predator updates both breeding and starving; starved predators die."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Predator looks for one of the 8 locations with Prey. If found
        moves to that location, updates the starve clock, removes the Prey.
        """
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                self.move_to(location)
                self.starve_clock = self.starve_time


class Human(Animal):
    """Human: moves and breeds like any animal, and every Human.hunt_time
    ticks hunts a neighboring Predator. Humans never kill prey. A human
    starves after Human.starve_time ticks without killing a predator.
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "H") -> None:
        """Create a human; Human.breed_time, starve_time and hunt_time must be set first."""
        Animal.__init__(self, island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time
        self.hunt_clock = self.hunt_time

    def clock_tick(self) -> None:
        """Human updates breeding, starving and hunting clocks; starved humans die."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """When the hunt clock has run out, look for a neighboring Predator.
        If found, move to its cell, removing it, and reset the starve clock.
        The hunt clock restarts whether or not a predator was found.
        """
        if not self.moved and self.hunt_clock <= 0:
            self.hunt_clock = self.hunt_time
            location = self.check_grid(Predator)
            if location:
                self.move_to(location)
                self.starve_clock = self.starve_time


###########################################
def has_converged(history: List[Tuple[int, int, int]], window: int) -> bool:
    """Return True iff the last `window` recorded (prey, predator, human)
    count triples are all identical (and there are at least `window` of them).
    """
    return len(history) >= window and len(set(history[-window:])) == 1


def main(predator_breed_time: int = 6, predator_starve_time: int = 3,
         initial_predators: int = 10, prey_breed_time: int = 3,
         initial_prey: int = 50, human_breed_time: int = 10,
         human_starve_time: int = 15, human_hunt_time: int = 3,
         initial_humans: int = 5, size: int = 10, ticks: int = 1000,
         stable_window: int = 50) -> None:
    """Main simulation. Sets class attributes, runs the event loop, plots at the end.

    The loop ends after `ticks` time units, or when the prey, predator and
    human populations have all stayed constant for `stable_window` ticks.
    """
    # initialization values
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    # for graphing
    predator_list: List[int] = []
    prey_list: List[int] = []
    human_list: List[int] = []
    history: List[Tuple[int, int, int]] = []

    # make an island
    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print("Initial island:")
    print(isle)

    # event loop.
    # For all the ticks, for every x,y location.
    # If there is an animal there, try eat, move, breed and clock_tick
    for i in range(ticks):
        # important to clear all the moved flags!
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        # record info for display, plotting
        counts = (isle.count_prey(), isle.count_predators(), isle.count_humans())
        prey_list.append(counts[0])
        predator_list.append(counts[1])
        human_list.append(counts[2])
        history.append(counts)
        # print out every 10th cycle, see what's going on
        if not i % 10:
            print("tick {}: prey={} predators={} humans={}".format(i, *counts))
        if has_converged(history, stable_window):
            print("Populations constant for {} ticks; stopping at tick {}."
                  .format(stable_window, i))
            break

    print("Final island:")
    print(isle)
    print("Final counts: prey={} predators={} humans={}".format(*history[-1]))

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.xlabel("Time (clock ticks)")
    plt.ylabel("Population")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
