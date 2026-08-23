"""Castle Chess application entry point."""

from datetime import date, datetime

from models.club_manager import ClubManager
from models.tournament_manager import TournamentManager
from services.report_service import ReportService
from services.tournament_service import TournamentService
from views.console_view import ConsoleView


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
                self.add_player()

            elif choice == "4":
                self.create_tournament()

            elif choice == "5":
                self.generate_report()

            elif choice == "6":
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

    def get_players_by_id(self):
        """Return all club players indexed by Chess ID."""
        return {
            player.chess_id: player
            for club in self.club_manager.clubs
            for player in club.players
        }

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

    def add_player(self):
        """Create a new player and add them to a selected club."""
        club = self.select_club()

        if club is None:
            return

        self.view.show_message("Add New Player")

        name = self.view.get_input("Player name: ")
        email = self.view.get_input("Email address: ")
        chess_id = self.view.get_input("Chess ID: ").upper()
        birthday_text = self.view.get_input(
            "Birthdate (MM-DD-YYYY): "
        )

        try:
            birthday = datetime.strptime(
                birthday_text,
                "%m-%d-%Y",
            ).date()

            if any(
                player.chess_id == chess_id
                for player in club.players
            ):
                raise ValueError(
                    "A player with that Chess ID already exists."
                )

            player = club.create_player(
                name=name,
                email=email,
                chess_id=chess_id,
                birthdate=birthday,
            )

            self.view.show_message(
                f"Player {player.name} was added successfully."
            )

        except ValueError as error:
            self.view.show_message(str(error))

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
            self.view.show_message(
                "Number of rounds must be a number."
            )
            return

        tournament = self.tournament_manager.create(
            name=name,
            venue=venue,
            start_date=date.today(),
            end_date=date.today(),
            number_of_rounds=number_of_rounds,
        )

        self.register_players(tournament)

        if len(tournament.registered_player_ids) < 2:
            self.view.show_message(
                "At least two players must be registered."
            )
            return

        if len(tournament.registered_player_ids) % 2 != 0:
            self.view.show_message(
                "An even number of players is required."
            )
            return

        self.tournament_manager.save(tournament)
        self.run_tournament(tournament)

    def register_players(self, tournament):
        """Allow players to be searched and registered."""
        while True:
            available_players = [
                player
                for club in self.club_manager.clubs
                for player in club.players
                if player.chess_id
                not in tournament.registered_player_ids
            ]

            print(
                "\nRegistered players: "
                f"{len(tournament.registered_player_ids)}"
            )

            print("1. List available players")
            print("2. Search by Chess ID")
            print("3. Search by player name")
            print("4. Finish registration")
            print("5. Add a new player")

            choice = self.view.get_input("Choose an option: ")

            if choice == "1":
                self.view.show_players(available_players)

            elif choice == "2":
                chess_id = self.view.get_input(
                    "Enter Chess ID: "
                ).upper()

                matches = [
                    player
                    for player in available_players
                    if player.chess_id == chess_id
                ]

                self.select_player_for_tournament(
                    tournament,
                    matches,
                )

            elif choice == "3":
                name = self.view.get_input(
                    "Enter part of the player's name: "
                ).lower()

                matches = [
                    player
                    for player in available_players
                    if name in player.name.lower()
                ]

                self.select_player_for_tournament(
                    tournament,
                    matches,
                )

            elif choice == "4":
                return

            elif choice == "5":
                self.add_player()

            else:
                self.view.show_message("Invalid choice.")

    def select_player_for_tournament(
        self,
        tournament,
        players,
    ):
        """Register one player from a list of search results."""
        if not players:
            self.view.show_message(
                "No matching players found."
            )
            return

        self.view.show_players(players)

        choice = self.view.get_input(
            "Select player number, or press Enter to cancel: "
        )

        if not choice:
            return

        try:
            player = players[int(choice) - 1]
        except (ValueError, IndexError):
            self.view.show_message(
                "Invalid player selection."
            )
            return

        try:
            tournament.register_player(player.chess_id)

            self.view.show_message(
                f"{player.name} registered successfully."
            )

            self.tournament_manager.save(tournament)

        except ValueError as error:
            self.view.show_message(str(error))

    def run_tournament(self, tournament):
        """Run rounds until the tournament is complete."""
        try:
            TournamentService.start_first_round(tournament)
            self.tournament_manager.save(tournament)

            while True:
                current_round = tournament.rounds[-1]
                players_by_id = self.get_players_by_id()

                self.view.show_pairings(
                    current_round,
                    players_by_id,
                )

                for index, match in enumerate(
                    current_round.matches,
                    start=1,
                ):
                    white = players_by_id[match.white_player_id]
                    black = players_by_id[match.black_player_id]

                    print(
                        f"\nMatch {index}: "
                        f"{white.name} ({white.chess_id}) vs "
                        f"{black.name} ({black.chess_id})"
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
                            result_map[result],
                        )

                        self.tournament_manager.save(tournament)
                        break

                self.view.show_standings(
                    tournament,
                    players_by_id,
                )

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

        players_by_id = self.get_players_by_id()

        print(
            ReportService.generate(
                tournament,
                players_by_id,
            )
        )


if __name__ == "__main__":
    app = CastleChessApp()
    app.run()
