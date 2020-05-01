import pygame
import pygame.gfxdraw as gfxdraw
import pygame.surfarray as surfarray
import numpy as np

# ----------- UTILITIES ------------------
def gaussian_blur(surface, radius, strength):
    """
    Blur the given surface
    Convolves pixel with gaussian kernel
    Modifies surface inplace
    """

    def in_gkernel(size):
        for n in range(size):
            ar = [ar[i - 1] + ar[i] for i in range(1, n)]
            ar = [1] + ar + [1]
        return ar

    k_half = radius // 2
    k_size = 1 + k_half * 2
    kern_l = in_gkernel(k_size)
    kernel = np.array(kern_l) / sum(kern_l)
    matrix = surfarray.pixels3d(surface)

    in_pad = lambda x: np.pad(x, k_half, mode="edge")
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
def construct_orbs(fore, back, width, glow_rad=100, glow_stren=1.0):
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

    # glow
    glow_rad = min(width - 1, glow_rad)

    # draw anti-aliased filled circle on surface
    def in_fcircle(surf, x, y, c):
        gfxdraw.aacircle(surf, cent + x, cent + y, radi, c)
        gfxdraw.filled_circle(surf, cent + x, cent + y, radi, c)

    # draw flat orbs on surface
    def in_flat_orbs(surf, num):
        if num == 1:
            in_fcircle(surf, 0, 0, col1)
        elif num == 2:
            in_fcircle(surf, -off2, 0, col2)
            in_fcircle(surf, +off2, 0, col1)
        elif num == 3:
            in_fcircle(surf, -off1, -off2, col3)
            in_fcircle(surf, -off1, +off2, col2)
            in_fcircle(surf, +off2, 0, col1)

    # return glowing orbs
    def in_glowing_orb(num):
        surf = pygame.Surface((width, width))
        surf.fill(back)
        in_flat_orbs(surf, num)
        gaussian_blur(surf, glow_rad, glow_stren)
        in_flat_orbs(surf, num)
        return surf

    return tuple(map(in_glowing_orb, range(1, 4)))
