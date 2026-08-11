"""Business logic for running Castle Chess tournaments."""

import random

from models.match import Match
from models.round import Round
from models.tournament import Tournament


class TournamentService:
    """Run tournament operations without handling user interface concerns."""

    @staticmethod
    def register_player(tournament: Tournament, chess_id: str) -> None:
        """Register a player for a tournament."""
        tournament.register_player(chess_id)

    @staticmethod
    def start_first_round(tournament: Tournament) -> Round:
        """Create the first round with random pairings."""
        if tournament.rounds:
            raise ValueError("The first round has already been created.")

        if len(tournament.registered_player_ids) < 2:
            raise ValueError("At least two players are required.")

        if len(tournament.registered_player_ids) % 2 != 0:
            raise ValueError("An even number of players is required.")

        player_ids = tournament.registered_player_ids.copy()
        random.shuffle(player_ids)

        round_ = Round(number=1)

        for index in range(0, len(player_ids), 2):
            round_.add_match(
                Match(
                    white_player_id=player_ids[index],
                    black_player_id=player_ids[index + 1],
                )
            )

        tournament.add_round(round_)
        return round_

    @staticmethod
    def record_result(
        tournament: Tournament,
        match_index: int,
        result: str,
    ) -> None:
        """Record the result of a match in the current round."""
        if not tournament.rounds:
            raise ValueError("The tournament has not started.")

        current_round = tournament.rounds[-1]

        if current_round.is_complete:
            raise ValueError("The current round is already complete.")

        try:
            match = current_round.matches[match_index]
        except IndexError:
            raise ValueError("Invalid match number.") from None

        match.record_result(result)

    @staticmethod
    def generate_next_round(tournament: Tournament) -> Round:
        """Generate the next round using tournament standings."""
        if not tournament.rounds:
            return TournamentService.start_first_round(tournament)

        current_round = tournament.rounds[-1]

        if not current_round.is_complete:
            raise ValueError(
                "All matches must have results before advancing."
            )

        if tournament.is_complete:
            raise ValueError("The tournament is already complete.")

        rankings = tournament.standings()
        pairings = TournamentService._pair_players(
            rankings,
            tournament,
        )

        round_number = len(tournament.rounds) + 1
        round_ = Round(number=round_number)

        for white_id, black_id in pairings:
            round_.add_match(
                Match(
                    white_player_id=white_id,
                    black_player_id=black_id,
                )
            )

        tournament.add_round(round_)
        return round_

    @staticmethod
    def _pair_players(
        rankings: list[tuple[str, float]],
        tournament: Tournament,
    ) -> list[tuple[str, str]]:
        """Pair players by score while trying to avoid repeat matches."""
        groups: dict[float, list[str]] = {}

        for chess_id, points in rankings:
            groups.setdefault(points, []).append(chess_id)

        ordered_players = []

        for players in groups.values():
            random.shuffle(players)
            ordered_players.extend(players)

        pairings = []
        remaining = ordered_players.copy()

        while remaining:
            player = remaining.pop(0)

            opponent_index = TournamentService._find_opponent(
                player,
                remaining,
                tournament,
            )

            if opponent_index is None:
                opponent_index = 0

            opponent = remaining.pop(opponent_index)
            pairings.append((player, opponent))

        return pairings

    @staticmethod
    def _find_opponent(
        player: str,
        candidates: list[str],
        tournament: Tournament,
    ) -> int | None:
        """Find a candidate who has not played this player before."""
        previous_opponents = set()

        for round_ in tournament.rounds:
            for match in round_.matches:
                if match.white_player_id == player:
                    previous_opponents.add(match.black_player_id)
                elif match.black_player_id == player:
                    previous_opponents.add(match.white_player_id)

        for index, candidate in enumerate(candidates):
            if candidate not in previous_opponents:
                return index

        return None
    