import turtle
import geometry as gd
import matplotlib.pyplot as plt
from random import randint

in_motion = False

s = turtle.getscreen()
s.colormode(255)
t = turtle.Turtle()

t.pensize(2)
t.speed(0)
t.shape("circle")
t.shapesize(.1, .1)


def plot_stable_generation_vs_nbr_cote(min_cote=3, max_cote=40, nbr_fig1=4):
    stable_generation = []

    for nbr_cote in range(min_cote, max_cote):
        print("\n-------------------------", nbr_cote, "--------------------------------")
        sum = 0
        for nbr_fig in range(nbr_fig1):
            fig = gd.Figure(str(nbr_cote) + "-polygon", 50, t, n_centers=10, fictive=True)
            fig.evolve()
            sum += fig.generation
        stable_generation.append(sum/nbr_fig1)

    plt.plot(range(min_cote, max_cote), stable_generation)
    plt.show()


def plot_stable_nbr_cote_vs_nbr_cote(min_cote=3, max_cote=40, nbr_fig1=4):
    stable_nbr_cote = []

    for nbr_cote in range(min_cote, max_cote):
        print("\n-------------------------", nbr_cote, "--------------------------------")
        sum = 0
        for nbr_fig in range(nbr_fig1):
            fig = gd.Figure(str(nbr_cote) + "-polygon", 50, t, n_centers=10, fictive=True)
            fig.evolve()
            sum += len(fig.points)
            print(len(fig.points), end=" ")
        stable_nbr_cote.append(sum/nbr_fig1)

    plt.plot(range(min_cote, max_cote), stable_nbr_cote)
    plt.show()


def test():

    for nbr_cote in range(6, 7):
        print("\n-------------------------", nbr_cote, "--------------------------------")
        for nbr_fig in range(100):
            min_w = randint(0, 20)
            max_w = randint(min_w, 200)
            myweights = [randint(min_w, max_w) for _ in range(nbr_cote)]
            fig = gd.Figure(str(nbr_cote) + "-polygon", 50, t, n_centers=10, weights=myweights, fictive=True)
            fig.evolve()
            print(fig.previous_set_of_weights[0], "----------->", fig.generation)


def generate_random_figures(n=100, max_nbr_p=10):
    i = 0
    while i < n:
        i += 1
        k = randint(3, max_nbr_p)
        fig = gd.Figure(str(k)+"-random", 50, t, n_centers=10, fictive=False)
        fig.evolve()
        print("okkk")
        turtle.clearscreen()
        s.colormode(255)


fig = gd.Figure("8-polygon", 50, t, n_centers=10)

fig.evolve()

turtle.mainloop()
