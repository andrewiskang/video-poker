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
sample_card_1 = Card("A", "Spades")
sample_card_2 = Card("A", "Spades")
sample_card_3 = Card("A", "Hearts")
sample_card_4 = Card("9", "Hearts")

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
    print("  "),
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
sample_hand = sample_deck.draw_hand()
print("Sample Hand:")
print("  "),
sample_hand.print_hand()
print("After drawing, deck contains 47 cards:")
if len(sample_deck) == 47:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nWe are going to redraw all cards from an empty deck:")
sample_hand = empty_deck.redraw(sample_hand, [0, 1, 2, 3, 4])
print("  "),
sample_hand.print_hand()
print("After redrawing, empty deck continues to contain 0 cards:")
if len(empty_deck) == 0:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nWe are going to redraw the middle card from an empty deck:")
sample_hand = empty_deck.redraw(sample_hand, [2])
print("  "),
sample_hand.print_hand()
print("After redrawing, empty deck continues to contain 0 cards:")
if len(empty_deck) == 0:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nWe are going to redraw the middle card from the correct deck:")
sample_hand = sample_deck.redraw(sample_hand, [2])
print("  "),
sample_hand.print_hand()
print("After redrawing, deck continues to contains 47 cards:")
if len(sample_deck) == 47:
    success()
    total += 1
    passed += 1
else:
    failure()
    total += 1

print("\nTotal Tests: " + str(total))
print("Passed Tests: " + str(passed))
print("Failed Tests: " + str(total - passed))
