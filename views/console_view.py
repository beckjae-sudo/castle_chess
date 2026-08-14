"""Console display functions for Castle Chess."""


class ConsoleView:
    """Handle displaying information and collecting basic input."""

    @staticmethod
    def show_title():
        print("\n" + "=" * 50)
        print("                 CASTLE CHESS")
        print("=" * 50)

    @staticmethod
    def show_clubs(clubs):
        print("\nAvailable clubs:")

        for index, club in enumerate(clubs, start=1):
            print(f"{index}. {club.name} ({len(club.players)} players)")

    @staticmethod
    def show_players(players):
        print("\nPlayers:")

        for player in players:
            print(
                f"{player.chess_id:<8} "
                f"{player.name:<25} "
                f"{player.email}"
            )

    @staticmethod
    def show_pairings(round_):
        print(f"\n--- Round {round_.number} ---")

        for index, match in enumerate(round_.matches, start=1):
            result = match.result or "Not played"

            print(
                f"{index}. "
                f"{match.white_player_id} vs "
                f"{match.black_player_id} "
                f"[{result}]"
            )

    @staticmethod
    def show_standings(tournament):
        print("\n--- Standings ---")

        standings = tournament.standings()

        for position, (chess_id, points) in enumerate(
            standings,
            start=1,
        ):
            print(f"{position:>2}. {chess_id:<8} {points:.1f} points")

    @staticmethod
    def show_menu():
        print("\nMain Menu")
        print("1. List clubs")
        print("2. List players")
        print("3. Create tournament")
        print("4. Generate tournament report")
        print("5. Exit")

    @staticmethod
    def get_choice():
        return input("\nChoose an option: ").strip()

    @staticmethod
    def show_message(message):
        print(f"\n{message}")

    @staticmethod
    def get_input(prompt):
        return input(prompt).strip()
