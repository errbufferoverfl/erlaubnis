from config.default import Configuration


class DevConfiguration(Configuration):
    """
    The development configuration for this Flask application.
    """

    """
    Project Details
    These are used to pre-fill the Jinja templates.
    """
    TITLE = "Erlaubnis - Development"
    DATABASE_NAME = "dev.db"

    """Flask Configuration"""
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True
