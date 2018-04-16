from video_poker import Card, Deck, Hand, Payout
import random

# keep track of all tests
total = 0
passed = 0

# success, failure functions that increment total and passed test count
def success():
    # prints success
    print("  Test passed!")
    global total, passed
    total += 1
    passed += 1
def failure():
    # prints failure
    print("  Test failed!")
    global total
    total += 1






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
else:
    failure()

print (sample_card_1.info() + " != " + sample_card_3.info() + ":")
if sample_card_1 != sample_card_3:
    success()
else:
    failure()

print (sample_card_1.info() + " != " + sample_card_4.info() + ":")
if sample_card_1 != sample_card_4:
    success()
else:
    failure()

print (sample_card_3.info() + " != " + sample_card_4.info() + ":")
if sample_card_3 != sample_card_4:
    success()
else:
    failure()

# Deck tests
print("\n\nDECK TESTS")

print("Full deck of cards contains the following:")
new_deck = Deck.full_deck()
for card in new_deck:
    print(" "),
    card.print_card()

print("Full deck of cards contains 52 cards:")
if len(new_deck) == 52:
    success()
else:
    failure()

print("Empty deck of cards contains 0 cards:")
empty_deck = Deck()
if len(empty_deck) == 0:
    success()
else:
    failure()

# Hand tests
print("\n\nHAND TESTS")

sample_deck = Deck.full_deck()
sample_hand_1 = sample_deck.draw_hand()
print("\nSample Hand:")
print(" "),
sample_hand_1.print_hand()
print("After drawing, deck contains 47 cards:")
if len(sample_deck) == 47:
    success()
else:
    failure()

print("\nWe are going to redraw all cards from an empty deck:")
sample_hand_1 = empty_deck.redraw(sample_hand_1, [])
print(" "),
sample_hand_1.print_hand()
print("After redrawing, empty deck continues to contain 0 cards:")
if len(empty_deck) == 0:
    success()
else:
    failure()

print("\nWe are going to redraw the middle card from an empty deck:")
sample_hand_1 = empty_deck.redraw(sample_hand_1, [0,1,3,4])
print(" "),
sample_hand_1.print_hand()
print("After redrawing, empty deck continues to contain 0 cards:")
if len(empty_deck) == 0:
    success()
else:
    failure()

print("\nWe are going to redraw the middle card from the correct deck:")
sample_hand_1 = sample_deck.redraw(sample_hand_1, [0,1,3,4])
print(" "),
sample_hand_1.print_hand()
print("After redrawing, deck continues to contains 47 cards:")
if len(sample_deck) == 47:
    success()
else:
    failure()

# outcome tests
print("\n\nOUTCOME TESTS")

def outcome_test(hand, expected_outcome):
    # helper function to compare outcomes of given hands with expected outcome
    hand_outcome = hand.outcome()
    print("\nThe following hand is a: " + hand_outcome)
    print(" "),
    hand.print_hand()
    if hand_outcome == expected_outcome:
        success()
    else:
        failure()

# royal flush
sample_hand_2 = Hand([Card(11, "Diamonds"), Card(1, "Diamonds"),
                      Card(12, "Diamonds"), Card(10, "Diamonds"),
                      Card(13, "Diamonds")])
outcome_test(sample_hand_2, "Royal Flush")
# straight flush
sample_hand_3 = Hand([Card(11, "Diamonds"), Card(9, "Diamonds"),
                      Card(12, "Diamonds"), Card(10, "Diamonds"),
                      Card(13, "Diamonds")])
outcome_test(sample_hand_3, "Straight Flush")
# straight
sample_hand_4 = Hand([Card(11, "Diamonds"), Card(1, "Diamonds"),
                      Card(12, "Diamonds"), Card(10, "Spades"),
                      Card(13, "Diamonds")])
outcome_test(sample_hand_4, "Straight")
# flush
sample_hand_5 = Hand([Card(11, "Hearts"), Card(2, "Hearts"),
                      Card(12, "Hearts"), Card(10, "Hearts"),
                      Card(13, "Hearts")])
outcome_test(sample_hand_5, "Flush")
# four of a kind
sample_hand_6 = Hand([Card(11, "Hearts"), Card(11, "Diamonds"),
                      Card(11, "Spades"), Card(11, "Clubs"),
                      Card(13, "Hearts")])
outcome_test(sample_hand_6, "Four of a Kind")
# full house
sample_hand_7 = Hand([Card(11, "Diamonds"), Card(1, "Diamonds"),
                      Card(11, "Spades"), Card(11, "Hearts"),
                      Card(1, "Clubs")])
outcome_test(sample_hand_7, "Full House")
# three of a kind
sample_hand_8 = Hand([Card(11, "Diamonds"), Card(4, "Diamonds"),
                      Card(11, "Spades"), Card(11, "Hearts"),
                      Card(1, "Clubs")])
outcome_test(sample_hand_8, "Three of a Kind")
# two pair
sample_hand_9 = Hand([Card(11, "Diamonds"), Card(4, "Diamonds"),
                      Card(11, "Spades"), Card(4, "Hearts"),
                      Card(1, "Clubs")])
outcome_test(sample_hand_9, "Two Pair")
# jacks or better
sample_hand_10 = Hand([Card(11, "Diamonds"), Card(4, "Diamonds"),
                       Card(11, "Spades"), Card(12, "Hearts"),
                       Card(1, "Clubs")])
outcome_test(sample_hand_10, "Jacks or Better")

# Payout Tests
print("\n\nPAYOUT TESTS")

def payout_test(payout, outcome, expected_amount):
    # helper function to compare payouts of outcomes with expected payout amount
    payout_amount = payout.table[outcome]
    print(outcome + " payout is: " + str(payout_amount))
    if payout_amount == expected_amount:
        success()
    else:
        failure()

print("\nDefault (9/6) payout table, should be 800-50-25-9-6-4-3-2-1")
sample_payout_1 = Payout()
sample_payout_1.print_payout()
payout_test(sample_payout_1, "Royal Flush", 800)
payout_test(sample_payout_1, "Straight Flush", 50)
payout_test(sample_payout_1, "Four of a Kind", 25)
payout_test(sample_payout_1, "Full House", 9)
payout_test(sample_payout_1, "Flush", 6)
payout_test(sample_payout_1, "Straight", 4)
payout_test(sample_payout_1, "Three of a Kind", 3)
payout_test(sample_payout_1, "Two Pair", 2)
payout_test(sample_payout_1, "Jacks or Better", 1)

print("\nCustom (8/5) payout table, should be 800-50-25-8-5-4-3-2-1")
sample_payout_1 = Payout(full_house=8, flush=5)
sample_payout_1.print_payout()
payout_test(sample_payout_1, "Royal Flush", 800)
payout_test(sample_payout_1, "Straight Flush", 50)
payout_test(sample_payout_1, "Four of a Kind", 25)
payout_test(sample_payout_1, "Full House", 8)
payout_test(sample_payout_1, "Flush", 5)
payout_test(sample_payout_1, "Straight", 4)
payout_test(sample_payout_1, "Three of a Kind", 3)
payout_test(sample_payout_1, "Two Pair", 2)
payout_test(sample_payout_1, "Jacks or Better", 1)

print("\nTotal Tests: " + str(total))
print("Passed Tests: " + str(passed))
print("Failed Tests: " + str(total - passed))
