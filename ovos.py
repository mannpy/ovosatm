# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:45:53 2015

@author: SYSTEM
"""

class Ovos(object):

    """ Класс-объект, для решения задач по дисциплине ОВОС"""


    def __init__(self, W0=None, D=0.25, H=30, Tg=100, Tv=26, V1=None,
                 cold=False, pr=False, L=None, b=None):

        """ Иниализация объекта.
        W0(м/с) - средння скорость выхода газовоздушной смеси из устья
        источника выброса;
        D(м) - диаметр устья источника выброса;
        H(м) - высота исчтоника выброса над уровнем земли
        (для наземных источников при расчетах принимается H = 2м);
        Tg(град. C) - температура выбрасываемой газовоздушной смеси
        (по действующим для данного производства технологическим нормативам);
        Tv(град. C) - температура окружающего атмосферного воздуха
        (следует принимать т-ру атмосферного воздуха, равной средней
        максимальной температуре наружного воздуха наиболее жаркого месяца
        года. Для котельных, работающих по отопительному графику,
        допускается при расчетах принимать значения Тv равными средним
        температурам наружного воздуха за самый холодный месяц);
        V1(м^3/c) - расход газовоздушной смеси
        cold - горячий или холодный истоник. False - горячий,
        True - холодный;
        pr - прямоугольный или круглый. True - прямоугольный;

        для источника с прямоугольным устьем:
        L(м) -длина устья
        b(м) -ширина устья
        """

        self.label = ""
        self.cold, self.pr = cold, pr
        self.dT = Tg - Tv
        if self.dT < 0:
            self.dT = 0
        # если dT = 0 то исчтоник - холодный
        if not self.dT:
            self.cold = True
        self.W0, self.V1 = W0, V1
        if not V1:
            self.V1 = round(0.785 * W0 * D ** 2, 3)
            if self.W0:
                self.label += "[i][color=00C853]   Расход\
      газовоздушной смеси:[/i][/color]\n"
                self.label += "V[sub]1[/sub] = 0.785 · W[sub]0[/sub] · D[sup]2[/sup] = 0.785 · {} · {}[sup]2[/sup] = {} м[sup]3[/sup]/c\n\n".format(
                    W0, D, self.V1
                )
        if not W0:
            try:
                self.W0 = round(4 * V1 / (3.14 * D ** 2), 3)
                if V1 and not self.cold:
                    self.label += '[i][color=00C853]Скорость выхода газовоздушной смеси W[sub]0[/sub]:[/color][/i]\n'
                    self.label += "W[sub]0[/sub] = 4 · V[sub]1[/sub] / (3.14 · D[sup]2[/sup]) = 4 · {} / (3.14 · {}[sup]2[/sup]) = {} м/c\n\n".format(
                        V1, D, self.W0
                    )
            except ZeroDivisionError:
                self.W0 = 0
        self.D, self.H = D, H
        # для прямоугольного источника
        self.L, self.b = L, b
        if L and b:
            self.pr = True
            self.label += "[b][color=673AB7]Одиночный источник с прямоугольным устьем "
            if self.cold:
                self.label += "(холодный):[/color][/b]\n\n"
            else:
                self.label += "(горячий):[/color][/b]\n\n"
            self.D = round((2  * L * b) / (L + b),3)
            self.label += "[i][color=00C853]   Эквивалентный диаметр:[/i][/color]\n"
            self.label += "D[sub]э[/sub] = 2  · L · b / (L + b) = 2  · {0} · {1} / ({0} + {1}) \
= {2}\n".format(self.L, self.b, self.D)
            self.W0 = round(V1 / (L * b),3)
            self.label += '[i][color=00C853]   Скорость выхода газовоздушной смеси W[sub]0[/sub]:[/color][/i]\n'
            self.label += "W[sub]0[/sub] = V[sub]1[/sub] / (L · b) = {} / ({} · {}) = {}\n".format(self.V1,
            self.L, self.b, self.W0)
            self.V1 = round((3.14 * self.D ** 2) / 4 * self.W0,3)
            self.label += "[i][color=00C853]   Эквивалентный объем выбрасываемой в атмосферу\
  газовоздушной смеси:[/i][/color]\n"
            self.label += "V[sub]1[/sub] = 3.14 · D[sup]2[/sup] / (4 · W0) = 3.14 · {}[sup]2[/sup] / (4 · {}) = {}\n".format(self.D, self.W0, self.V1)

        if not self.pr:
            self.label += "[b][color=673AB7]Одиночный источник с круглым устьем"
            if self.cold:
                self.label += "(холодный):[/color][/b]\n\n"
            else:
                self.label += "(горячий):[/color][/b]\n\n"

    def parameters(self):

        """ Возвращает параметры f, Vm, Vml, fe - для горячего,
        Vml - для холодного
        """

        if not self.cold:
            self.f = round(1000 * (self.W0 ** 2 * self.D) / (self.H ** 2 * self.dT), 3)
            self.label += " [i][color=00C853]Вычисляем f:[/i][/color]\n 1000 · (W0[sup]2[/sup] · D) / (H[sup]2[/sup] · ΔT) = 1000 · ({}[sup]2[/sup] · {}) / ({}[sup]2[/sup] · {}) = {}\n" \
        .format(self.W0, self.D, self.H, self.dT, self.f)
            self.Vm =  round((0.65 * ((self.V1 * self.dT) / self.H) ** (1.0/3)), 3)
            self.label += " [i][color=00C853]Вычисляем V[sub]m[/sub]:[/i][/color]\n 0.65 · ((V[sub]1[/sub] · ΔT) / H)[sup]1/3[/sup] = 0.65 · (({} · {}) / {})[sup]1/3[/sup] = {}\n" \
        .format(self.V1, self.dT, self.H, self.Vm)

        self.Vml = round(1.3 * (self.W0 * self.D) / self.H, 3)
        self.label += " [i][color=00C853]Вычисляем V[sub]m[/sub]':[/i][/color]\n 1.3 · (W[sub]0[/sub] · D) / H = 1.3 · ({} · {}) / {} = {}\n" \
        .format(self.W0, self.D, self.H, self.Vml)

        if not self.cold:

            self.fe = round(800 * (self.Vml) ** 3, 3)
            self.label += " [i][color=00C853]Вычисляем fe:[/i][/color]\n 800 · (V[sub]m[/sub]')[sup]3[/sup] = 800 · {}[sup]3[/sup] = {}\n\n" \
        .format(self.Vml, self.fe)

    def m_coef(self):

        """ Возвращает коэффициент m """

        if self.fe < self.f < 100:
            self.m = round(1 / (0.67 + 0.1 * self.fe ** (1.0/2) + \
            0.34 * self.fe ** (1.0/3)), 3)
            self.label += "[i][color=304FFE]при fe < f < 100:[/i][/color]\n"
            self.label += "  [b]m[/b] = 1 / (0.67 + 0.1 · √fe + 0.34 · 3√fe) \
= 1 / (0.67 + 0.1 · √{0} + 0.34 · 3√{0}) = {1}\n".format(self.fe, self.m)
        elif self.f < 100:
            self.m = round(1.0 / (0.67 + 0.1 * self.f ** (1.0/2) + \
            0.34 * self.f ** (1.0/3)), 3)
            self.label += "[i][color=304FFE]при f < 100:[/i][/color]\n"
            self.label += "  [b]m[/b] = 1 / (0.67 + 0.1 · √f + 0.34 · 3√f) \
= 1 / (0.67 + 0.1 · √{0} + 0.34 · 3√{0}) = {1}\n".format(self.f, self.m)
        else:
            self.m = round(1.47 / (self.f ** (1.0/3)), 3)
            self.label += "[i][color=304FFE]при f ≥ 100:[/i][/color]\n"
            self.label += "  [b]m[/b] = 1.47 / 3√f \
= 1.47 / 3√{0} = {1}\n".format(self.f, self.m)
    def n_coef(self):

        """ Возвращает коэффициент n """

        if self.cold:
            V = self.Vml
            self.label += "[color=00BCD4]Для холодного источника [color=FF1744]n[/color] определяется в зависмости от Vm'[/color]:\n"
        else:
            V = self.Vm

        if V >= 2:
                self.n = 1
                self.label += "[i][color=304FFE]при V[sub]m[/sub] ≥ 2:[/i][/color]\n"
                self.label += "  [b]n[/b] = 1\n\n"
        elif 0.5 <= V < 2:
            self.n = round(0.532 * V ** 2 - 2.13 * V + 3.13, 3)
            self.label += "[i][color=304FFE]при 0.5 ≤ V[sub]m[/sub] < 2:\n[/i][/color]"
            self.label += "  [b]n[/b] = 0.532 · Vm[sup]2[/sup] - 2.13 · V[sub]m[/sub] + 3.13 = \
0.532 * {}^ 2 - 2.13 * {} + 3.13 = {}\n\n".format(V, V, self.n)
        elif V < 0.5:
            self.n = round(4.4 * V, 3)
            self.label += "[i][color=304FFE]при V[sub]m[/sub] < 0.5:[/i][/color]\n"
            self.label += "  [b]n[/b] = 4.4 · V[sub]m[/sub] = 4.4 · {} = {}\n\n".format(V, self.n)

    def max_concentrate(self, M, F, A=160, nu=1):

        """ определяет максимальную концентрацию """

        self.label += "[color=673AB7]Определяем максимальную концентрацию C[sub]m[/sub]:[/color]\n"
        self.M = float(M)
        if not hasattr(self, "F"):
            self.F = float(F)
        if not hasattr(self, "A"):
            self.A = float(A)
        if not hasattr(self, "nu"):
            self.nu = float(nu)

        K = round(self.D / (8 * self.V1),3)

        if self.cold:
            self.label += "[b]K[/b] = D / (8 · V[sub]1[/sub]) = K = {} / (8 · {}) = {}\n".format(
                self.D, self.V1, K)
            self.Cm = round((A * M * F * self.n * nu) / (self.H ** (4.0/3)) * K, 3)
            self.label += "[b]C[sub]m[/sub][/b] = (A · M · F · n · η) / (H[sup]4/3[/sub]) · K = \
({} · {} · {} · {} · {}) / ({}[sup]4/3[/sub]) · {} = {} мг/м[sup]3[/sup]\n\n".format(
    A, M, F, self.n, nu, self.H, K, self.Cm)
        else:
            self.Cm = round((A * M * F * self.m * self.n * nu)/(self.H ** 2 * (self.V1 * self.dT) ** (1.0/3)),3)
            self.label += "[b]C[sub]m[/sub][/b] = (A · M · F · m · n · η) / \
(H[sup]2[/sup] · 3√(V[sub]1[/sub] · ΔT)) = ({} · {} · {} · {} · {} · {}) / \
({}[sup]2[/sup] · 3√({} · {})) = {} мг/м[sup]3[/sup]\n\n".format(
A, M, F, self.m, self.n, nu, self.H, self.V1, self.dT, self.Cm)


    def max_distance(self):

        """ Расстояние Xm, где наблюдается Cm """

        self.label += "[color=673AB7]Определяем расстояние X[sub]m[/sub]:[/color]\n"

        if self.cold or self.f > 100:

            if self.Vml <= 0.5:
                self.label += "[i][color=304FFE]при V[sub]m[/sub]' < 0.5:[/i][/color]\n"
                d = 5.7
                self.label += "[b]d[/b] = {}\n".format(d)
            elif 0.5 < self.Vml <= 2:
                self.label += "[i][color=304FFE]при 0.5 ≤ V[sub]m[/sub]' < 2:\n[/i][/color]"
                d = 11.4 * self.Vml
                self.label += "[b]d[/b] = 11.4 · {} = {:.3g}\n".format(self.Vml, d)
            elif self.Vml > 2:
                self.label += "[i][color=304FFE]при V[sub]m[/sub]' ≥ 2:[/i][/color]\n"
                d = 16 * self.Vml ** (1.0 / 2)
                self.label += "[b]d[/b] = 16 · √{} = {:.3g}\n".format(self.Vml, d)
        else:

            if self.Vm <= 0.5:
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.label += "[i][color=304FFE]при V[sub]m[/sub] < 0.5:[/i][/color]\n"
                d = 2.48 * (1 + 0.28 * self.fe ** (1.0 / 3))
                self.label += "[b]d[/b] = 2.48 · (1 + 0.28 · 3√{}) = {:.3g}\n".format(self.fe, d)
            elif 0.5 < self.Vm <= 2:
                self.label += "[i][color=304FFE]при 0.5 ≤ V[sub]m[/sub]' < 2:\n[/i][/color]"
                d = 4.95 * self.Vm * (1 + 0.28 * self.f ** (1.0 / 3))
                self.label += "[b]d[/b] = 4.95 · {} · (1 + 0.28 · 3√{}) = {:.3g}\n".format(
                    self.Vm, self.f, d)
            elif self.Vm > 2:
                self.label += "[i][color=304FFE]при V[sub]m[/sub]' ≥ 2:[/i][/color]\n"
                d = 7 * self.Vm ** (1.0 / 2) * (1 + 0.28 * self.f ** (1.0 / 3))
                self.label += "[b]d[/b] = 7 · √{} · (1 + 0.28 · 3√{}) = {:.3g}\n".format(
                    self.Vm, self.f, d)

        self.Xm = round((5 - self.F) / 4 * self.H * d,3)
        self.label += "[b]X[sub]m[/sub][/b] = (5 - F) / 4 · H · d = (5 - {}) / 4 · {} · {:.3g} = {} м\n\n".format(self.F,
            self.H, d, self.Xm)

    def pdv_func(self, pdk, Cf, F=1, A=160, nu=1):

        """ Расчет нормативов предельно допустимых выбросов """

        self.pdk = pdk
        self.Cf = Cf
        if not hasattr(self, "F"):
            self.F = float(F)
        if not hasattr(self, "A"):
            self.A = float(A)
        if not hasattr(self, "nu"):
            self.nu = float(nu)

        self.label += "[color=673AB7]Определяем ПДВ:[/color]\n"

        if self.cold:
            self.pdv = round(((pdk - Cf) * self.H ** (4.0 / 3) * 8 * self.V1) / \
            (self.A * self.F * self.n * self.nu * self.D),3)
            self.label += 'ПДВ = ((ПДК - C[sub]ф[/sub]) · H[sup]4/3[/sup] · 8 · V[sub]1[/sub]) / \
(A · F · n · η · D) =(({} - {}) · {}[sup]4/3[/sup] · 8 · {}) / \
({} · {} · {} · {} · {}) = {} мг/м[sup]3[/sup]'.format(
            pdk, Cf, self.H, self.V1, self.A, self.F, self.n, self.nu, self.D, self.pdv)
        else:
            self.pdv = round(((pdk - Cf) * self.H ** 2 * (self.V1 * self.dT) ** (1.0 / 3)) / \
            (self.A * self.F * self.m * self.n * self.nu),3)
            self.label += "ПДВ = ((ПДК - C[sub]ф[/sub]) · H[sup]2[/sup]) / (A · F · m · n · η ) · \
3√(V[sub]1[/sub] · ΔT) = (({} - {}) · {}[sup]2[/sup]) / ({} · {} · {} · {} · {} ) · \
3√({} · {}) = {} мг/м[sup]3[/sup]\n".format(pdk, Cf, self.H,  self.A, self.F, self.m, self.n, self.nu, self.V1,
self.dT, self.pdv)



def main():
    zad = Ovos(V1=0.98, H=25, L=0.875, b=0.35, Tg=25, Tv=25)
    zad.parameters()
    if not zad.cold:
        zad.m_coef()
    zad.n_coef()
    zad.max_concentrate(A=160, M=16, F=1, nu=1)
    zad.max_distance()
    print(zad.label)
    zad.pdv_func(1.5, 0.3)
