import os
import supervisely as sly


def _download_js_bundle_files():
    """
    Temporarily fix: Downloads JS and CSS files for the app.
    """
    js_link = "https://github.com/supervisely-ecosystem/solution-object-detection/releases/download/v0.0.1/sly-app-widgets-2.2.3.bundle.js"
    css_link = "https://github.com/supervisely-ecosystem/solution-object-detection/releases/download/v0.0.1/sly-app-widgets-2.2.3.bundle.css"

    sly.logger.info("Downloading JS and CSS files for the app...")

    static_dir = "static"
    sly.fs.mkdir(static_dir, True)

    js_path = os.path.join(static_dir, "sly-app-widgets-2.2.3.bundle.js")
    css_path = os.path.join(static_dir, "sly-app-widgets-2.2.3.bundle.css")

    if not sly.fs.file_exists(js_path):
        sly.fs.download(js_link, js_path)
        sly.logger.info("JS file downloaded successfully.")

    if not sly.fs.file_exists(css_path):
        sly.fs.download(css_link, css_path)
        sly.logger.info("CSS file downloaded successfully.")

    # check if files exist
    if not os.path.exists(js_path) or not os.path.exists(css_path):
        raise FileNotFoundError("Failed to download JS and CSS files for the app.")
