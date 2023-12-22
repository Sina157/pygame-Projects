import pygame
import random
# add screenshot and disable
colors = {"Green": (0, 255, 0), "Black": (0, 0, 0), "White": (255, 255, 255),
          "Blue": (0, 0, 255), "Red": (255, 0, 0), "LightBlue": (0, 255, 255),
          "Yellow": (255, 255, 0), "Pink": (255, 0, 255), "Gray": (128, 128, 128),
          "Purple": (125, 0, 255), "DarkPurple": (50, 0, 103), "DarkGreen": (0, 64, 0),
          "DarkRed": (64, 0, 0), "DarkBlue": (0, 0, 64), "Silver": (190, 190, 190)}
pygame.init()
GameRunning = True
clock = pygame.time.Clock()
GameWindow = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Draw")
Lineslist = []


def Update():
    global GameRunning
    GameWindow.fill(colors["Black"])
    IsSPress = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                IsSPress = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(Lineslist) == 0:
                    Lineslist.append(event.pos)
                Lineslist.append(event.pos)
            elif event.button == 3 and len(Lineslist) > 0:
                Lineslist.pop()
        if event.type == pygame.MOUSEMOTION and len(Lineslist) >= 2:
            Lineslist[-1] = event.pos
    if len(Lineslist) >= 2:
        pygame.draw.lines(
            GameWindow, colors["LightBlue"], True, (Lineslist), 5)
    if IsSPress:
            pygame.display.update()
            pygame.image.save(GameWindow, f"screenshot{random.randint(0,100000)}.jpg")
    else:
        label1 = pygame.font.Font(None, 20).render(
          "Press s to save image", True, colors["LightBlue"])
        GameWindow.blit(label1, (0, 0))
        pygame.display.update()

   


while GameRunning:
    clock.tick(30)
    Update()
