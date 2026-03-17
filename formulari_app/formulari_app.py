import reflex as rx
from reflex import App
from formulari_app.lib import copy

from formulari_app.pages.formulari.views.formulari import formulari


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("Benviguts a la pàgina de la Breda de l'Eixample!", size="8", text_align="center"),
            rx.list.ordered(
                rx.foreach(copy.copy, lambda item: rx.list.item(item, margin_bottom="5px")),
            ),
            rx.hstack(
                rx.link(
                    rx.button("Paelles"),
                    href="/formulari/paelles",
                    margin="0 auto"
                ),
                rx.link(
                    rx.button("Tast"),
                    href="/formulari/tast",
                    margin="0 auto"
                ),
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        )
    )

app = App(
    theme=rx.theme(radius="full", accent_color="grass"),
)
app.add_page(index, title="Breda de l'Eixample", route="/", description="Benvinguts a la pàgina de la Breda de l'Eixample! Aquí trobareu tota la informació sobre el concurs de paelles i podreu inscriure-us per participar. No us perdeu aquesta oportunitat de mostrar les vostres habilitats culinàries i gaudir d'un dia ple de sabor i diversió!", image="/assets/breda.png")
app.add_page(formulari, route="/formulari/[sheet]", title="Formulari de la Breda")
