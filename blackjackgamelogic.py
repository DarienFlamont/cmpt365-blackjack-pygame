#This is the code that will invoke our blackjack game
import random
import os
import sys

def initializeDeck():
	deck = []

	card_values = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
	card_suits = ['Hearts','Spades','Clubs','Diamonds']

	for i in card_values:
		for j in card_suits:
			card = [i,j]
			#deck.append(i + ' of ' + j)
			deck.append(card)

	print(len(deck))
	print(deck)
	for i in range(len(deck)):
		print(deck[i][0])
		print(deck[i][1])
		print(deck[i][0] + ' of ' + deck[i][1])
	return deck

def deal(deck):
	hand = []
	for i in range(2):
		card = deck.pop()
		print("This is our card popped from deck:")
		print(card)
		hand.append(card)

	return hand

def hit(deck, hand):
	card = deck.pop()
	hand.append(card)

	return hand

def total(hand):
	total = 0
	for card in hand:
		if card[0] == 'Jack' or card[0] == 'Queen' or card[0] == 'King':
			total += 10
		elif card[0] == 'Ace':
			if total >= 11:
				total += 1
			else:
				total += 11
		else:
			total += int(card[0])
	return total

def replay():
	replay = input("Do you want to play again? (Y/N): ").lower()
	if replay == "y":
		main()
	else:
		print("Bye!")
		exit()

def score(dealer_hand, player_hand):
	if total(player_hand) == 21:
		print ("Congrats! You got a Blackjack!\n")
		print("Your hand had:")
		for card in player_hand:
			print(card[0] + " of " + card[1])
		print("The dealer had:")
		for card in dealer_hand:
			print(card[0] + " of " + card[1])

	elif total(dealer_hand) == 21:
		print ("Sorry! You lose. The dealer got a blackjack.\n")
		print("Your hand had:")
		for card in player_hand:
			print(card[0] + " of " + card[1])
		print("The dealer had:")
		for card in dealer_hand:
			print(card[0] + " of " + card[1])

	elif total(player_hand) > 21:
		print ("Sorry! You have busted. You lose.\n")
		print("Your hand had:")
		for card in player_hand:
			print(card[0] + " of " + card[1])
		print("The dealer had:")
		for card in dealer_hand:
			print(card[0] + " of " + card[1])

	elif total(dealer_hand) > 21:		   
		print ("Congrats the dealer busts. You win!\n")
		print("Your hand had:")
		for card in player_hand:
			print(card[0] + " of " + card[1])
		print("The dealer had:")
		for card in dealer_hand:
			print(card[0] + " of " + card[1])

	elif total(player_hand) < total(dealer_hand):
		print("You have less than the dealer.  You lose!")
		print("Your hand had:")
		for card in player_hand:
			print(card[0] + " of " + card[1])
		print("The dealer had:")
		for card in dealer_hand:
			print(card[0] + " of " + card[1])
	elif total(player_hand) > total(dealer_hand):
		print("Congrats! You have more than the dealer.  You win!")
		print("Your hand had:")
		for card in player_hand:
			print(card[0] + " of " + card[1])
		print("The dealer had:")
		for card in dealer_hand:
			print(card[0] + " of " + card[1])

def main():
	playing_deck = initializeDeck()
	random.shuffle(playing_deck)

	player_hand = deal(playing_deck)
	print("This is our players hand after being dealt 2 cards:")
	print(player_hand)
	print("The total for the player is:")
	print(total(player_hand))
	dealer_hand = deal(playing_deck)
	print("This is our dealers hand after being dealt 2 cards:")
	print(dealer_hand)
	print("The total for the dealer is:")
	print(total(dealer_hand))

	print("This is our deck after dealing both hands:")
	print(len(playing_deck))
	print(playing_deck)

if __name__ == "__main__":
	main()