from video_poker import Card, Deck, Hand
import random


def success():
    # prints success
    print("  Test passed!")
def failure():
    # prints failure
    print("  Test failed!")




# keep track of all tests
total = 0
passed = 0

# sample Cards
sample_card_1 = Card(1, "Spades")
sample_card_2 = Card(1, "Spades")
sample_card_3 = Card(1, "Hearts")
sample_card_4 = Card(9, "Hearts")

# Card tests
print("CARD TESTS")

print (sample_card_1.info() + " == " + sample_card_2.info() + ":")
if sample_card_1 == sample_card_2:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print (sample_card_1.info() + " != " + sample_card_3.info() + ":")
if sample_card_1 != sample_card_3:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print (sample_card_1.info() + " != " + sample_card_4.info() + ":")
if sample_card_1 != sample_card_4:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print (sample_card_3.info() + " != " + sample_card_4.info() + ":")
if sample_card_3 != sample_card_4:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# Deck tests
print("\nDECK TESTS")

print("Full deck of cards contains the following:")
new_deck = Deck.full_deck()
for card in new_deck:
    print(" "),
    card.print_card()

print("Full deck of cards contains 52 cards:")
if len(new_deck) == 52:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("Empty deck of cards contains 0 cards:")
empty_deck = Deck()
if len(empty_deck) == 0:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# Hand tests
print("\nHAND TESTS")

sample_deck = Deck.full_deck()
sample_hand_1 = sample_deck.draw_hand()
print("Sample Hand:")
print(" "),
sample_hand_1.print_hand()
print("After drawing, deck contains 47 cards:")
if len(sample_deck) == 47:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nWe are going to redraw all cards from an empty deck:")
sample_hand_1 = empty_deck.redraw(sample_hand_1, [0, 1, 2, 3, 4])
print(" "),
sample_hand_1.print_hand()
print("After redrawing, empty deck continues to contain 0 cards:")
if len(empty_deck) == 0:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nWe are going to redraw the middle card from an empty deck:")
sample_hand_1 = empty_deck.redraw(sample_hand_1, [2])
print(" "),
sample_hand_1.print_hand()
print("After redrawing, empty deck continues to contain 0 cards:")
if len(empty_deck) == 0:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nWe are going to redraw the middle card from the correct deck:")
sample_hand_1 = sample_deck.redraw(sample_hand_1, [2])
print(" "),
sample_hand_1.print_hand()
print("After redrawing, deck continues to contains 47 cards:")
if len(sample_deck) == 47:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# outcome tests
print("\nOUTCOME TESTS")

# royal flush
sample_hand_2 = Hand([Card(11, "Diamonds"), Card(1, "Diamonds"),
                      Card(12, "Diamonds"), Card(10, "Diamonds"),
                      Card(13, "Diamonds")])
sample_hand_2_outcome = sample_hand_2.outcome()
print("\nThe following hand is a " + sample_hand_2_outcome)
print(" "),
sample_hand_2.print_hand()
if sample_hand_2_outcome == "Royal Flush":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# straight flush
sample_hand_3 = Hand([Card(11, "Diamonds"), Card(9, "Diamonds"),
                      Card(12, "Diamonds"), Card(10, "Diamonds"),
                      Card(13, "Diamonds")])
sample_hand_3_outcome = sample_hand_3.outcome()
print("\nThe following hand is a " + sample_hand_3_outcome)
print(" "),
sample_hand_3.print_hand()
if sample_hand_3_outcome == "Straight Flush":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# straight
sample_hand_4 = Hand([Card(11, "Diamonds"), Card(1, "Diamonds"),
                      Card(12, "Diamonds"), Card(10, "Spades"),
                      Card(13, "Diamonds")])
sample_hand_4_outcome = sample_hand_4.outcome()
print("\nThe following hand is a " + sample_hand_4_outcome)
print(" "),
sample_hand_4.print_hand()
if sample_hand_4_outcome == "Straight":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# flush
sample_hand_5 = Hand([Card(11, "Hearts"), Card(2, "Hearts"),
                      Card(12, "Hearts"), Card(10, "Hearts"),
                      Card(13, "Hearts")])
sample_hand_5_outcome = sample_hand_5.outcome()
print("\nThe following hand is a " + sample_hand_5_outcome)
print(" "),
sample_hand_5.print_hand()
if sample_hand_5_outcome == "Flush":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# four of a kind
sample_hand_6 = Hand([Card(11, "Hearts"), Card(11, "Diamonds"),
                      Card(11, "Spades"), Card(11, "Clubs"),
                      Card(13, "Hearts")])
sample_hand_6_outcome = sample_hand_6.outcome()
print("\nThe following hand is a " + sample_hand_6_outcome)
print(" "),
sample_hand_6.print_hand()
if sample_hand_6_outcome == "Four of a Kind":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# full house
sample_hand_7 = Hand([Card(11, "Diamonds"), Card(1, "Diamonds"),
                      Card(11, "Spades"), Card(11, "Hearts"),
                      Card(1, "Clubs")])
sample_hand_7_outcome = sample_hand_7.outcome()
print("\nThe following hand is a " + sample_hand_7_outcome)
print(" "),
sample_hand_7.print_hand()
if sample_hand_7_outcome == "Full House":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# three of a kind
sample_hand_8 = Hand([Card(11, "Diamonds"), Card(4, "Diamonds"),
                      Card(11, "Spades"), Card(11, "Hearts"),
                      Card(1, "Clubs")])
sample_hand_8_outcome = sample_hand_8.outcome()
print("\nThe following hand is a " + sample_hand_8_outcome)
print(" "),
sample_hand_8.print_hand()
if sample_hand_8_outcome == "Three of a Kind":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# two pair
sample_hand_9 = Hand([Card(11, "Diamonds"), Card(4, "Diamonds"),
                      Card(11, "Spades"), Card(4, "Hearts"),
                      Card(1, "Clubs")])
sample_hand_9_outcome = sample_hand_9.outcome()
print("\nThe following hand is a " + sample_hand_9_outcome)
print(" "),
sample_hand_9.print_hand()
if sample_hand_9_outcome == "Two Pair":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# jacks or better
sample_hand_10 = Hand([Card(11, "Diamonds"), Card(4, "Diamonds"),
                       Card(11, "Spades"), Card(12, "Hearts"),
                       Card(1, "Clubs")])
sample_hand_10_outcome = sample_hand_10.outcome()
print("\nThe following hand is a " + sample_hand_10_outcome)
print(" "),
sample_hand_10.print_hand()
if sample_hand_10_outcome == "Jacks or Better":
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

# Payout Tests
print("\nPAYOUT TESTS")

print("\nTotal Tests: " + str(total))
print("Passed Tests: " + str(passed))
print("Failed Tests: " + str(total - passed))
