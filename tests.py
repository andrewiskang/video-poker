import video_poker



def success(total_tests, passed_tests):
    # prints success
    print("Test passed!")
def failure(total_tests):
    # prints failure
    print("Test failed!")




def tests():
    # function to hold all tests

    # keep track of all tests
    total = 0
    passed = 0

    # sample cards
    sample_card_1 = Card("A", "Spades")
    sample_card_2 = Card("A", "Spades")
    sample_card_3 = Card("A", "Hearts")
    sample_card_4 = Card("9", "Hearts")

    # card tests
    print("Card Tests")

    print("card 1 == card 2")
    if sample_card_1 == sample_card_2:
        success(total, passed)
    else:
        failure(total)

    print("card 1 != card 3")
    if sample_card_1 != sample_card_3:
        success(total, passed)
    else:
        failure(total)

    print("card 1 != card 4")
    if sample_card_1 != sample_card_4:
        success(total, passed)
    else:
        failure(total)

    print("card 3 != card 4")
    if sample_card_3 != sample_card_4:
        success(total, passed)
    else:
        failure(total)

    # deck tests
    print("\nDeck Tests")

    deck = full_deck()
    for card in deck:
        card.print_card()
    if len(deck) = 52:
        success(total, passed)
    else:
        failure(total)

    print("\nTotal Tests:", str(total))
    print("Passed Tests:", str(passed))
    print("Failed Tests:", str(total - passed))
