"""Tournament report generation."""

from models.tournament import Tournament


class ReportService:
    """Generate plain-text tournament reports."""

    @staticmethod
    def generate(tournament: Tournament, players_by_id: dict) -> str:
        """Return a formatted report for a tournament."""
        lines = [
            "=" * 60,
            "CASTLE CHESS TOURNAMENT REPORT",
            "=" * 60,
            f"Name: {tournament.name}",
            f"Venue: {tournament.venue}",
            f"Dates: {tournament.start_date} to {tournament.end_date}",
            f"Rounds: {tournament.number_of_rounds}",
            "",
            "STANDINGS",
            "-" * 60,
        ]

        for position, (chess_id, points) in enumerate(
            tournament.standings(),
            start=1,
        ):
            player = players_by_id[chess_id]

            lines.append(
                f"{position:>2}. "
                f"{player.name} ({player.chess_id}) "
                f"{points:.1f} points"
            )

        lines.extend(
            [
                "",
                "ROUNDS",
                "-" * 60,
            ]
        )

        for round_ in tournament.rounds:
            lines.append(f"Round {round_.number}")

            for match in round_.matches:
                white = players_by_id[match.white_player_id]
                black = players_by_id[match.black_player_id]
                result = match.result or "Not played"

                lines.append(
                    f"  {white.name} ({white.chess_id}) vs "
                    f"{black.name} ({black.chess_id}) - {result}"
                )

            lines.append("")

        return "\n".join(lines)
