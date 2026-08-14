from models.club_manager import ClubManager


def main():
    manager = ClubManager()

    print(f"Loaded {len(manager.clubs)} clubs.")

    for club in manager.clubs:
        print(f"{club.name}: {len(club.players)} players")

        if club.players:
            player = club.players[0]
            print(f"  First player: {player.name}")
            print(f"  Chess ID: {player.chess_id}")
            print(f"  Birthdate: {player.birthdate}")


if __name__ == "__main__":
    main()
