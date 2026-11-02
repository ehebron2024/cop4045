from typing import Dict, List


class ParkingPermit:
    """A parking permit purchased by an owner for some number of months.

    The fee schedule is a dictionary mapping fee names to dollar amounts.
    The base class uses the key "monthly" (cost per month).
    """

    def __init__(self, owner: str, months: int, fees: Dict[str, float]) -> None:
        """Create a permit.

        Preconditions: months >= 0 (ValueError otherwise); fees contains
        every key the permit type needs (KeyError is raised by cost() if not).
        The fee dictionary is copied, so later changes to the argument do not
        affect this permit.
        """
        if months < 0:
            raise ValueError("months must be non-negative")
        self.owner: str = owner
        self.months: int = months
        self.fees: Dict[str, float] = dict(fees)

    def cost(self) -> float:
        """Return the total cost: months * fees["monthly"]."""
        return self.months * self.fees["monthly"]

    def __str__(self) -> str:
        """Return a readable description including the owner and the cost."""
        return (f"{type(self).__name__} for {self.owner}, "
                f"{self.months} month(s), cost ${self.cost():.2f}")

    def __repr__(self) -> str:
        """Return an unambiguous representation of the permit."""
        return (f"{type(self).__name__}(owner={self.owner!r}, "
                f"months={self.months!r}, fees={self.fees!r})")


class StudentPermit(ParkingPermit):
    """A student permit; additionally stores the number of vehicles.

    Uses fee keys "monthly" and "extra_vehicle" (one-time fee per vehicle
    after the first).
    """

    def __init__(self, owner: str, months: int, fees: Dict[str, float],
                 vehicles: int) -> None:
        """Create a student permit. Precondition: vehicles >= 1 (ValueError otherwise)."""
        super().__init__(owner, months, fees)
        if vehicles < 1:
            raise ValueError("a permit needs at least one vehicle")
        self.vehicles: int = vehicles

    def cost(self) -> float:
        """Return monthly fees plus a one-time fee for each vehicle after the first."""
        return (super().cost()
                + (self.vehicles - 1) * self.fees["extra_vehicle"])

    def __str__(self) -> str:
        """Return a readable description including vehicles and cost."""
        return super().__str__() + f", {self.vehicles} vehicle(s)"

    def __repr__(self) -> str:
        """Return an unambiguous representation of the permit."""
        return (f"{type(self).__name__}(owner={self.owner!r}, "
                f"months={self.months!r}, fees={self.fees!r}, "
                f"vehicles={self.vehicles!r})")


class FacultyPermit(ParkingPermit):
    """A faculty permit; additionally stores whether garage access is included.

    Uses fee keys "monthly" and "garage_monthly" (extra cost per month for
    garage access).
    """

    def __init__(self, owner: str, months: int, fees: Dict[str, float],
                 garage: bool) -> None:
        """Create a faculty permit; garage is True if garage access is included."""
        super().__init__(owner, months, fees)
        self.garage: bool = garage

    def cost(self) -> float:
        """Return monthly fees, plus the monthly garage fee if garage access is included."""
        total = super().cost()
        if self.garage:
            total += self.months * self.fees["garage_monthly"]
        return total

    def __str__(self) -> str:
        """Return a readable description including garage access and cost."""
        return super().__str__() + f", garage access: {'yes' if self.garage else 'no'}"

    def __repr__(self) -> str:
        """Return an unambiguous representation of the permit."""
        return (f"{type(self).__name__}(owner={self.owner!r}, "
                f"months={self.months!r}, fees={self.fees!r}, "
                f"garage={self.garage!r})")


def summarize_list(permits: List[ParkingPermit]) -> float:
    """Print each permit (owner name and cost, via its __str__) and return the total revenue.

    Parameters: permits - a possibly mixed list of ParkingPermit objects.
    Returns: the sum of cost() over all permits (0 for an empty list).
    """
    total = 0.0
    for permit in permits:
        print(permit)
        total += permit.cost()
    return total


def main() -> None:
    """Demonstrate the permit classes and summarize_list."""
    student_fees = {"monthly": 25, "extra_vehicle": 10}
    faculty_fees = {"monthly": 40, "garage_monthly": 15}

    permits: List[ParkingPermit] = [
        StudentPermit("Alice", 4, student_fees, 1),
        StudentPermit("Bob", 6, student_fees, 3),
        FacultyPermit("Dr. Chen", 12, faculty_fees, True),
        FacultyPermit("Prof. Diaz", 3, faculty_fees, False),
    ]

    print("repr of each permit:")
    for p in permits:
        print(repr(p))

    print("\nSummary:")
    total = summarize_list(permits)
    print(f"Total revenue: ${total:.2f}")


if __name__ == "__main__":
    main()
