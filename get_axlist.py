import matplotlib.pyplot as plt

def get_axlist(n, rows=7):
    fig = plt.figure()
    fig.set_size_inches(8.3, 10.5)
    bottom = 0.07
    top = 0.95
    lt = 0.05
    rt = 0.95
    ht = (top - bottom) / n
    wd = (rt - lt) / rows
    axlist = []
    for cnt in range(n):
        y = top - ht * (cnt + 1)
        row = []
        for i in range(rows):
            x = lt + i * wd
            if i == 0 and rows == 7:
                ax = plt.axes([x, y, wd / 2, ht / 2])
                ax.tick_params(labelsize=4)
            else:
                ax = plt.axes([x + wd * 0.2, y, wd * 0.8, ht * 0.8])
                ax.tick_params(labelsize=4)
            row.append(ax)
        axlist.append(row)
    if n == 1:
        fig.set_size_inches(440 / 80, 100 / 80)
    else:
        fig.set_size_inches(540 / 80, 400 / 80)
    h = plt.axes([0.05, 0.95, 0.5, 0.03])
    t = h.text(0, 0, 'Tag')
    t.set_color('r')
    t.set_weight('bold')
    t.set_horizontalalignment('left')
    h.axis('off')
    plt.draw()
    return axlist, fig
