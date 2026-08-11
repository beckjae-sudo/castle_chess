from datetime import date
from models.tournament_manager import TournamentManager


def main():
    manager = TournamentManager()

    tournament = manager.create(
        name="Persistence Test Open",
        venue="Castle Chess Club",
        start_date=date(2026, 8, 14),
        end_date=date(2026, 8, 14),
        number_of_rounds=3,
    )

    tournament.register_player("NG39713")
    tournament.register_player("JW63361")

    manager.save(tournament)

    print(f"Saved: {tournament.name}")

    new_manager = TournamentManager()

    print(f"Loaded {len(new_manager.tournaments)} tournament(s).")

    for loaded in new_manager.tournaments:
        print(loaded)


if __name__ == "__main__":
    main()
