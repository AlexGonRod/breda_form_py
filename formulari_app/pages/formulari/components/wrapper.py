import reflex as rx

def wrapper(sheet_name: str) -> rx.Component:
    return rx.flex(
                rx.cond(
                    sheet_name == "tast",
                    rx.text("🍷", size="9", align="center", margin=""),
                    rx.text("🥘", size="9", align="center", margin=""),
                ),
                rx.cond(
                    sheet_name == "tast",
                    rx.heading("Tast de vins", as_="h1", size="8", align="center"),
                    rx.heading("Concurs de paelles", as_="h1", size="8", align="center"),
                ),
                rx.heading("Breda de l'Eixample", as_="h2", size="6", align="center", margin_bottom="16px"),
                rx.cond(
                    sheet_name == "tast",
                    rx.text("Si us plau, ompliu el formulari per participar en el Tast de vins.\nAquest any, el pagamanet es farà per transferència bancària.\nUna vegada ompliu el formulari, rebreu per missatge al móvil les dades corresponents.", white_space="pre-wrap", ),
                    rx.text("Si us plau, ompliu el formulari per participar en el Concurs de paelles."),
                ),
                rx.text("Qualsevol dubte, posseu-vos en contacte amb: ", rx.link("bredainfocat@gmail.com ", href="mailto:bredainfocat@gmail.com")),
                border="1px solid",
                border_radius="10px",
                padding="20px",
                margin_bottom="20px",
                direction="column",
                spacing="1",
                width="100%",
                text_wrap="auto"
                # class_name="bg-white text-black",
            )
