import reflex as rx

config = rx.Config(
    app_name="formulari_app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    app_title="Formulari de la Breda",
    app_description="Formulari per a la Breda de l'Eixample",
    app_icon="favicon.ico"
)
