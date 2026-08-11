"""Tournament model for Castle Chess."""

from dataclasses import dataclass, field
from datetime import date

from models.round import Round


@dataclass
class Tournament:
    """Represent a chess tournament and its current state."""

    name: str
    venue: str
    start_date: date
    end_date: date
    number_of_rounds: int
    registered_player_ids: list[str] = field(default_factory=list)
    rounds: list[Round] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate required tournament data."""
        self.name = self.name.strip()
        self.venue = self.venue.strip()

        if not self.name:
            raise ValueError("Tournament name is required.")

        if not self.venue:
            raise ValueError("Tournament venue is required.")

        if self.end_date < self.start_date:
            raise ValueError("Tournament end date cannot be before start date.")

        if self.number_of_rounds < 1:
            raise ValueError("A tournament must have at least one round.")

    @property
    def current_round_number(self) -> int:
        """Return the current round number, or zero before play begins."""
        return len(self.rounds)

    @property
    def is_complete(self) -> bool:
        """Return whether every required round has been completed."""
        return (
            len(self.rounds) == self.number_of_rounds
            and self.rounds[-1].is_complete
        )

    def register_player(self, chess_id: str) -> None:
        """Register a player once for this tournament."""
        if chess_id in self.registered_player_ids:
            raise ValueError("Player is already registered.")

        self.registered_player_ids.append(chess_id)

    def add_round(self, round_: Round) -> None:
        """Add the next sequential round to the tournament."""
        expected_number = len(self.rounds) + 1

        if round_.number != expected_number:
            raise ValueError(
                f"Expected round {expected_number}, got round {round_.number}."
            )

        self.rounds.append(round_)

    def standings(self) -> list[tuple[str, float]]:
        """Return player IDs and tournament points, highest first."""
        points = {
            chess_id: 0.0 for chess_id in self.registered_player_ids
        }

        for round_ in self.rounds:
            for match in round_.matches:
                for chess_id, score in match.points().items():
                    points[chess_id] += score

        return sorted(
            points.items(),
            key=lambda item: item[1],
            reverse=True,
        )

    def to_dict(self) -> dict:
        """Serialize this tournament for JSON storage."""
        return {
            "name": self.name,
            "venue": self.venue,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "number_of_rounds": self.number_of_rounds,
            "registered_player_ids": self.registered_player_ids,
            "rounds": [round_.to_dict() for round_ in self.rounds],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        """Create a tournament instance from JSON-compatible data."""
        return cls(
            name=data["name"],
            venue=data["venue"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            number_of_rounds=data["number_of_rounds"],
            registered_player_ids=data.get("registered_player_ids", []),
            rounds=[
                Round.from_dict(round_data)
                for round_data in data.get("rounds", [])
            ],
        )