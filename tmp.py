from tabulate import tabulate


x = [i for i in range(7, 38, 5)]
f = [83.7, 72.9, 63.2, 54.7, 47.5, 41.4, 36.3]
N = len(f) - 1
print(x)
F = [f]+[[0]*(N-i) for i in range(N)]  # таблица значений f

k = 1
for j in range(1, len(F)):
    for i in range(len(F[j])):
        if (x[i+k] - x[i]) != 0:
            F[j][i] = (F[j-1][i+1] - F[j-1][i]) / (x[i+k] - x[i])
        else:
            print(f"STOP! YOU HAVE EQUAL NODES: {x[i+k]} and {x[i]}")
            exit(0)
    k += 1
    print(tabulate(F, showindex=[f"k={i}" for i in range(N+1)], tablefmt="fancy_grid"))


print(f"P_6 = {F[0][0]} + (x-{x[0]})*{F[1][0]} + (x-{x[0]})*(x-{x[1]})*{F[2][0]} + (x-{x[0]})*(x-{x[1]})*(x-{x[2]})*{F[3][0]} +\n"
      f" + (x-{x[0]})*(x-{x[1]})*(x-{x[2]})*(x-{x[3]})*{F[4][0]} + (x-{x[0]})*(x-{x[1]})*(x-{x[2]})*(x-{x[3]})*(x-{x[4]})*{F[5][0]} +\n"
      f" + (x-{x[0]})*(x-{x[1]})*(x-{x[2]})*(x-{x[3]})*(x-{x[4]})*(x-{x[5]})*{F[6][0]}")


from sympy import Symbol
from sympy.solvers import solve


x = Symbol("x")
f = 10 + (x-10)*33.0 - (x-10)*(x-20)*0.6 - (x-10)*(x-20)*(x-30)*0.01 + (x-10)*(x-20)*(x-30)*(x-40)*0.00050 + (x-10)*(x-20)*(x-30)*(x-40)*(x-50)*2.499*(10**(-6)) - (x-10)*(x-20)*(x-30)*(x-40)*(x-50)*(x-60)*6.66*(10**(-7))


def find_extremums(func, arg):

    dy = func.diff(arg)
    extremums = solve(dy, arg)

    return extremums


for el in find_extremums(f, x):
    print(f"Значение в точке и точка: {f.subs(x, el), el}")
print("То есть максимальная концентрация это 591.198569714837")