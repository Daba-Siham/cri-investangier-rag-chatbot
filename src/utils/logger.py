"""Application logging setup shared by API entrypoints."""

import logging


def configure_logging() -> None:
    """Ensure application diagnostics reach the active process console."""
    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
    logging.getLogger("src").setLevel(logging.INFO)
