"""Player model for Castle Chess."""

from dataclasses import dataclass
from datetime import date
import re


CHESS_ID_PATTERN = re.compile(r"^[A-Z]{2}\d{5}$")


@dataclass
class Player:
    """Represent a player registered with a chess club."""

    name: str
    email: str
    chess_id: str
    birthdate: date

    def __post_init__(self) -> None:
        """Validate and normalize player data."""
        self.name = self.name.strip()
        self.email = self.email.strip()
        self.chess_id = self.chess_id.strip().upper()

        if not self.name:
            raise ValueError("A player name is required.")

        if not self.email or "@" not in self.email:
            raise ValueError("A valid email address is required.")

        if not CHESS_ID_PATTERN.fullmatch(self.chess_id):
            raise ValueError(
                "Chess identifier must contain two letters and five digits."
            )

    def to_dict(self) -> dict:
        """Serialize this player for JSON storage."""
        return {
            "name": self.name,
            "email": self.email,
            "chess_id": self.chess_id,
            "birthdate": self.birthdate.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create a player instance from JSON-compatible data."""
        return cls(
            name=data["name"],
            email=data["email"],
            chess_id=data["chess_id"],
            birthdate=date.fromisoformat(data["birthdate"]),
        )