# suppress pygame welcome message
import os, contextlib
with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    import pygame

import core.graphics.sprites as sprites


# ----------- COLORS -------------
COL_BCK = (0, 0, 0)
COL_GRD = (255, 255, 255)
COL_PL1 = (250, 100, 40)
COL_PL2 = (40, 200, 100)


# --------- DIMS -----------
R_THIC = 10
R_VOFF = 40
G_HOFF = 50
G_VOFF = 70
G_WIDC = 50
G_WALL = 2


# -------- ON INIT ----------
G_SHAP = None
G_DIMS = None
R_DIMS = None
W_DIMS = None

ORB_PL1 = None
ORB_PL2 = None


# ----------- INIT ---------------
def init(g_shape=(9, 6)):
    """
    Calculate dimensions and construct sprites
    Input : g_shape (rows, cols)
    """
    global G_SHAP, G_DIMS, R_DIMS, W_DIMS
    global ORB_PL1, ORB_PL2

    # calculate dims
    G_SHAP = (g_shape[1], g_shape[0])
    G_DIMS = (G_SHAP[0] * G_WIDC + G_WALL, G_SHAP[1] * G_WIDC + G_WALL)
    R_DIMS = (G_DIMS[0], R_THIC)
    W_DIMS = (G_DIMS[0] + (2 * G_HOFF), G_DIMS[1] + G_HOFF + G_VOFF)

    # construct sprites
    ORB_SIZ = G_WIDC - G_WALL
    ORB_PL1 = sprites.construct_orbs(COL_PL1, COL_BCK, ORB_SIZ)
    ORB_PL2 = sprites.construct_orbs(COL_PL2, COL_BCK, ORB_SIZ)


# ---------- CLASSES -------------
class StaticGameWindow:
    def __init__(self):
        """ Display static graphics for the game """

        # warn if not init
        assert W_DIMS, "Window not initialized"

        # window
        self.win = pygame.display.set_mode(W_DIMS)
        self.clk = pygame.time.Clock()

        # params
        self.open = True

        # mouse click and index
        self.midx = None
        self.mclk = False

        # draw empty grid
        self.clear()
        self.draw_nxpl(0)
        self.draw_grid()
        self.update()

    def clear(self):
        self.win.fill(COL_BCK)

    def update(self):
        pygame.display.update()

    def event_handler(self):
        """ Handle events in window """
        # Refresh values
        self.mclk = False
        self.midx = None

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                self.open = False
                return

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mclk = True
                crx, cry = pygame.mouse.get_pos()
                idx = ((cry - G_VOFF) // G_WIDC, (crx - G_HOFF) // G_WIDC)
                val = (0 <= idx[0] < G_SHAP[1]) * (0 <= idx[1] < G_SHAP[0])
                self.midx = idx if val else None

        self.clk.tick(40)

    def draw_nxpl(self, plr):
        """ Draw rectangle to indicate next player """
        pcolor = COL_PL2 if plr else COL_PL1
        nxrect = (G_HOFF, R_VOFF, G_DIMS[0], R_THIC)
        pygame.draw.rect(self.win, pcolor, nxrect)

    def draw_grid(self):
        """ Draw grid on screen """
        surface = self.win
        gwid, ghgt = G_DIMS

        # horizontal lines
        for j in range(G_SHAP[1] + 1):
            grect = (G_HOFF, G_VOFF + j * G_WIDC, gwid, G_WALL)
            pygame.draw.rect(surface, COL_GRD, grect)

        # vertical lines
        for i in range(G_SHAP[0] + 1):
            grect = (G_HOFF + i * G_WIDC, G_VOFF, G_WALL, ghgt)
            pygame.draw.rect(surface, COL_GRD, grect)

    def draw_orbs(self, state):
        """ Draw orb sprites on the surface """
        gcol, grow = G_SHAP
        offx, offy = (G_HOFF + G_WALL, G_VOFF + G_WALL)
        for idx in range(grow * gcol):
            ccount = state[idx]
            if ccount != 0:
                i_y, i_x = idx // gcol, idx % gcol
                pos = (G_WIDC * i_x + offx, G_WIDC * i_y + offy)
                psprite = ORB_PL1 if ccount > 0 else ORB_PL2
                self.win.blit(psprite[abs(ccount) - 1], pos)

    def draw_all(self, board, plr):
        """ Draw all elements and update display """
        self.clear()
        self.draw_orbs(board)
        self.draw_nxpl(plr)
        self.draw_grid()
        self.update()
