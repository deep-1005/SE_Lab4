from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def round(self):
    # Get a valid wager before changing the bankroll
        while True:
            try:
                wager = int(input(f"Enter wager (1-{self.chips}): ").strip())
            except ValueError:
                print("Invalid wager. Enter a whole number.")
                continue

            if wager <= 0 or wager > self.chips:
                print(f"Invalid wager. Enter an amount between 1 and {self.chips}.")
                continue

            break

        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]

        print("Cards dealt.")
        self.show(player, dealer)

        player_value = hand_value(player)
        dealer_value = hand_value(dealer)

        # Natural blackjack
        if player_value == 21:
            self.show(player, dealer, hide=False)

            if dealer_value == 21:
                print("Push - both have blackjack.")
            else:
                self.chips += wager
                print(f"Blackjack! Player wins +{wager} chips.")

            return True

        if dealer_value == 21:
            self.show(player, dealer, hide=False)
            self.chips -= wager
            print(f"Dealer has blackjack. You lose {wager} chips.")
            return True

        # Player's turn
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                print("Quitting round.")
                return False

            if key == "s":
                print("Player stands.")
                break

            if key == "h":
                card = deck.draw()

                if card is None:
                    print("Deck is empty.")
                    return True

                player.append(card)
                print(f"Player draws {card[0]}{card[1]}.")
                self.show(player, dealer)

                if hand_value(player) > 21:
                    self.chips -= wager
                    print(f"Player busts. You lose {wager} chips.")
                    return True

            else:
                print("Invalid command. Use h, s, or q.")

        # Player has 21
        if hand_value(player) == 21:
            print("Player has 21.")

        # Dealer draws until 17
        while hand_value(dealer) < 17:
            card = deck.draw()

            if card is None:
                print("Deck is empty.")
                break

            dealer.append(card)
            print(f"Dealer draws {card[0]}{card[1]}.")

        # Show final hands
        self.show(player, dealer, hide=False)

        pv = hand_value(player)
        dv = hand_value(dealer)

        # Dealer bust
        if dv > 21:
            self.chips += wager
            print(f"Dealer busts. Player wins +{wager} chips.")
            return True

        # Compare scores
        if pv > dv:
            self.chips += wager
            print(f"Player wins +{wager} chips.")
        elif pv < dv:
            self.chips -= wager
            print(f"Dealer wins. You lose {wager} chips.")
        else:
            print("Push. Your wager is returned.")

        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                return
            if input("Play again? [y/n]: ").strip().lower() != "y":
                return
