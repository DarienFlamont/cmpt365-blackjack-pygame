import random
import time

import pygame
import components
from components import Button
from scenes.scene_template import Scene

#PLEASE CHANGE THIS RESOURCES PATH TO WHEREEVER THE FINAL PROJECT IS STORED ON YOUR MACHINE
#YOU NEED TO INCLUDE 2 \\'s AT THE END AS THE LAST ONE IS PERCEIVED AS EOL (END OF LINE)
resources_path = r"C:\Users\user\Desktop\SFU\CMPT 365\Final Project\Blackjack\resources\\"

button_width = 150
button_height = 60
size = (928, 696)
centerx = size[0] // 2
centery = size[1] // 2
black = 0, 0, 0

deal_button_rect = pygame.Rect((centerx + button_width / 2 + 200), (centery - button_height / 2 + 100), button_width,
                               button_height)
hit_button_rect = pygame.Rect((centerx + button_width / 2 + 200), (centery - button_height / 2 + 200), button_width,
                              button_height)
stay_button_rect = pygame.Rect((centerx + button_width / 2 + 200), (centery - button_height / 2 + 300), button_width,
                               button_height)

deal_button_color = (253, 205, 68)
stay_button_color = (0, 83, 155)
hit_button_color = (208, 32, 0)
button_text_color = (0, 0, 0)

background_felt = pygame.image.load(resources_path + r"graphics\casino_felt.jpg")
background_felt = pygame.transform.scale(background_felt, size)

def play_click():
    path = resources_path + r"sounds\click.wav"
    sound = pygame.mixer.Sound(path)
    sound.play()

def play_cardfan():
    path = resources_path + r"sounds\cardFan1.wav"
    sound = pygame.mixer.Sound(path)
    sound.play()


def play_cardplace1():
    path = resources_path + r"sounds\cardPlace1.wav"
    sound = pygame.mixer.Sound(path)
    sound.play()


def play_cardplace2():
    path = resources_path + r"sounds\cardPlace2.wav"
    sound = pygame.mixer.Sound(path)
    sound.play()


def play_deal():
    path = resources_path + r"sounds\deal.wav"
    sound = pygame.mixer.Sound(path)
    sound.play()


class deck_back(pygame.sprite.Sprite):
    def __init__(self, position = (10,10)):
        pygame.sprite.Sprite.__init__(self)
        path = resources_path + r"graphics\deck_back.png"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (175, 275))
        self.image = image
        self.rect = (*position, 175, 275)


    def draw(self, surface):
        surface.blit(self.image, self.rect)


class card_sprite(pygame.sprite.Sprite):

    def __init__(self, card, position):
        pygame.sprite.Sprite.__init__(self)
        path = resources_path + r"graphics\playing_cards\\" + card[0] + card[1] + ".png"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (175, 275))
        self.image = image
        self.rect = (*position, 175, 275)

    # def update(self):
    # self.rect.center = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class deal_button(pygame.sprite.Sprite):

    def __init__(self, button_color, rect, button_text_color, font, size, text=''):
        self.button_color = button_color
        self.rect = rect
        self.text = text
        self.font = font
        self.size = size
        self.button_text_color = button_text_color
        self.button = self.make_button()
        
    def make_button(self):
        final_button = pygame.Surface((self.rect.w, self.rect.h)).convert()
        final_button.fill(self.button_color)
        final_button_rect = final_button.get_rect()
        if self.text != '':
            fontpath = resources_path + r"fonts\{}.ttf".format(self.font)
            font = pygame.font.Font(fontpath, self.size)
            text = font.render(self.text, 1, self.button_text_color)
            final_button.blit(text, text.get_rect(center=final_button_rect.center))
        return final_button

    def update(self, click, funds, bet, dealt_deck, player_hand_list, dealer_hand_list, player_hand_sprites, dealer_hand_sprites, GeneralDisplay):
  

        if bet>=funds:
            bet = funds

        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.left + self.rect.w:
            if pos[1] > self.rect.top and pos[1] < self.rect.top + self.rect.h:
                if click == 1 and funds>=bet and bet != 0:
                    init_deck = initialize_shuffle_deck()
                    play_deal()
                    funds -= bet
                    player_hand_sprites =  CardGroup ((370,400))
                    dealer_hand_sprites =  CardGroup ((370,50), dealer = True)
                    dealt_deck, player_hand_list, dealer_hand_list = deal(init_deck)
                    if player_hand_list and dealer_hand_list:
                        for card in player_hand_list:
                            player_hand_sprites.card_add(card)
                        for card in dealer_hand_list:
                            dealer_hand_sprites.card_add(card)

                    check = blackjack_check(player_hand_list,dealer_hand_list)
                    if check == "dealer_win":
                        dealer_hand_sprites = dealer_hand_sprites.flip_dealer_card()
                        GeneralDisplay.update("DEALER BLACKJACK!","${} LOST ".format(bet))
                        click = 0
                        return click, funds, bet, None, None, None, player_hand_sprites, dealer_hand_sprites, GeneralDisplay
                    elif check == "push":
                        dealer_hand_sprites = dealer_hand_sprites.flip_dealer_card()
                        GeneralDisplay.update("PUSH! BOTH BLACKJACK!","${} RETURNED ".format(bet))
                        funds += bet
                        click = 0
                        return click, funds, bet, None, None, None, player_hand_sprites, dealer_hand_sprites, GeneralDisplay
                    elif check == "player_blackjack":
                        dealer_hand_sprites = dealer_hand_sprites.flip_dealer_card()
                        GeneralDisplay.update("PLAYER BLACKJACK!","${} WON ".format(3*bet))
                        funds += (3 * bet)
                        return click, funds, bet, None, None, None, player_hand_sprites, dealer_hand_sprites, GeneralDisplay
                    click = 0
        return click, funds, bet, dealt_deck, player_hand_list, dealer_hand_list, player_hand_sprites, dealer_hand_sprites, GeneralDisplay

    def draw(self, surface):
        surface.blit(self.button, self.rect)


class hit_button(pygame.sprite.Sprite):

    def __init__(self, button_color, rect, button_text_color, font, size, text=''):
        self.button_color = button_color
        self.rect = rect
        self.text = text
        self.font = font
        self.size = size
        self.button_text_color = button_text_color
        self.button = self.make_button()

    def make_button(self):
        final_button = pygame.Surface((self.rect.w, self.rect.h)).convert()
        final_button.fill(self.button_color)
        final_button_rect = final_button.get_rect()
        if self.text != '':
            fontpath = resources_path + r"fonts\{}.ttf".format(self.font)
            font = pygame.font.Font(fontpath, self.size)
            text = font.render(self.text, 1, self.button_text_color)
            final_button.blit(text, text.get_rect(center=final_button_rect.center))
        return final_button

    def update(self, click, deck, player_hand_list,player_hand_sprites):

        flag = 0

        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.left + self.rect.w:
            if pos[1] > self.rect.top and pos[1] < self.rect.top + self.rect.h:
                if click == 1:
                    #print("hit button clicked")
                    play_cardplace1()
                    pre_hit_len = len(player_hand_list)
                    deck, player_hand_list, flag = hit(deck, player_hand_list)

                    for card in range(pre_hit_len,len(player_hand_list)):
                        player_hand_sprites.card_add(player_hand_list[card])
                    click = 0

        return click, deck, player_hand_list, flag

    def draw(self, surface):
        surface.blit(self.button, self.rect)


class stay_button(pygame.sprite.Sprite):

    def __init__(self, button_color, rect, button_text_color, font, size, text=''):
        self.button_color = button_color
        self.rect = rect
        self.text = text
        self.font = font
        self.size = size
        self.button_text_color = button_text_color
        self.button = self.make_button()

    def make_button(self):
        final_button = pygame.Surface((self.rect.w, self.rect.h)).convert()
        final_button.fill(self.button_color)
        final_button_rect = final_button.get_rect()
        if self.text != '':
            fontpath = resources_path + r"fonts\{}.ttf".format(self.font)
            font = pygame.font.Font(fontpath, self.size)
            text = font.render(self.text, 1, self.button_text_color)
            final_button.blit(text, text.get_rect(center=final_button_rect.center))
        return final_button

    def update(self, click, deck ,player_hand_list, dealer_hand_list, dealer_hand_sprites):
        result = ""
        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.left + self.rect.w:
            if pos[1] > self.rect.top and pos[1] < self.rect.top + self.rect.h:
                if click == 1:
                    dealer_hand_sprites = dealer_hand_sprites.flip_dealer_card()
                    pre_hit_len = len(dealer_hand_list)
                    deck, dealer_hand_list, dealer_hit_flag = dealer_hit(deck,dealer_hand_list)
                    for card in range(pre_hit_len,len(dealer_hand_list)):
                        dealer_hand_sprites.card_add(dealer_hand_list[card])
                    if dealer_hit_flag == 0:
                        result = stay_score(player_hand_list, dealer_hand_list)
                    else:
                        result = "dealer_bust"
                    #print("stay button clicked")
                    play_cardplace2()
                    
                    click = 0

        return click, result, player_hand_list, dealer_hand_list, dealer_hand_sprites

    def draw(self, surface):
        surface.blit(self.button, self.rect)


class BetUpButton(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        path = resources_path + r"graphics\right_arrow.png"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (128, 128))
        self.image = image
        self.rect = image.get_rect(left=250, centery=(size[1] / 2 + size[1] / 3 + 45))

    def update(self, click, bet, funds):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.left + self.rect.w:
            if pos[1] > self.rect.top and pos[1] < self.rect.top + self.rect.h:
                if click == 1:
                    if bet < funds:
                        bet += 5
                        play_click()
                    #click = 0
                    time.sleep(0.11)
        return click, bet, funds

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BetDownButton(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        path = resources_path + r"graphics\left_arrow.png"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (128, 128))
        self.image = image
        self.rect = image.get_rect(left=1, centery=(size[1] / 2 + size[1] / 3 + 45))


    def update(self, click, bet, funds):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.left + self.rect.w:
            if pos[1] > self.rect.top and pos[1] < self.rect.top + self.rect.h:
                if click == 1:
                    if bet > 5:
                        bet -= 5
                        play_click()
                    #click = 0
                    time.sleep(0.11)
        return click, bet, funds

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BetDisplay(pygame.sprite.Sprite):
    def __init__(self, bet, funds):
        pygame.sprite.Sprite.__init__(self)
        self.font = "card"
        self.font_size = 24
        self.color = (0, 0, 0)
        self.size = (200, 100)
        self.position = (90, 590)
        self.rect_funds = pygame.Rect(*self.position, *self.size)
        self.rect_bet = pygame.Rect(self.position[0], self.position[1] + self.font_size, *self.size)
        self.text_funds, self.text_bet = self.generateText(bet, funds)

    def generateText(self, bet, funds):
        fontpath = resources_path + r"fonts\{}.ttf".format(self.font)
        font = pygame.font.Font(fontpath, self.font_size)
        text_funds = font.render("funds: ${}".format(funds), 1, self.color)
        text_bet = font.render("bet: ${}".format(bet), 1, self.color)
        return text_funds, text_bet

    def update(self, bet, funds):
        self.text_funds, self.text_bet = self.generateText(bet, funds)

    def draw(self, surface):
        surface.blit(self.text_funds, self.rect_funds)
        surface.blit(self.text_bet, self.rect_bet)

class GeneralDisplay(pygame.sprite.Sprite):
    def __init__(self, line1, line2 = ""):
        pygame.sprite.Sprite.__init__(self)
        self.text_line1 = line1
        self.text_line2 = line2
        self.font = "card"
        self.font_size = 28
        self.color = (0, 0, 0)
        self.size = (200, 100)
        self.position = (35, 400)
        self.line1_rect = pygame.Rect(*self.position, *self.size)
        self.line2_rect = pygame.Rect(self.position[0], self.position[1] + self.font_size, *self.size)
        self.line1, self.line2  = self.generateText(self.text_line1, self.text_line2)
        

    def generateText(self, text_line1, text_line2 = ""):
        self.text = text_line1 + text_line2
        #print("General Display Set To", self.text)

        fontpath = resources_path + r"fonts\{}.ttf".format(self.font)
        font = pygame.font.Font(fontpath, self.font_size)
        line1 = font.render(text_line1, 1, self.color)
        line2 = font.render(text_line2, 1, self.color)
        return line1, line2

    def update(self, text_line1, text_line2 = ""):
        self.line1, self.line2  = self.generateText(text_line1, text_line2 = text_line2)

    def draw(self, surface):
        surface.blit(self.line1, self.line1_rect)
        surface.blit(self.line2, self.line2_rect)

class CardGroup(pygame.sprite.Group):

    def __init__(self, start_pos, dealer = False):
        pygame.sprite.Group.__init__(self)
        self.size = 0
        self.dealer = dealer
        self.cardOffset = 40
        self.position = start_pos
        self.dealer_back_card = ""
        self.back_card = deck_back(position = self.position)

    def card_add(self,card):
        if not self.dealer:
            x_position = self.position[0] + (self.size * self.cardOffset)
            sprite = card_sprite(card, (x_position, self.position[1]))
            self.add(sprite)
            self.size += 1 
        if self.dealer:
            if self.size == 0:
                self.dealer_back_card = card
                self.add(self.back_card)
                self.size += 1 
            else:
                x_position = self.position[0] + (self.size * self.cardOffset)
                sprite = card_sprite(card, (x_position, self.position[1]))
                self.add(sprite)
                self.size += 1 
    
    def flip_dealer_card(self):
        if self.dealer and self.dealer_back_card != "":
            x_position = self.position[0] + (self.size * self.cardOffset)
            self.remove(self.back_card)
            sprite =  card_sprite(self.dealer_back_card, self.position)
            flipped = CardGroup((self.position))
            flipped.add(sprite)
            flipped.size += 1
            for sprites in self:
                flipped.add(sprites) 
                flipped.size += 1
            self.add(sprite)
            return flipped
        else:
            return self



def initialize_shuffle_deck():
    deck = []

    card_values_png = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    card_suits_png = ['C', 'S', 'D', 'H']

    for i in card_values_png:
        for j in card_suits_png:
            card = [i, j]
            deck.append(card)

    random.shuffle(deck)

    return deck


def deal(deck):
    player_hand = []
    dealer_hand = []

    cardcount = 4

    while cardcount>0:
        if cardcount % 2 ==0:
            card = deck.pop()
            player_hand.append(card)
        else:
            card = deck.pop()
            dealer_hand.append(card)
        cardcount -= 1

    return deck, player_hand, dealer_hand

def hit(deck, hand):

    flag = 0

    card = deck.pop()
    hand.append(card)

    if total(hand) > 21:
        flag = 1
        return deck, hand, flag

    return deck, hand, flag

def dealer_hit(deck, hand):
    flag = 0

    while total(hand) < 17:
        card = deck.pop()
        hand.append(card)

    if total(hand) > 21:
        #print("Dealer Bust")
        flag = 1
        return deck, hand, flag

    return deck, hand, flag

def total(hand):
    total = 0
    for card in hand:
        if card[0] == 'J' or card[0] == 'Q' or card[0] == 'K':
            total += 10
        elif card[0] == 'A':
            total += 11
        else:
            total += int(card[0])

    if total > 21:
        for card in hand:
            if card[0] == 'A':
                total -= 10
            if total <= 21:
                break
            else:
                continue
    return total

def blackjack_check(player_hand_list, dealer_hand_list):
    player_blackjack_flag = 0
    dealer_blackjack_flag = 0
    if len(player_hand_list) == 2 and total(player_hand_list) == 21:
        player_blackjack_flag = 1
    if len(dealer_hand_list) == 2 and total(dealer_hand_list) == 21:
        dealer_blackjack_flag = 1
    if dealer_blackjack_flag == 1 and player_blackjack_flag == 1:
        return "push"
    elif dealer_blackjack_flag == 1:
        return "dealer_win"
    elif player_blackjack_flag == 1:
        return "player_blackjack"
    else:
        return "none"
    
def stay_score(player_hand_list, dealer_hand_list):
    if total(player_hand_list) == total(dealer_hand_list):
        return "push"
    elif total(player_hand_list) > total(dealer_hand_list):
        #print("Player won without blackjack!")
        return "player_win"
    elif total(player_hand_list) < total(dealer_hand_list):
        #print("Dealer won without blackjack!")
        return "dealer_win"

class BlackJackScreen(Scene):
    name = "blackjack"

    def __init__(self):
        super().__init__()
        self.background_color = (0, 0, 0)
        self.deal_button = deal_button(deal_button_color, deal_button_rect, button_text_color, "card", 40, "Deal")
        self.hit_button = hit_button(hit_button_color, hit_button_rect, button_text_color, "card", 40, "Hit")
        self.stay_button = stay_button(stay_button_color, stay_button_rect, button_text_color, "card", 40, "Stay")
        self.deck_back = deck_back()
        self.betup_button = BetUpButton()
        self.betdown_button = BetDownButton()
        self.player_hand_sprites = CardGroup((300,300))
        self.dealer_hand_sprites = CardGroup((50,50), dealer = True)
        self.general_text = "Press Deal To Play"
        self.general_display = GeneralDisplay(self.general_text)
        self.round_start = False 
        self.bet = 20
        self.funds = 500
        self.deck = None
        self.player_hand_list = None
        self.dealer_hand_list = None
        self.hit_flag = 0
        self.result = ""
        self.bet_display = BetDisplay(self.bet, self.funds)
        self.click = None
        play_cardfan()

    def round_reset(self):
        self.round_start = False
        self.player_hand_list = None 
        self.dealer_hand_list = None 
        self.deck = None 
        self.result = ""
        self.hit_flag = 0

    def get_event(self, event):
        self.click = 0
        if event.type == pygame.QUIT:
            self.finished = True
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_F4:
                self.finished = True
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = 1
        elif event.type ==  pygame.MOUSEBUTTONUP:
            self.click = 0

    def update(self, surface, keys, tick):
        if self.funds == 0:
            self.general_display.update("GAMEOVER!", "RELAUNCH TO REPLAY")

        if not self.round_start:
            self.click, self.bet, self.funds = self.betup_button.update(self.click, self.bet, self.funds)
            self.click, self.bet, self.funds = self.betdown_button.update(self.click, self.bet, self.funds)
        self.bet_display.update(self.bet, self.funds)
        if not self.round_start:
            self.click, self.funds, self.bet, self.deck, self.player_hand_list, self.dealer_hand_list, self.player_hand_sprites, self.dealer_hand_sprites, self.general_display = self.deal_button.update(self.click, self.funds, self.bet, self.deck, self.player_hand_list, self.dealer_hand_list, self.player_hand_sprites, self.dealer_hand_sprites, self.general_display )
        if self.player_hand_list != None:
            self.general_display.update("HIT OR STAND","TO PROCEED")
            self.round_start = True
        else:
            self.round_reset()
        if self.round_start:
            self.click, self.deck, self.player_hand_list, self.hit_flag = self.hit_button.update(self.click, self.deck, self.player_hand_list,self.player_hand_sprites)
        if self.player_hand_list != None:
            if self.hit_flag == 0 and total(self.player_hand_list) == 21:
                    self.dealer_hand_sprites =  self.dealer_hand_sprites.flip_dealer_card()
                    #print("PLAYER WON ${} FROM 21".format(self.bet *2))
                    self.general_display.update("PLAYER WON ","${} FROM 21!".format(2*self.bet))
                    self.funds += (2 *self.bet)
                    self.round_reset()
        if self.hit_flag == 1:
            self.dealer_hand_sprites =  self.dealer_hand_sprites.flip_dealer_card()
            self.general_display.update("PLAYER BUST!","LOST ${} ON HIT".format(self.bet))
            self.round_reset()
        if self.hit_flag == 0 and self.round_start:
            self.click, self.result, self.player_hand_list, self.dealer_hand_list, self.dealer_hand_sprites = self.stay_button.update(self.click, self.deck, self.player_hand_list, self.dealer_hand_list, self.dealer_hand_sprites)
            if self.result == "push":
                self.general_display.update("PUSH!","${} RETURNED".format(self.bet))
                self.dealer_hand_sprites =  self.dealer_hand_sprites.flip_dealer_card()
                self.funds += self.bet
                self.round_reset()
            elif self.result == "player_win":
                self.general_display.update("PLAYER WON ${}!".format(self.bet * 2))
                self.dealer_hand_sprites =  self.dealer_hand_sprites.flip_dealer_card()
                self.funds += (2 * self.bet) 
                self.round_reset()
            elif self.result == "dealer_win":
                self.general_display.update("DEALER WON!","PLAYER LOST ${}".format(self.bet))
                self.dealer_hand_sprites =  self.dealer_hand_sprites.flip_dealer_card()
                self.round_reset()
            elif self.result == "dealer_bust":
                self.general_display.update("PLAYER WON ${}!".format(self.bet * 2),"DEALER BUST!")
                self.dealer_hand_sprites =  self.dealer_hand_sprites.flip_dealer_card()
                self.funds += (2 * self.bet) 
                self.round_reset()
                
            # self.deck, self.dealer_hand_list, self.dealer_hit_flag = dealer_hit(self.deck,self.dealer_hand_list)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(black)
        surface.blit(background_felt, (0, 0))
        if not self.round_start:
            self.deal_button.draw(surface)
        if self.round_start:
            self.hit_button.draw(surface)
            self.stay_button.draw(surface)
        self.deck_back.draw(surface)
        self.betup_button.draw(surface)
        self.betdown_button.draw(surface)
        self.bet_display.draw(surface)
        self.player_hand_sprites.draw(surface)
        self.dealer_hand_sprites.draw(surface)
        self.general_display.draw(surface)