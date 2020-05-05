import numpy as np
import pygame
import pygame.gfxdraw as gfxdraw
import pygame.surfarray as surfarray


# ----------- UTILITIES ------------------
def gaussian_blur(surface, std, strength):
    """
    Blur the given surface
    Convolves pixel with gaussian kernel
    Modifies surface inplace
    """

    matrix = surfarray.pixels3d(surface)
    width = matrix.shape[1] // 2

    def in_gkernel():
        # generate one dimensional gaussian kernel
        drange = lambda x: range(-x, 1 + x)
        return [np.exp(-0.4 * abs(i)) for i in drange(width)]

    kern_l = in_gkernel()
    kernel = np.array(kern_l) / np.sum(kern_l)

    in_pad = lambda x: np.pad(x, width, mode="edge")
    in_cnv = lambda x: np.convolve(in_pad(x), kernel, mode="valid")

    for i in range(matrix.shape[1]):
        matrix[i, :, 0] = in_cnv(matrix[i, :, 0])
        matrix[i, :, 1] = in_cnv(matrix[i, :, 1])
        matrix[i, :, 2] = in_cnv(matrix[i, :, 2])

    for j in range(matrix.shape[0]):
        matrix[:, j, 0] = in_cnv(matrix[:, j, 0])
        matrix[:, j, 1] = in_cnv(matrix[:, j, 1])
        matrix[:, j, 2] = in_cnv(matrix[:, j, 2])


# ----------- HIGH LEVEL -----------------
def construct_orbs(fore, back, width, glow_std=0.5, glow_stren=1.0):
    """ Construct orb sprites for blitting """

    # dimensions
    cent = int(width * 0.50)
    radi = int(width * 0.20)
    off1 = int(width * 0.08)
    off2 = int(width * 0.12)

    # colors
    col1 = fore
    col2 = tuple(int(i * 0.8) for i in col1)
    col3 = tuple(int(i * 0.8) for i in col2)

    # draw anti aliased circle on surf
    def in_draw_circle(surf, o1, o2, c):
        gfxdraw.aacircle(surf, cent + o1, cent + o2, radi, c)
        gfxdraw.filled_circle(surf, cent + o1, cent + o2, radi, c)

    # draw n orbs on surf
    def in_flat_orbs(surf, num):
        if num == 1:
            in_draw_circle(surf, 0, 0, col1)
        elif num == 2:
            in_draw_circle(surf, -off2, 0, col2)
            in_draw_circle(surf, +off2, 0, col1)
        elif num == 3:
            in_draw_circle(surf, -off1, -off2, col3)
            in_draw_circle(surf, -off1, +off2, col2)
            in_draw_circle(surf, +off2, 0, col1)

    # get glowing orbs
    def in_glowing_orb(num):
        surf = pygame.Surface((width, width))
        surf.fill(back)
        in_flat_orbs(surf, num)
        gaussian_blur(surf, glow_std, glow_stren)
        in_flat_orbs(surf, num)
        return surf

    return tuple([in_glowing_orb(i) for i in range(1, 4)])
