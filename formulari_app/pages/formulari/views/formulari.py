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
from formulari_app.lib.logger import logger
from formulari_app.lib.validators import FormDataValidator
from formulari_app.lib.rate_limiter import RateLimiter


load_dotenv()

# Validate environment variables on startup
GOOGLE_SPREADSHEET_ID = os.getenv("GOOGLE_ACTES_SPREADSHEET_ID")
if not GOOGLE_SPREADSHEET_ID:
    error_msg = "GOOGLE_ACTES_SPREADSHEET_ID env var not set"
    logger.error(error_msg)
    raise ValueError(f"⚠️ {error_msg}")

logger.info("Formulari page configured with Spreadsheet ID: %s...", GOOGLE_SPREADSHEET_ID[:20])

def get_sheets_client(sheet_name):
    creds = GoogleClient.create_with_credentials(credentials_args = credentials, scopes = SCOPES)
    current_date = date.today()
    current_year = current_date.year
    sheet_name = f"{sheet_name.capitalize()} {current_year}"
    logger.debug("Getting sheets client for: %s", sheet_name)
    return sheets_client(creds, GOOGLE_SPREADSHEET_ID, sheet_name)

class FormState(rx.State):
    form_data: dict = {}
    loading: bool = False
    total_persones: int = 0
    max_persons: int = 999

    @rx.var
    def spots_left(self) -> int:
        return max(0, self.max_persons - self.total_persones)

    @rx.var
    def is_full(self) -> bool:
        return self.total_persones >= self.max_persons

    async def load_occupancy(self):
        """Load current occupancy and max persons for the event"""
        try:
            logger.info("Loading occupancy for: %s", self.sheet_name)

            # Set max persons based on event type
            self.max_persons = SheetsService.get_max_personas(self.sheet_name)
            logger.debug("Max persons set to: %d for event: %s", self.max_persons, self.sheet_name)

            loop = asyncio.get_running_loop()
            client = get_sheets_client(sheet_name=self.sheet_name)
            res = await loop.run_in_executor(None, SheetsService.get_total_personas, client)
            self.total_persones = int(res) if res else 0
            logger.info("✅ Occupancy loaded: %d/%d participants", self.total_persones, self.max_persons)
        except Exception as e:
            logger.error("Error loading occupancy: %s", e, exc_info=True)
            self.total_persones = 0


    @rx.var
    def sheet_name(self) -> str:
        return self.router.url.split("/")[-1]


    async def handle_submit(self, data: dict)
        self.form_data = data
        self.loading = True

        # Rate limiting: use session_id as unique identifier
        allowed, rate_limit_msg = RateLimiter.is_allowed(self.session_id)
        if not allowed:
            logger.warning("Rate limit hit for session %s", self.session_id)
            yield rx.toast.error(f"⚠️ {rate_limit_msg}", duration=5000, position="top-center")
            self.loading = False
            yield
            return

        logger.info("Form submission initiated for %s", self.sheet_name)
        yield

        try:
            # 1. Validate and convert form data
            logger.debug("Raw form data: %s", data)
            validated_data = FormDataValidator.validate_and_convert(data)
            logger.info("Form data validated: %s", validated_data.model_dump())

            # 2. Get sheets client
            loop = asyncio.get_event_loop()
            client = get_sheets_client(sheet_name=self.sheet_name)

            # 3. Append to spreadsheet
            await loop.run_in_executor(
                None,
                SheetsService.append_row,
                [validated_data.nom, validated_data.telefon, validated_data.persones],
                client,
                self.sheet_name
            )

            logger.info("✅ Form submitted successfully for %s", self.sheet_name)
            yield rx.toast.success("✅ Reserva enviada correctament", duration=3000, position="top-center")

        except ValueError as e:
            # Validation error - user-friendly message
            message = str(e)
            logger.warning("Form validation failed: %s", message)
            yield rx.toast.error(f"⚠️ {message}", duration=5000, position="top-center")

        except Exception as e:
            # Other errors
            message = str(e)
            logger.error("Form submission failed for %s: %s", self.sheet_name, message, exc_info=True)
            yield rx.toast.error(f"❌ Error enviant la reserva: {message}", duration=5000, position="top-center")

        finally:
            self.loading = False
            yield


def formulari():
    return rx.container(
        wrapper(),
        # Occupancy Status Section
        rx.cond(
            FormState.sheet_name == "tast",
            rx.box(
                rx.cond(
                    FormState.is_full,
                    rx.vstack(
                        rx.text("⛔ No s'accepten més sol.licituts!", font_size="18px", font_weight="bold", color="red"),
                        rx.text(f"Actualment tenim {FormState.total_persones} persones registrades (màxim: {FormState.max_persons})",
                            font_size="14px", color="red"),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(f"📊 Lugares disponibles: {FormState.spots_left}/{FormState.max_persons}",
                            font_size="16px", font_weight="bold", color="green"),
                        spacing="2",
                        width="100%",
                    ),
                ),
                border="1px solid",
                border_radius="10px",
                padding="15px",
                margin_bottom="20px",
                background_color=rx.cond(FormState.is_full, "#ffe6e6", "#e6ffe6"),
            ),
            None,
        ),
        # Form (hide only if tast is full)
        rx.cond(
            rx.cond(FormState.sheet_name == "tast", FormState.is_full, False),
            None,
            rx.form(
                rx.vstack(
                    rx.form.field(
                        rx.form.label('Formulari de participació', font_size="24px", font_weight="bold", margin_bottom="16px"),
                        rx.flex(
                            rx.form.label("Nom"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Nom i cognoms",
                                    type="text",
                                    pattern="[A-Za-záéíóú']+",
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
                            rx.form.label("Telèfon"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Telèfon (9 dígits)",
                                    type="string",
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
                                "El telèfon ha de tenir exactament 9 dígits",
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
                            rx.form.label("Participants"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Nombre de persones (1-40)",
                                    type="string",
                                    pattern="^[1-9][0-9]?$|^40$",
                                    required=True,
                                    radius="small",
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "Nombre obligatori entre 1 i 40",
                                match="valueMissing",
                                color="red"
                            ),
                            rx.form.message(
                                "Nombre de participants entre 1 i 40",
                                match="patternMismatch",
                                color="orange"
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="persones",
                        width="100%",
                    ),
                    rx.button(
                        rx.cond(
                            FormState.loading,
                            rx.hstack(rx.spinner(), rx.text("Enviant...")),
                            rx.text("Enviar participació")
                        ),
                        is_disabled=FormState.loading,
                        type="submit",
                        width="100%",
                        radius="small",
                        cursor=rx.cond(FormState.loading,
                            "not-allowed",
                            "pointer"
                        ),
                    ),
                ),
                on_submit=FormState.handle_submit,
                reset_on_submit=True,
                border="1px solid",
                border_radius="10px",
                padding="20px",
                spacing="15px",
            ),
        ),
        rx.divider(),
        on_mount=FormState.load_occupancy,
    )
