"""Match model for Castle Chess."""

from dataclasses import dataclass


WHITE_WIN = "white_win"
BLACK_WIN = "black_win"
DRAW = "draw"
VALID_RESULTS = {WHITE_WIN, BLACK_WIN, DRAW}


@dataclass
class Match:
    """Represent one match between two tournament players."""

    white_player_id: str
    black_player_id: str
    result: str | None = None

    def __post_init__(self) -> None:
        """Ensure a player is not paired with themselves."""
        if self.white_player_id == self.black_player_id:
            raise ValueError("A player cannot play against themselves.")

        if self.result is not None and self.result not in VALID_RESULTS:
            raise ValueError("Match result is invalid.")

    @property
    def is_complete(self) -> bool:
        """Return whether a result has been recorded."""
        return self.result is not None

    def record_result(self, result: str) -> None:
        """Record a win or draw for this match."""
        if result not in VALID_RESULTS:
            raise ValueError("Match result is invalid.")

        self.result = result

    def points(self) -> dict[str, float]:
        """Return tournament points awarded by this match."""
        if self.result is None:
            return {}

        if self.result == WHITE_WIN:
            return {
                self.white_player_id: 1.0,
                self.black_player_id: 0.0,
            }

        if self.result == BLACK_WIN:
            return {
                self.white_player_id: 0.0,
                self.black_player_id: 1.0,
            }

        return {
            self.white_player_id: 0.5,
            self.black_player_id: 0.5,
        }

    def to_dict(self) -> dict:
        """Serialize this match for JSON storage."""
        return {
            "white_player_id": self.white_player_id,
            "black_player_id": self.black_player_id,
            "result": self.result,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Match":
        """Create a match instance from JSON-compatible data."""
        return cls(
            white_player_id=data["white_player_id"],
            black_player_id=data["black_player_id"],
            result=data.get("result"),
        )