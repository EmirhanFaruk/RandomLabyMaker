import pygame
from random import choice


pygame.init()
win_width, win_height = 800, 800
win = pygame.display.set_mode((win_width, win_height))

class Cellule:
    def __init__(self, x, y, width, height, murNord, murEst, murSud, murOuest):
        self.murs = {"N": murNord, "E": murEst,
                    "S": murSud, "O": murOuest}
        self.voisins = {"N": None, "E": None,
                        "S": None, "O": None,
                        "NE": None, "NO": None,
                        "SE": None, "SO": None}
        self.x, self.y, self.width, self.height = x, y, width, height
    def draw(self, win):
        if self.murs["N"]:
            pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x + self.width, self.y))
        if self.murs["S"]:
            pygame.draw.line(win, (0, 0, 0), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height))
        if self.murs["E"]:
            pygame.draw.line(win, (0, 0, 0), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height))
        if self.murs["O"]:
            pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.height))
        


class Labyrinthe:
    def __init__(self, x, y, width, height, hauteur, longueur):
        self.x, self.y, self.width, self.height, self.hauteur, self.longueur = x, y, width, height, hauteur, longueur
        self.grille = self.construire_grille(x, y, width, height, hauteur, longueur)
        
    def construire_grille(self, x, y, width, height, hauteur, longueur):
        grille = []
        for i in range(hauteur):
            ligne = []
            for j in range(longueur):
                cellule = Cellule(y + i * width, x + j * height, width, height, True, True, True, True)
                ligne.append(cellule)
            grille.append(ligne)
        return grille

    def creer_passage(self, c1_lig, c1_col, c2_lig, c2_col):
        #print(self.grille)
        cellule1 = self.grille[c1_lig][c1_col]
        cellule2 = self.grille[c2_lig][c2_col]
        #cellule2 au Nord de cellule1
        if c1_lig - c2_lig == 1 and c1_col == c2_col:
            cellule1.murs["N"] = False
            cellule2.murs["S"] = False
        #cellule2 à l'Ouest de cellule1
        elif c1_lig == c2_lig and c1_col - c2_col == 1:
            cellule1.murs["O"] = False
            cellule2.murs["E"] = False
        #cellule2 au Sud de cellule1
        elif c1_lig - c2_lig == -1 and c1_col == c2_col:
            cellule1.murs["S"] = False
            cellule2.murs["N"] = False
        #cellule2 à l'Est de cellule1
        elif c1_lig == c2_lig and c1_col - c2_col == -1:
            cellule1.murs["E"] = False
            cellule2.murs["O"] = False

    def draw(self, win):
        for sıra in range(self.hauteur):
            for sütun in range(self.longueur):
                self.grille[sıra][sütun].draw(win)
        #pygame.draw.line(win, colour, (x, y), (x2, y2))

    def creer_labyrinthe(self, ligne, colonne):
        if ligne < 1:# and colonne < 1:
            return
        dal = []
        for j in lab.grille[ligne][colonne].murs:
            if j:
                dal.append(j)
        dac = choice(dal)
        if dac == "N":
            self.creer_passage(ligne, colonne, ligne - 1, colonne)
        elif dac == "S":
            self.creer_passage(ligne, colonne, ligne + 1, colonne)
        elif dac == "E":
            self.creer_passage(ligne, colonne, ligne, colonne + 1)
        elif dac == "O":
            self.creer_passage(ligne, colonne, ligne , colonne - 1)
        #print(ligne, colonne)
        if colonne <= 1:
            return self.creer_labyrinthe(ligne - 1, self.longueur - 2)
        else:
            return self.creer_labyrinthe(ligne, colonne - 1)



lab = Labyrinthe(100, 100, 50, 50, 12, 12)
lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)





class Text:
    def __init__(self, x, y, text, size, colour, variable = ""):
        self.x, self.y, self.size, self.colour = x, y, size, colour
        self.text = text
        self.variable = variable
        self.font = pygame.font.SysFont('Comic Sans MS', self.size)
        self.text_surface = self.font.render(self.text, False, self.colour)
        self.text_width = self.text_surface.get_width()

    def draw(self, win):
        self.text_surface = self.font.render(self.text + str(self.variable), False, self.colour)
        self.text_width = self.text_surface.get_width()
        win.blit(self.text_surface, (self.x - self.text_width/2, self.y))
        return

class Node:
    def __init__(self, x, y, w, h, number):
        self.x, self.y, self.w, self.h, self.number = x, y, w, h, number
        self.start = False
        self.finish = False
        self.closed = False
        self.opened = False
        self.route = {}
        self.neighbors = {0: ["NW", None], 1: ["N", None], 2: ["NE", None], 3: ["W", None], 4: ["E", None], 5: ["SW", None], 6: ["S", None], 7: ["SE", None]}
        self.text = Text(self.x + self.w/2, self.y + self.h/3, str(self.number), 10, (50, 70, 160))

    def get_neighbors(self, nodes):
        da_n = [(self.number - 11), (self.number - 10), (self.number - 9), (self.number - 1), (self.number + 1), (self.number + 9), (self.number + 10), (self.number + 11)]
        for key, value in nodes.items():
            for index, element in enumerate(da_n):
                if element == key:
                    self.neighbors[index][1] = value
    def get_costs(self, start, finish):
        return

    def draw(self, win):
        pygame.draw.rect(win, (50, 170, 90), pygame.Rect(self.x, self.y, self.w, self.h))
        self.text.draw(win)
        for key, node in self.neighbors.items():
            """
            try:
                print(self.number, key, node[1].number)
            except:
                print(self.number, key, node[1])
            """
            if node[1] != None:
                if node[0] == "NW":
                    pygame.draw.circle(win, (255, 255, 0), (self.x + self.w / 4, self.y + self.h / 4), 3)
                if node[0] == "N":
                    pygame.draw.circle(win, (255, 255, 0), (self.x + self.w / 2, self.y + self.h / 4), 3)
                if node[0] == "NE":
                    pygame.draw.circle(win, (255, 255, 0), ((self.x + (self.w * 3) / 4), self.y + self.h / 4), 3)
                if node[0] == "W":
                    pygame.draw.circle(win, (255, 255, 0), (self.x + self.w / 4, self.y + self.h / 2), 3)
                if node[0] == "E":
                    pygame.draw.circle(win, (255, 255, 0), ((self.x + (self.w * 3) / 4), self.y + self.h / 2), 3)
                if node[0] == "SW":
                    pygame.draw.circle(win, (255, 255, 0), (self.x + self.w / 4, self.y + (self.h * 3) / 4), 3)
                if node[0] == "S":
                    pygame.draw.circle(win, (255, 255, 0), (self.x + self.w / 2, self.y + (self.h * 3) / 4), 3)
                if node[0] == "SE":
                    pygame.draw.circle(win, (255, 255, 0), (self.x + (self.w * 3) / 4, self.y + (self.h * 3) / 4), 3)
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x + self.w, self.y), 1)
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.h), 1)
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 1)
        pygame.draw.line(win, (0, 0, 0), (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), 1)



nodes = {}
for i in range(10):
    for j in range(1, 11):
        nodes[i * 10 + j] = Node(50 + 50 * (j - 1), 50 + 50 * i, 50, 50, i * 10 + j)
nodes[1].start = True
nodes[100].finish = True
nodes[1].opened = True
for node in nodes.values():
    node.get_neighbors(nodes)
for node in nodes.values():
    node.get_neighbors(nodes)


for node in nodes.values():
    print("---------------------------------------------")
    for key, value in node.neighbors.items():
        try:
            print(node.number, value[0], value[1].number)
        except Exception as e:
            print(node.number, value[0], "None", e)




clock = pygame.time.Clock()
fps = 30
running = True
while running:
    clock.tick(30)
    win.fill((20, 150, 70))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lab = Labyrinthe(100, 100, 50, 50, 12, 12)
                lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
                lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
                lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
            if event.key == pygame.K_RETURN:
                continue
    #lab = Labyrinthe(100, 100, 50, 50, 12, 12)
    #lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
    #lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
    #lab.creer_labyrinthe(lab.hauteur - 2, lab.longueur - 2)
    lab.draw(win)
    pygame.display.flip()
