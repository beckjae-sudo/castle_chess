"""Round model for Castle Chess."""

from dataclasses import dataclass, field

from models.match import Match


@dataclass
class Round:
    """Represent one numbered round in a tournament."""

    number: int
    matches: list[Match] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the round number and its pairings."""
        if self.number < 1:
            raise ValueError("Round number must be at least 1.")

        self._validate_unique_players()

    @property
    def is_complete(self) -> bool:
        """Return whether every match in the round has a result."""
        return bool(self.matches) and all(
            match.is_complete for match in self.matches
        )

    def add_match(self, match: Match) -> None:
        """Add a match if neither player is already paired this round."""
        self.matches.append(match)

        try:
            self._validate_unique_players()
        except ValueError:
            self.matches.pop()
            raise

    def _validate_unique_players(self) -> None:
        """Ensure each player appears only once in this round."""
        player_ids = []

        for match in self.matches:
            player_ids.extend(
                [match.white_player_id, match.black_player_id]
            )

        if len(player_ids) != len(set(player_ids)):
            raise ValueError(
                "A player cannot be assigned to multiple matches in one round."
            )

    def to_dict(self) -> dict:
        """Serialize this round for JSON storage."""
        return {
            "number": self.number,
            "matches": [match.to_dict() for match in self.matches],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Round":
        """Create a round instance from JSON-compatible data."""
        return cls(
            number=data["number"],
            matches=[
                Match.from_dict(match_data)
                for match_data in data.get("matches", [])
            ],
        )
