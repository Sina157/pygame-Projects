import pygame
import random
import DBUI as DB

colors = {"Green": (0, 255, 0), "Black": (0, 0, 0), "White": (255, 255, 255),
          "Blue": (0, 0, 255), "Red": (255, 0, 0), "LightBlue": (0, 255, 255),
          "Yellow": (255, 255, 0), "Pink": (255, 0, 255), "Gray": (128, 128, 128),
          "Purple": (125, 0, 255), "DarkPurple": (50, 0, 103), "DarkGreen": (0, 64, 0),
          "DarkRed": (64, 0, 0), "DarkBlue": (0, 0, 64), "Silver": (190, 190, 190)}
pygame.init()
GameRunning = True
clock = pygame.time.Clock()
GameWindow = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Snake")
Player = {"Pos": [275, 225], "NormalSpeed": 15, "Speed": 15, "MoveDir": None,
          "Size": 25, "Color": colors["Green"], "EatenFood": 0, "Score": 0}
PlayerTrail = []
objects = []
pygame.mixer.music.load("./sounds/notification.wav")
isGameOver = False
isSnakeMoved = True
isGamePaused = False
GameFont = pygame.font.Font(None, 20)


# Game Core and Display OperatorS
def Update():
    global PlayerTrail, isSnakeMoved
    HeadPosFix = [0, 0]
    PlayerTrail = PlayerTrail[-Player["EatenFood"]:]
    GameWindow.fill(colors["Black"])
    label1 = GameFont.render(
        "Score: "+str(Player["Score"]), True, colors["LightBlue"])
    GameWindow.blit(label1, (0, 0))
    if isSnakeMoved:
        if Player["MoveDir"] == "Down":
            HeadPosFix = [0, 10]
        elif Player["MoveDir"] == "Up":
            HeadPosFix = [0, -10]
        elif Player["MoveDir"] == "Left":
            HeadPosFix = [-10, 0]
        elif Player["MoveDir"] == "Right":
            HeadPosFix = [10, 0]
    for item in PlayerTrail:
        pygame.draw.rect(GameWindow, Player["Color"], [
            item[0], item[1], Player["Size"], Player["Size"]])
    if Player["MoveDir"] != None and Player["EatenFood"] != 0 and not isGamePaused:
        PlayerTrail.append((Player["Pos"][0], Player["Pos"][1]))
    PlayerHead = pygame.draw.rect(GameWindow, colors["Blue"], [
        Player["Pos"][0] + HeadPosFix[0], Player["Pos"][1] + HeadPosFix[1], Player["Size"], Player["Size"]])
    pygame.draw.circle(
        GameWindow, colors["LightBlue"], GetPlayerEyesPos(PlayerHead.center), 4)
    for item in objects:
        pygame.draw.rect(GameWindow, colors["Yellow"], [
            item[0], item[1], 25, 25])
    isSnakeMoved = True
    PlayerControls()
    GameOperator()
    if isGameOver:
        GameOverLable = pygame.font.Font(None, 100).render(
            "Game Over", True, colors["Red"])
        GameOverLable2 = pygame.font.Font(None, 40).render(
            "Press r to restart and s to submit record", True, colors["Red"])
        GameWindow.blit(GameOverLable, (115, 180))
        GameWindow.blit(GameOverLable2, (40, 270))
    if isGamePaused:
        Lable3 = pygame.font.Font(None, 100).render(
            "Game Paused", True, colors["Yellow"])
        GameWindow.blit(Lable3, (70, 200))
    pygame.display.update()


def GetPlayerEyesPos(PlayerHeadCenterPos):
    if Player["MoveDir"] == "Up":
        return (PlayerHeadCenterPos[0], PlayerHeadCenterPos[1] - 7)
    elif Player["MoveDir"] == "Down":
        return (PlayerHeadCenterPos[0], PlayerHeadCenterPos[1] + 7)
    elif Player["MoveDir"] == "Right":
        return (PlayerHeadCenterPos[0] + 7, PlayerHeadCenterPos[1])
    elif Player["MoveDir"] == "Left":
        return (PlayerHeadCenterPos[0] - 7, PlayerHeadCenterPos[1])
    else:
        return (PlayerHeadCenterPos[0] - 7, PlayerHeadCenterPos[1])


def CheckCollision(firstPos, secondPos, firstSize=[25, 25], SecondSize=[25, 25]):
    # checks pos x
    if any(item in range(firstPos[0], firstPos[0] + firstSize[0]) for item in range(secondPos[0], secondPos[0] + SecondSize[0])):
        # checks pos y
        if any(item in range(firstPos[1], firstPos[1] + firstSize[1]) for item in range(secondPos[1], secondPos[1] + SecondSize[1])):
            return True
    else:
        return False


def CheckFoodCollisionWithObjects(pos):
    for item in PlayerTrail:
        if CheckCollision(pos, item):
            return True


def GameOperator():
    global Player, objects, isGameOver
    if objects == []:
        x = random.randint(0, GameWindow.get_size()[0] - 25)
        y = random.randint(0, GameWindow.get_size()[1] - 25)
        while CheckFoodCollisionWithObjects((x, y)):
            x = random.randint(0, GameWindow.get_size()[0] - 25)
            y = random.randint(0, GameWindow.get_size()[1] - 25)
        objects.append([x, y, "food"])
    for item in objects:
        if CheckCollision((item[0], item[1]), Player["Pos"]):
            objects.pop()
            Player["EatenFood"] += 2
            Player["Score"] += 1
            pygame.mixer.music.play()

    if Player["MoveDir"] == "Right":
        Player["Pos"][0] += Player["Speed"]
    elif Player["MoveDir"] == "Left":
        Player["Pos"][0] -= Player["Speed"]
    elif Player["MoveDir"] == "Up":
        Player["Pos"][1] -= Player["Speed"]
    elif Player["MoveDir"] == "Down":
        Player["Pos"][1] += Player["Speed"]
    # Right Check
    if Player["Pos"][0] > GameWindow.get_size()[0] - Player["Size"]:
        Player["Pos"][0] = 0
    # Left Check
    if Player["Pos"][0] < 0:
        Player["Pos"][0] = GameWindow.get_size()[0] - Player["Size"]
    # Top Check
    if Player["Pos"][1] < 0:
        Player["Pos"][1] = GameWindow.get_size()[1] - Player["Size"]
    # Down Check
    if Player["Pos"][1] > GameWindow.get_size()[1] - Player["Size"]:
        Player["Pos"][1] = 0
    for item in PlayerTrail[:-5]:
        if CheckCollision(Player["Pos"], item) and not isGameOver:
            Player["Speed"] = 0
            isGameOver = True
            GameOver()
    if not isGameOver and not isGamePaused:
        Player["Speed"] = Player["NormalSpeed"]


def GameOver():
    Update()
    Player["Speed"] = 0
    Player["MoveDir"] = None


def PlayerControls():
    global Player, GameRunning, isSnakeMoved, isGamePaused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == pygame.KEYDOWN and not isGameOver and isSnakeMoved:
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and Player["MoveDir"] not in ["Left", "Right"]:
                Player["MoveDir"] = "Right"
                Player["Speed"] = Player["Size"]
                isSnakeMoved = False
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and Player["MoveDir"] not in ["Left", "Right"]:
                Player["MoveDir"] = "Left"
                Player["Speed"] = Player["Size"]
                isSnakeMoved = False
            elif (event.key == pygame.K_w or event.key == pygame.K_UP) and Player["MoveDir"] not in ["Down", "Up"]:
                Player["MoveDir"] = "Up"
                Player["Speed"] = Player["Size"]
                isSnakeMoved = False
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and Player["MoveDir"] not in ["Down", "Up"]:
                Player["MoveDir"] = "Down"
                Player["Speed"] = Player["Size"]
                isSnakeMoved = False
            if event.key == pygame.K_SPACE and not isGamePaused:
                Player["Speed"] = 0
                isGamePaused = True
            else:
                isGamePaused = False
        if isGameOver and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Restart()
            if event.key == pygame.K_s:
                DB.Submit(Player["Score"])
                Restart()


def Restart():
    global isGameOver, objects, PlayerTrail
    isGameOver = False
    Player["Score"] = 0
    Player["EatenFood"] = 0
    Player["Pos"] = [275, 225]
    objects = []
    PlayerTrail = []


while GameRunning:
    clock.tick(15)
    Update()
