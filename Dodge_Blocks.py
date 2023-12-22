import pygame
import random
import DBUI as DB


colors = {"Green": (0, 255, 0), "Black": (0, 0, 0), "White": (255, 255, 255),
          "Blue": (0, 0, 255), "Red": (255, 0, 0), "LightBlue": (0, 255, 255),
          "Yellow": (255, 255, 0), "Pink": (255, 0, 255), "Gray": (128, 128, 128),
          "Purple": (125, 0, 255), "DarkPurple": (50, 0, 103), "DarkGreen": (0, 64, 0),
          "DarkRed": (64, 0, 0), "DarkBlue": (0, 0, 64), "Silver": (190, 190, 190)}
pygame.init()
pygame.mixer.music.load("./sounds/notification.wav")
Score = 0
isGameOver = False
GameRunning = True
clock = pygame.time.Clock()
GameWindow = pygame.display.set_mode((600, 500))


PlayerPos = [250, 450]
enemiesPos = []
PlayerMoveSpeed = 15
EnemiesMoveSpeed = 10
Level = 1
StopTime = 0
WastedTime = 0
isSumbmit = False
r = random.randint(0, 550)
enemiesPos.append([r, 0])


def CheckCollision(firstPos, secondPos, firstSize=[50, 50], SecondSize=[50, 50]):
    # checks pos x
    if any(item in range(firstPos[0], firstPos[0] + firstSize[0]) for item in range(secondPos[0], secondPos[0] + SecondSize[0])):
        # checks pos y
        if any(item in range(firstPos[1], firstPos[1] + firstSize[1]) for item in range(secondPos[1], secondPos[1] + SecondSize[1])):
            return True
    else:
        return False


def EnemiesAct():
    global Score, EnemiesMoveSpeed, isGameOver
    for enemyPos in enemiesPos:
        enemyPos[1] += EnemiesMoveSpeed
        if enemyPos[1] >= 500:
            Score += 1
            enemyPos[1] = random.randint(-500, -50)
            enemyPos[0] = random.randint(0, 550)
            pygame.mixer.music.play()
        pygame.draw.rect(GameWindow, colors["Red"], [
                         enemyPos[0], enemyPos[1], 50, 50])
        if CheckCollision(PlayerPos, enemyPos):
            isGameOver = True
            pygame.mixer.music.load("./sounds/Gameover2.ogg")
            pygame.mixer.music.play()
            GameOver()


def CheckForLevels():
    global Level, EnemiesMoveSpeed
    if StopTime == 0:
        if int(pygame.time.get_ticks()/1000) - WastedTime > 3 and Level == 1:
            for i in range(2):
                y = random.randint(-500, -50)
                x = random.randint(0, 550)
                enemiesPos.append([x, y])
            Level = 2
        elif int(pygame.time.get_ticks()/1000) - WastedTime > 10 and Level == 2:
            for i in range(3):
                y = random.randint(-500, -50)
                x = random.randint(0, 550)
                enemiesPos.append([x, y])
            Level = 3
        elif int(pygame.time.get_ticks()/1000) - WastedTime > 20 and Level == 3:
            for i in range(3):
                y = random.randint(-500, -50)
                x = random.randint(0, 550)
                enemiesPos.append([x, y])
                EnemiesMoveSpeed += 1
            Level = 4
        elif int(pygame.time.get_ticks()/1000) - WastedTime > 35 and Level == 4:
            for i in range(5):
                y = random.randint(-500, -50)
                x = random.randint(0, 550)
                enemiesPos.append([x, y])
            Level = 5


def PlayerControls():
    global GameRunning, PlayerMoveSpeed, EnemiesMoveSpeed, WastedTime, StopTime
    KeysPressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and PlayerMoveSpeed != 0:
                PlayerMoveSpeed = 0
                EnemiesMoveSpeed = 0
                StopTime = int(pygame.time.get_ticks())
            elif event.key == pygame.K_SPACE and PlayerMoveSpeed == 0:
                PlayerMoveSpeed = 15
                WastedTime += (int(pygame.time.get_ticks()) - StopTime) / 1000
                StopTime = 0
    if KeysPressed[pygame.K_d] or KeysPressed[pygame.K_RIGHT]:
        PlayerPos[0] += PlayerMoveSpeed
    if KeysPressed[pygame.K_a] or KeysPressed[pygame.K_LEFT]:
        PlayerPos[0] -= PlayerMoveSpeed
    if PlayerPos[0] > 550:
        PlayerPos[0] = 550
    if PlayerPos[0] < 0:
        PlayerPos[0] = 0


def Update():
    global PlayerPos, Score
    GameWindow.fill(colors["Black"])
    if StopTime != 0:
        StopLabel = pygame.font.Font(None, 100).render(
            "Paused", True, colors["Yellow"])
        GameWindow.blit(StopLabel, (175, 200))
    ScoreLabel = pygame.font.Font(None, 20).render(
        "Score: "+str(Score), True, colors["LightBlue"])
    GameWindow.blit(ScoreLabel, (0, 0))
    pygame.draw.rect(GameWindow, colors["Green"], PlayerPos+[50, 50])
    PlayerControls() # allow player to move
    EnemiesAct() # moves enemies and checks collision
    CheckForLevels() # make the game harder over time
    pygame.display.update()


# checks for game over
def GameOver():
    global isSumbmit, Score, isGameOver, GameRunning, PlayerPos, enemiesPos, PlayerMoveSpeed, EnemiesMoveSpeed, Level, StopTime, WastedTime
    EnemiesMoveSpeed = 0
    PlayerMoveSpeed = 0
    GameWindow.fill(colors["DarkRed"])
    GameOveLable1 = pygame.font.Font(None, 50).render(
        "Your Score Was: "+str(Score), True, colors["White"])
    GameOveLable2 = pygame.font.Font(None, 100).render(
        "Game Over", True, colors["White"])
    GameOveLable3 = pygame.font.Font(None, 50).render(
        "Press r to restart", True, colors["White"])
    GameOveLable4 = pygame.font.Font(None, 50).render(
        "Press s to submit record", True, colors["White"])
    RecordsLabel = pygame.font.Font(None, 25).render(
        "records", True, colors["LightBlue"])
    GameWindow.blit(RecordsLabel, (0, 0))
    GameWindow.blit(GameOveLable1, (150, 210))
    GameWindow.blit(GameOveLable2, (120, 110))
    GameWindow.blit(GameOveLable3, (160, 280))
    GameWindow.blit(GameOveLable4, (100, 340))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if CheckCollision(event.pos, (0, 0), (1, 1), RecordsLabel.get_size()):
                DB.ShowRecords()
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                enemiesPos = []
                pygame.mixer.music.load("./sounds/Space/notification.wav")
                Score = 0
                isGameOver = False
                GameRunning = True
                isSumbmit = False
                PlayerPos = [250, 450]
                enemiesPos = []
                PlayerMoveSpeed = 15
                EnemiesMoveSpeed = 10
                Level = 1
                StopTime = 0
                WastedTime = int(pygame.time.get_ticks()) / 1000
                r = random.randint(0, 550)
                enemiesPos.append([r, 0])
            if event.key == pygame.K_s and isSumbmit == False:
                if DB.Submit(Score):
                    isSumbmit = True
    pygame.display.update()


while GameRunning:
    clock.tick(30)
    if isGameOver:
        GameOver()
    else:
        Update()
