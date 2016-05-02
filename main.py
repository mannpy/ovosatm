# coding: utf-8
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from ovos import Ovos


class OvosSet(Screen):

    def add_widget_to_screen(self, screen, label_text, input_id, input_text="", markup=False, color=(0, 0, 0, 1)):
        """ добавляет виджеты на экран """
        screen.layout.add_widget(Label(text=label_text, color=color, size_hint_y=None, markup=markup))
        screen.layout.add_widget(TextInput(id=input_id, text=input_text, multiline=False,
                                             size_hint_y=None, input_type="number", input_filter="float"))

    def apply(self):

        dataset = []
        self.ovosinput.layout.clear_widgets()

        for widget in self.ovosinput.walk():
            dataset.append(widget.id)

        if "H" not in dataset:
            self.add_widget_to_screen(self.ovosinput, "H (м)", "H")

        if self.round.state == "down":
            if "D" not in dataset:
                self.add_widget_to_screen(self.ovosinput, "D (м)", "D")

        if self.rectangular.state == "down":
            if "L" and "b" not in dataset:
                self.add_widget_to_screen(self.ovosinput, "L (м)", "L")
                self.add_widget_to_screen(self.ovosinput, "b (м)", "b")

        if self.hot.state == "down":
            if "Tv" and "Tg" not in dataset:
                self.add_widget_to_screen(self.ovosinput, "T[sub]г[/sub] (°С)", "Tg", markup=True)
                self.add_widget_to_screen(self.ovosinput, "T[sub]в[/sub] (°С)", "Tv", markup=True)

        if self.rectangular.state == "down":
            self.v1.state = "down"
            self.w0.state = "normal"

        if self.w0.state == "down":
            if "W0" not in dataset:
                self.add_widget_to_screen(self.ovosinput, "W[sub]0[/sub] (м/c)", "W0", markup=True)


        if self.v1.state == "down":
            if "V1" not in dataset:
                self.add_widget_to_screen(self.ovosinput, "V[sub]1[/sub] (м[sup]3[/sup]/c)", "V1", markup=True)

        if self.cmxm.active:
            if "A" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="A", input_id="A", input_text="160")

            if "M" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="M (г/c)", input_id="M")

            if "F" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="F", input_id="F")

            if "nu" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="η", input_id="nu", input_text="1")

        if self._pdv.active:
            for widget in self.ovosinput.walk():
                dataset.append(widget.id)
            if "pdk" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="ПДК (мг/м[sup]3[/sup])", input_id="pdk", markup=True)

            if "Cf" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="С[sub]ф[/sub] (мг/м[sup]3[/sup])", input_id="Cf", markup=True)

            if "A" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="A", input_id="A", input_text="160")

            if "F" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="F", input_id="F")

            if "nu" not in dataset:
                self.add_widget_to_screen(self.ovosinput, label_text="η", input_id="nu", input_text="1")


class OvosInput(Screen):

    def calculate(self):

        dataset = {}
        data = ("W0", "V1", "Tv", "Tg", "L", "b", "H", "D", "A", "F", "M", "nu",
        	"pdk", "Cf")

        for w in self.walk():
            if w.id is not None:
                try:
                    dataset[w.id] = float(w.text)
                except ValueError:
                    w.text = "!"
                    dataset[w.id] = w.text

        for d in data:
            if d not in dataset:
                dataset[d] = 0
        if dataset["H"] == 0:
            dataset["H"] = "!"

        if "!" not in dataset.values():
            self.manager.current = '_result'
            self.task = Ovos(W0=dataset['W0'], D=dataset['D'], H=dataset['H'],
                             Tg=dataset['Tg'], Tv=dataset['Tv'], V1=dataset['V1'],
                             L=dataset['L'], b=dataset['b'])
            self.task.parameters()
            if not self.task.cold:
                self.task.m_coef()
            self.task.n_coef()

            if self.manager.ovosset.cmxm.active:
            	self.task.max_concentrate(M=dataset['M'], F=dataset['F'],
            		A=dataset['A'], nu=dataset['nu'])
            	self.task.max_distance()

            if self.manager.ovosset._pdv.active:
            	self.task.pdv_func(pdk=dataset['pdk'], Cf=dataset['Cf'],
            	F=dataset['F'], A=dataset['A'], nu=dataset['nu'])
            self.manager.result.text = self.task.label


class MainClass(Widget):
    pass


class OvosApp(App):

    def build(self):
        return MainClass()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    OvosApp().run()
