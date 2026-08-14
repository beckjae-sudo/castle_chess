"""Tournament report generation."""

from models.tournament import Tournament


class ReportService:
    """Generate plain-text tournament reports."""

    @staticmethod
    def generate(tournament: Tournament) -> str:
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
            lines.append(
                f"{position:>2}. {chess_id:<10} {points:.1f} points"
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
                result = match.result or "Not played"
                lines.append(
                    f"  {match.white_player_id} vs "
                    f"{match.black_player_id} - {result}"
                )

            lines.append("")

        return "\n".join(lines)
