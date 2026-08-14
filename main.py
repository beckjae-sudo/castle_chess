"""Castle Chess application entry point."""

from datetime import date

from models.club_manager import ClubManager
from models.tournament_manager import TournamentManager
from services.tournament_service import TournamentService
from views.console_view import ConsoleView
from services.report_service import ReportService


class CastleChessApp:
    """Coordinate the Castle Chess application."""

    def __init__(self):
        self.club_manager = ClubManager()
        self.tournament_manager = TournamentManager()
        self.view = ConsoleView()

    def run(self):
        """Run the main application loop."""
        self.view.show_title()

        while True:
            self.view.show_menu()
            choice = self.view.get_choice()

            if choice == "1":
                self.list_clubs()

            elif choice == "2":
                self.list_players()

            elif choice == "3":
                self.create_tournament()

            elif choice == "4":
                self.generate_report()

            elif choice == "5":
                self.view.show_message("Goodbye!")
                break

            else:
                self.view.show_message("Invalid choice.")

    def list_clubs(self):
        """Display all available clubs."""
        if not self.club_manager.clubs:
            self.view.show_message("No clubs found.")
            return

        self.view.show_clubs(self.club_manager.clubs)

    def list_players(self):
        """Display players from a selected club."""
        club = self.select_club()

        if club:
            self.view.show_players(club.players)

    def select_club(self):
        """Ask the user to select a club."""
        clubs = self.club_manager.clubs

        if not clubs:
            self.view.show_message("No clubs found.")
            return None

        self.view.show_clubs(clubs)

        choice = self.view.get_input("Select club: ")

        try:
            index = int(choice) - 1
            return clubs[index]
        except (ValueError, IndexError):
            self.view.show_message("Invalid club selection.")
            return None

    def create_tournament(self):
        """Create and run a new tournament."""
        self.view.show_message("Create Tournament")

        name = self.view.get_input("Tournament name: ")
        venue = self.view.get_input("Venue: ")

        try:
            number_of_rounds = int(
                self.view.get_input("Number of rounds: ")
            )
        except ValueError:
            self.view.show_message("Number of rounds must be a number.")
            return

        club = self.select_club()

        if club is None:
            return

        tournament = self.tournament_manager.create(
            name=name,
            venue=venue,
            start_date=date.today(),
            end_date=date.today(),
            number_of_rounds=number_of_rounds,
        )

        self.view.show_players(club.players)

        player_ids = self.view.get_input(
            "\nEnter player IDs separated by commas: "
        )

        selected_ids = [
            chess_id.strip().upper()
            for chess_id in player_ids.split(",")
            if chess_id.strip()
        ]

        try:
            for chess_id in selected_ids:
                if not any(
                    player.chess_id == chess_id
                    for player in club.players
                ):
                    raise ValueError(
                        f"Player {chess_id} does not belong to this club."
                    )

                tournament.register_player(chess_id)

            if len(tournament.registered_player_ids) < 2:
                raise ValueError(
                    "At least two players must be registered."
                )

            if len(tournament.registered_player_ids) % 2 != 0:
                raise ValueError(
                    "An even number of players is required."
                )

        except ValueError as error:
            self.view.show_message(str(error))
            return

        self.tournament_manager.save(tournament)

        self.run_tournament(tournament)

    def run_tournament(self, tournament):
        """Run rounds until the tournament is complete."""
        try:
            TournamentService.start_first_round(tournament)
            self.tournament_manager.save(tournament)

            while True:
                current_round = tournament.rounds[-1]

                self.view.show_pairings(current_round)

                for index, match in enumerate(
                    current_round.matches,
                    start=1,
                ):
                    print(
                        f"\nMatch {index}: "
                        f"{match.white_player_id} vs "
                        f"{match.black_player_id}"
                    )

                    while True:
                        print("1. White wins")
                        print("2. Black wins")
                        print("3. Draw")

                        result = self.view.get_input("Result: ")

                        result_map = {
                            "1": "white_win",
                            "2": "black_win",
                            "3": "draw",
                        }

                        if result not in result_map:
                            self.view.show_message(
                                "Invalid result. Please enter 1, 2, or 3."
                            )
                            continue

                        TournamentService.record_result(
                            tournament,
                            index - 1,
                            result_map[result]
                        )

                        self.tournament_manager.save(tournament)
                        break

                self.view.show_standings(tournament)

                if tournament.is_complete:
                    self.view.show_message(
                        "Tournament complete!"
                    )
                    break

                choice = self.view.get_input(
                    "\nGenerate next round? (y/n): "
                ).lower()

                if choice != "y":
                    self.view.show_message(
                        "Tournament paused. "
                        "The current state has been saved."
                    )
                    break

                TournamentService.generate_next_round(tournament)
                self.tournament_manager.save(tournament)

        except ValueError as error:
            self.view.show_message(str(error))

    def generate_report(self):
        """Display a report for a saved tournament."""
        if not self.tournament_manager.tournaments:
            self.view.show_message("No tournaments found.")
            return

        print("\nAvailable tournaments:")

        for index, tournament in enumerate(
            self.tournament_manager.tournaments,
            start=1,
        ):
            print(f"{index}. {tournament.name}")

        choice = self.view.get_input("Select tournament: ")

        try:
            tournament = self.tournament_manager.tournaments[
                int(choice) - 1
            ]
        except (ValueError, IndexError):
            self.view.show_message("Invalid tournament selection.")
            return

        print()
        print(ReportService.generate(tournament))


if __name__ == "__main__":
    app = CastleChessApp()
    app.run()
