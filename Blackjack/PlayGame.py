import pygame
from controller import Controller


caption = "Our Blackjack Game"

#PLEASE CHANGE THIS RESOURCES PATH TO WHEREEVER THE FINAL PROJECT IS STORED ON YOUR MACHINE
#YOU NEED TO INCLUDE 2 \\'s AT THE END AS THE LAST ONE IS PERCEIVED AS EOL (END OF LINE)
resources_path = r"C:\Users\user\Desktop\SFU\CMPT 365\Final Project\Blackjack\resources\\"

music_path = resources_path + r"music\FATS WALLER & HIS RHYTHM - BUCKIN' THE DICE.ogg"
size = (928, 696)
win_pos = (0, 0)
names = { "title_screen" : "TitleScreen",
    "blackjack" : "BlackJackScreen",
}

pygame.init()
pygame.mixer.init()
pygame.display.set_caption(caption)
pygame.display.set_mode(size)
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(.08)
pygame.mixer.music.play()
main_controller = Controller(size, names)
main_controller.set_scene("title_screen")
main_controller.mainloop()
pygame.quit()
