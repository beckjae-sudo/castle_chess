"""Tests for the Castle Chess tournament service."""

from datetime import date

import pytest

from models.tournament import Tournament
from services.tournament_service import TournamentService

PLAYER_IDS = [
    "AA11111",
    "BB22222",
    "CC33333",
    "DD44444",
    "EE55555",
    "FF66666",
    "GG77777",
    "HH88888",
]


def make_tournament(number_of_rounds=3):
    """Create a tournament populated with test players."""
    tournament = Tournament(
        name="Test Tournament",
        venue="Test Venue",
        start_date=date(2026, 8, 14),
        end_date=date(2026, 8, 14),
        number_of_rounds=number_of_rounds,
    )

    for chess_id in PLAYER_IDS:
        tournament.register_player(chess_id)

    return tournament


def test_first_round_pairs_every_player_once():
    tournament = make_tournament()

    round_ = TournamentService.start_first_round(tournament)

    paired_players = []

    for match in round_.matches:
        paired_players.extend(
            [match.white_player_id, match.black_player_id]
        )

    assert len(round_.matches) == 4
    assert len(paired_players) == 8
    assert set(paired_players) == set(PLAYER_IDS)


def test_first_round_is_numbered_one():
    tournament = make_tournament()

    round_ = TournamentService.start_first_round(tournament)

    assert round_.number == 1
    assert tournament.current_round_number == 1


def test_match_results_produce_correct_standings():
    tournament = make_tournament()

    round_ = TournamentService.start_first_round(tournament)

    for index in range(len(round_.matches)):
        TournamentService.record_result(
            tournament,
            index,
            "draw",
        )

    standings = tournament.standings()

    assert len(standings) == 8
    assert all(points == 0.5 for _, points in standings)


def test_tournament_cannot_advance_before_round_is_complete():
    tournament = make_tournament()

    TournamentService.start_first_round(tournament)

    with pytest.raises(ValueError):
        TournamentService.generate_next_round(tournament)


def test_completed_round_can_generate_next_round():
    tournament = make_tournament()

    round_1 = TournamentService.start_first_round(tournament)

    for index in range(len(round_1.matches)):
        TournamentService.record_result(
            tournament,
            index,
            "draw",
        )

    round_2 = TournamentService.generate_next_round(tournament)

    assert round_2.number == 2
    assert tournament.current_round_number == 2


def test_player_cannot_be_registered_twice():
    tournament = make_tournament()

    with pytest.raises(ValueError):
        tournament.register_player(PLAYER_IDS[0])


def test_odd_number_of_players_is_rejected():
    tournament = Tournament(
        name="Odd Tournament",
        venue="Test Venue",
        start_date=date(2026, 8, 14),
        end_date=date(2026, 8, 14),
        number_of_rounds=3,
    )

    for chess_id in PLAYER_IDS[:7]:
        tournament.register_player(chess_id)

    with pytest.raises(ValueError):
        TournamentService.start_first_round(tournament)


def test_invalid_match_result_is_rejected():
    tournament = make_tournament()

    TournamentService.start_first_round(tournament)

    with pytest.raises(ValueError):
        TournamentService.record_result(
            tournament,
            0,
            "not_a_real_result",
        )


def test_repeat_opponents_are_avoided_when_possible():
    tournament = make_tournament()

    round_1 = TournamentService.start_first_round(tournament)

    for index in range(len(round_1.matches)):
        TournamentService.record_result(
            tournament,
            index,
            "draw",
        )

    round_2 = TournamentService.generate_next_round(tournament)

    round_1_pairs = {
        frozenset(
            [match.white_player_id, match.black_player_id]
        )
        for match in round_1.matches
    }

    round_2_pairs = {
        frozenset(
            [match.white_player_id, match.black_player_id]
        )
        for match in round_2.matches
    }

    assert round_1_pairs.isdisjoint(round_2_pairs)


def test_tournament_completes_after_required_rounds():
    tournament = make_tournament(number_of_rounds=2)

    round_1 = TournamentService.start_first_round(tournament)

    for index in range(len(round_1.matches)):
        TournamentService.record_result(
            tournament,
            index,
            "draw",
        )

    round_2 = TournamentService.generate_next_round(tournament)

    for index in range(len(round_2.matches)):
        TournamentService.record_result(
            tournament,
            index,
            "draw",
        )

    assert tournament.is_complete


def test_completed_tournament_cannot_generate_another_round():
    tournament = make_tournament(number_of_rounds=1)

    round_1 = TournamentService.start_first_round(tournament)

    for index in range(len(round_1.matches)):
        TournamentService.record_result(
            tournament,
            index,
            "draw",
        )

    assert tournament.is_complete

    with pytest.raises(ValueError):
        TournamentService.generate_next_round(tournament)


def test_next_round_pairs_players_by_score():
    tournament = make_tournament()

    round_1 = TournamentService.start_first_round(tournament)

    for index, match in enumerate(round_1.matches):
        if index % 2 == 0:
            TournamentService.record_result(
                tournament,
                index,
                "white_win",
            )
        else:
            TournamentService.record_result(
                tournament,
                index,
                "black_win",
            )

    standings = tournament.standings()

    top_players = {
        chess_id
        for chess_id, points in standings
        if points == 1.0
    }

    bottom_players = {
        chess_id
        for chess_id, points in standings
        if points == 0.0
    }

    round_2 = TournamentService.generate_next_round(tournament)

    for match in round_2.matches:
        players = {
            match.white_player_id,
            match.black_player_id,
        }

        assert players <= top_players or players <= bottom_players
