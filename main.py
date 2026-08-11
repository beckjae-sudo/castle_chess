"""Entry point for Castle Chess."""

from datetime import date
from models import tournament
from models.match import DRAW, Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament


def main() -> None:
    """Create and display sample models."""
    player_one = Player(
        name="Ada Lovelace",
        email="ada@example.com",
        chess_id="AL12345",
        birthdate=date(1815, 12, 10),
    )

    player_two = Player(
        name="Grace Hopper",
        email="grace@example.com",
        chess_id="GH67890",
        birthdate=date(1906, 12, 9),
    )

    match = Match(
        white_player_id=player_one.chess_id,
        black_player_id=player_two.chess_id,
    )

    match.record_result(DRAW)

    round_one = Round(number=1, matches=[match])
    tournament = Tournament(
        name="Castle Chess Summer Open",
        venue="Castle Chess Club",
        start_date=date(2026, 8, 14),
        end_date=date(2026, 8, 14),
        number_of_rounds=3,
    )

    tournament.register_player(player_one.chess_id)
    tournament.register_player(player_two.chess_id)
    tournament.add_round(round_one)

    print(player_one)
    print(player_two)
    print(match)
    print(match.points())
    print(round_one)
    print(f"Round complete: {round_one.is_complete}")
    print(tournament)
    print(f"Standings: {tournament.standings()}")
    print(f"Tournament complete: {tournament.is_complete}")


if __name__ == "__main__":
    main()

