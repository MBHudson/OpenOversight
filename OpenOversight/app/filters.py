"""Contains all templates filters."""
from datetime import datetime

import bleach
import markdown as _markdown
import pytz as pytz
from bleach_allowlist import markdown_attrs, markdown_tags
from flask import Flask, session
from markupsafe import Markup

from OpenOversight.app.utils.constants import FIELD_NOT_AVAILABLE, KEY_TIMEZONE


def instantiate_filters(app: Flask):
    """Instantiate all template filters"""

    def get_timezone() -> str:
        """Return the applicable timezone for the filter."""
        return (
            session[KEY_TIMEZONE]
            if KEY_TIMEZONE in session
            else app.config.get(KEY_TIMEZONE)
        )

    @app.template_filter("capfirst")
    def capfirst_filter(s: str) -> str:
        return s[0].capitalize() + s[1:]  # only change 1st letter

    @app.template_filter("get_age")
    def get_age_from_birth_year(birth_year: int) -> int:
        return int(datetime.now(pytz.timezone(get_timezone())).year - birth_year)

    @app.template_filter("field_in_query")
    def field_in_query(form_data, field) -> str:
        """
        Determine if a field is specified in the form data, and if so return a Bootstrap
        class which will render the field accordion open.
        """
        return " in " if form_data.get(field) else ""

    @app.template_filter("markdown")
    def markdown(text: str) -> Markup:
        text = text.replace("\n", "  \n")  # make markdown not ignore new lines.
        html = bleach.clean(_markdown.markdown(text), markdown_tags, markdown_attrs)
        return Markup(html)

    @app.template_filter("display_date")
    def display_date(value: datetime) -> str:
        """Convert UTC datetime.datetime into a localized date string."""
        if value:
            return value.strftime("%b %d, %Y")
        return FIELD_NOT_AVAILABLE

    @app.template_filter("local_date")
    def local_date(value: datetime) -> str:
        """Convert UTC datetime.datetime into a localized date string."""
        if value:
            return value.astimezone(pytz.timezone(get_timezone())).strftime("%b %d, %Y")
        return FIELD_NOT_AVAILABLE

    @app.template_filter("local_date_time")
    def local_date_time(value: datetime) -> str:
        """Convert UTC datetime.datetime into a localized date time string."""
        if value:
            return value.astimezone(pytz.timezone(get_timezone())).strftime(
                "%I:%M %p on %b %d, %Y"
            )
        return FIELD_NOT_AVAILABLE

    @app.template_filter("display_time")
    def display_time(value: datetime) -> str:
        """Convert UTC datetime.datetime into a localized date string."""
        if value:
            return value.strftime("%I:%M %p")
        return FIELD_NOT_AVAILABLE

    @app.template_filter("local_time")
    def local_time(value: datetime) -> str:
        """Convert UTC datetime.datetime into a localized time string."""
        if value:
            return value.astimezone(pytz.timezone(get_timezone())).strftime("%I:%M %p")
        return FIELD_NOT_AVAILABLE

    @app.template_filter("thousands_seperator")
    def thousands_seperator(value: int) -> str:
        """Convert int to string with the appropriately applied commas."""
        return f"{value:,}"
