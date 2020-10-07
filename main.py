import numpy as np
import pygame
import matplotlib.pyplot as plt


def get_curve_order(order, rotations):
    if order == 0:
        return np.array([[0]])
    else:
        factor = (2 ** (order - 1)) ** 2
        if rotations == 0:
            x10 = get_curve_order(order - 1, 1)
            x00 = get_curve_order(order - 1, 0) + factor
            x01 = get_curve_order(order - 1, 0) + 2 * factor
            x11 = get_curve_order(order - 1, 3) + 3 * factor
        elif rotations == 1:
            x10 = get_curve_order(order - 1, 0)
            x11 = get_curve_order(order - 1, 1) + factor
            x01 = get_curve_order(order - 1, 1) + 2 * factor
            x00 = get_curve_order(order - 1, 2) + 3 * factor
        elif rotations == 2:
            x01 = get_curve_order(order - 1, 3)
            x11 = get_curve_order(order - 1, 2) + factor
            x10 = get_curve_order(order - 1, 2) + 2 * factor
            x00 = get_curve_order(order - 1, 1) + 3 * factor
        else:
            x01 = get_curve_order(order - 1, 2)
            x00 = get_curve_order(order - 1, 3) + factor
            x10 = get_curve_order(order - 1, 3) + 2 * factor
            x11 = get_curve_order(order - 1, 0) + 3 * factor
        x0 = np.concatenate((x00, x01), axis=1)
        x1 = np.concatenate((x10, x11), axis=1)
        return np.concatenate((x0, x1), axis=0)


def get_next_color(num_colors):
    cmap = plt.cm.get_cmap('jet')
    step = -1 / num_colors
    ind = 0
    while True:
        if ind < 0.000001 or 0.99999 < ind:
            step *= -1
        clr = cmap(ind)
        ind += step
        yield int(clr[0] * 255), int(clr[1] * 255), int(clr[2] * 255)


phc_order = 5
curve_order = get_curve_order(phc_order, 0)
points = np.dstack(np.unravel_index(np.argsort(curve_order.ravel()), curve_order.shape))[0]
color = get_next_color((2 ** phc_order) ** 2)

pygame.init()

window_size = 2 ** max(phc_order + 1, 9)
cells_per_side = 2 ** phc_order
cell_length = window_size // cells_per_side

window = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()
frequency = 30  # the higher the frequency, the faster the curve will be drawn
run = True

window.fill((255, 255, 255))
index = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    if index < (len(points) - 1):
        row, col = points[index]
        n_row, n_col = points[index + 1]
        pygame.draw.line(window, next(color),
                         (cell_length // 2 + cell_length * col, cell_length // 2 + cell_length * row),
                         (cell_length // 2 + cell_length * n_col, cell_length // 2 + cell_length * n_row),
                         1)
        index += 1

    pygame.display.flip()
    clock.tick(frequency)

pygame.quit()
