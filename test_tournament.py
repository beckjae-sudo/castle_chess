
from datetime import date

from models.tournament import Tournament
from services.tournament_service import TournamentService


def main():
    tournament = Tournament(
        name="Castle Chess Test Open",
        venue="Castle Chess Club",
        start_date=date(2026, 8, 14),
        end_date=date(2026, 8, 14),
        number_of_rounds=3,
    )

    players = [
        "NG39713",
        "JW63361",
        "QZ98880",
        "QQ22510",
        "QF01697",
        "BR95594",
        "GN87065",
        "LH07588",
    ]

    for chess_id in players:
        TournamentService.register_player(tournament, chess_id)

    round_1 = TournamentService.start_first_round(tournament)

    print("ROUND 1")
    for match in round_1.matches:
        print(match)

    for index in range(len(round_1.matches)):
        TournamentService.record_result(tournament, index, "draw")

    print("\nSTANDINGS")
    print(tournament.standings())

    round_2 = TournamentService.generate_next_round(tournament)

    print("\nROUND 2")
    for match in round_2.matches:
        print(match)


if __name__ == "__main__":
    main()
