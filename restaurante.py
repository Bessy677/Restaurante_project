import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=20, padding=50)

        titulo = Label(text="RESTAURANTE LA ESQUINA DEL SABOR",
                       font_size="24sp",
                       size_hint=(1, 0.3))

        boton_menu = Button(text="Ver menú",
                            font_size="20sp",
                            size_hint=(1, 0.2))
        boton_menu.bind(on_press=self.ir_a_menu)

        layout.add_widget(titulo)
        layout.add_widget(boton_menu)
        self.add_widget(layout)

    def ir_a_menu(self, instance):
        self.manager.current = "categorias"


class CategoriasScreen(Screen):
    def __init__(self, menu_data, **kwargs):
        super().__init__(**kwargs)
        self.menu_data = menu_data

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        titulo = Label(text="Categorías", font_size="22sp", size_hint=(1, 0.2))
        layout.add_widget(titulo)

        for categoria in self.menu_data.keys():
            boton = Button(text=categoria, font_size="18sp", size_hint=(1, 0.2))
            boton.bind(on_press=lambda instance, cat=categoria: self.ir_a_productos(cat))
            layout.add_widget(boton)

        self.add_widget(layout)

    def ir_a_productos(self, categoria):
        productos_screen = self.manager.get_screen("productos")
        productos_screen.mostrar_productos(categoria, self.menu_data[categoria])
        self.manager.current = "productos"


class ProductosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        self.scroll = ScrollView(size_hint=(1, 1))
        self.productos_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.productos_layout.bind(minimum_height=self.productos_layout.setter("height"))
        self.scroll.add_widget(self.productos_layout)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def mostrar_productos(self, categoria, productos):
        self.productos_layout.clear_widgets()

        titulo = Label(text=f"Productos - {categoria}", font_size="22sp", size_hint=(1, None), height=50)
        self.productos_layout.add_widget(titulo)

        for producto in productos:
            fila = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            nombre = Label(text=producto["nombre"], font_size="18sp", size_hint=(0.7, 1))
            precio = Label(text=f"L {producto['precio']}", font_size="18sp", size_hint=(0.3, 1))
            fila.add_widget(nombre)
            fila.add_widget(precio)
            self.productos_layout.add_widget(fila)

        boton_volver = Button(text="Volver a categorías", size_hint=(1, None), height=50)
        boton_volver.bind(on_press=lambda x: self.volver())
        self.productos_layout.add_widget(boton_volver)

    def volver(self):
        self.manager.current = "categorias"


class RestauranteApp(App):
    def build(self):
        with open("menu.json", "r", encoding="utf-8") as f:
            menu_data = json.load(f)

        sm = ScreenManager()
        sm.add_widget(InicioScreen(name="inicio"))
        sm.add_widget(CategoriasScreen(menu_data, name="categorias"))
        sm.add_widget(ProductosScreen(name="productos"))
        return sm


if __name__ == "__main__":
    RestauranteApp().run()
