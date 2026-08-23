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
        """Display players with selection numbers."""
        print("\nPlayers:")

        for index, player in enumerate(players, start=1):
            print(
            f"{index}. "
            f"{player.name} ({player.chess_id}) - "
            f"{player.email} - "
            f"{player.birthdate}"
        )

    @staticmethod
    def show_pairings(round_, players_by_id):
        """Display round pairings using player names and Chess IDs."""
        print(f"\n--- Round {round_.number} ---")

        for index, match in enumerate(round_.matches, start=1):
            white = players_by_id[match.white_player_id]
            black = players_by_id[match.black_player_id]
            result = match.result or "Not played"

            print(
                f"{index}. "
                f"{white.name} ({white.chess_id}) vs "
                f"{black.name} ({black.chess_id}) "
                f"[{result}]"
            )

    @staticmethod
    def show_standings(tournament, players_by_id):
        """Display standings using player names and Chess IDs."""
        print("\n--- Standings ---")

        standings = tournament.standings()

        for position, (chess_id, points) in enumerate(
            standings,
            start=1,
        ):
            player = players_by_id[chess_id]

            print(
                f"{position:>2}. "
                f"{player.name} ({player.chess_id}) "
                f"{points:.1f} points"
            )

    @staticmethod
    def show_menu():
        print("\nMain Menu")
        print("1. List clubs")
        print("2. List players")
        print("3. Add player")
        print("4. Create tournament")
        print("5. Generate tournament report")
        print("6. Exit")

    @staticmethod
    def get_choice():
        return input("\nChoose an option: ").strip()

    @staticmethod
    def show_message(message):
        print(f"\n{message}")

    @staticmethod
    def get_input(prompt):
        return input(prompt).strip()
