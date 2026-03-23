import os
import asyncio
from datetime import date
from dotenv import load_dotenv
import reflex as rx
from formulari_app.pages.formulari.components.wrapper import wrapper
from formulari_app.services.sheets_service import SheetsService
from formulari_app.services.google_clients.sheets_client import sheets_client
from formulari_app.services.google_clients.google_client import GoogleClient
from formulari_app.lib.google_credentials import credentials, SCOPES


load_dotenv()
GOOGLE_SPREADSHEET_ID=os.getenv("GOOGLE_ACTES_SPREADSHEET_ID") or ""
GOOGLE_SHEET = "Paelles 2026"

def get_sheets_client(sheet_name):
    creds = GoogleClient.create_with_credentials(credentials_args = credentials, scopes = SCOPES)
    current_date = date.today()
    current_year = current_date.year
    sheet_name = f"{sheet_name.capitalize()} {current_year}"
    return sheets_client(creds, GOOGLE_SPREADSHEET_ID, sheet_name)

class FormState(rx.State):
    form_data: dict = {}
    loading: bool = False
    total_personas: int = 0
    max_persons: int = 40

    @rx.var
    def spots_left(self) -> int:
        return max(0, self.max_persons - self.total_personas)

    @rx.var
    def is_full(self) -> bool:
        return self.total_personas >= self.max_persons

    async def get_current_occupancy(self):
        loop = asyncio.get_running_loop()
        client = get_sheets_client(sheet_name=self.sheet_name)
        # Usamos el método que ya tienes en SheetsService
        res = await loop.run_in_executor(None, SheetsService.get_total_personas, client.open(self.sheet_name).sheet1)
        self.total_personas = int(res) if res else 0


    @rx.var
    def sheet_name(self) -> str:
        return self.router.url.split("/")[-1] or "paelles"


    async def handle_submit(self, data: dict):
        """Handle the form submit."""
        self.form_data = data
        self.loading = True
        yield

        try:
            loop = asyncio.get_event_loop()
            client = get_sheets_client(sheet_name=self.sheet_name)
            await loop.run_in_executor(None, SheetsService.append_row, list(self.form_data.values()), client, self.sheet_name)
            yield rx.toast.success("✅ Reserva enviada correctament", duration=3000, position="top-center")

        except Exception as e:
            message = str(e)
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
