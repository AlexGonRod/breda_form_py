import os
from dotenv import load_dotenv
import asyncio
import reflex as rx
from formulari_app.pages.formulari.components.wrapper import wrapper
from formulari_app.services.sheets_service import SheetsService
from formulari_app.services.google_clients.sheets_client import sheets_client
from formulari_app.services.google_clients.google_client import GoogleClient
from formulari_app.lib.google_credentials import credentials, SCOPES

load_dotenv()
GOOGLE_SPREADSHEET_ID=os.getenv("GOOGLE_ACTES_SPREADSHEET_ID") or ""
GOOGLE_SHEET = "Paellas 2026"

def get_sheets_client():
    creds = GoogleClient.create_with_credentials(credentials_args = credentials, scopes = SCOPES)
    return sheets_client(creds, GOOGLE_SPREADSHEET_ID, GOOGLE_SHEET)

class FormState(rx.State):
    form_data: dict = {}
    loading: bool = False

    async def handle_submit(self, data: dict):
        """Handle the form submit."""
        self.form_data = data
        self.loading = True
        yield

        try:
            loop = asyncio.get_event_loop()
            client = get_sheets_client()
            loop.run_in_executor(None, SheetsService.append_row, list(self.form_data.values()), client)
            yield rx.toast.success("✅ Reserva enviada correctament", duration=3000, position="top-center")

        except Exception as e:
            message = hasattr(e, 'message') or str(e)
            yield rx.toast.error(f"❌ Error enviant la reserva: {message}", duration=5000, position="top-center")

        finally:
            self.loading = False
            yield


def formulari():
    return rx.container(
            wrapper(),
            rx.form(
                rx.vstack(
                    rx.form.field(
                        rx.form.label("Formulari del Concurs de paelles", font_size="24px", font_weight="bold", margin_bottom="16px"),
                        rx.flex(
                            rx.form.label("Nom"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Nom i cognoms",
                                    type="text",
                                    pattern="[A-Za-z]+",
                                    required=True,
                                    radius="small"
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "El nom és obligatori",
                                match="valueMissing",
                                color="red"
                            ),
                            rx.form.message(
                                "El nom no és vàlid",
                                match="patternMismatch",
                                color="orange",
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="nom",
                        width="100%",
                    ),
                    rx.form.field(
                        rx.flex(
                            rx.form.label("telefon"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Telèfon",
                                    type="text",
                                    pattern="[0-9]{9}",
                                    required=True,
                                    radius="small",
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "El telèfon és obligatori",
                                match="valueMissing",
                                color="red",
                            ),
                            rx.form.message(
                                "El telèfon no és vàlid",
                                match="patternMismatch",
                                color="orange",
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="telefon",
                        width="100%",
                    ),
                    rx.form.field(
                        rx.flex(
                            rx.form.label("persones"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Participants",
                                    type="number",
                                    required=True,
                                    radius="small"
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "Aquest camp és obligatori",
                                match="valueMissing",
                                color="red"
                            ),
                            rx.form.message(
                                "Aquest camp és obligatori",
                                match="typeMismatch",
                                color="red"
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="nombre",
                        width="100%",
                    ),
                    rx.button("Submit",rx.spinner(loading=FormState.loading), is_disabled=FormState.loading, type="submit", width="100%",
                                    radius="small"),

                ),
                on_submit=FormState.handle_submit,
                reset_on_submit=True,

                border="1px solid",
                border_radius="10px",
                padding="20px",
                spacing="15px",
            ),
            rx.divider(),
    )
