import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_PRINT_OPTIONS = {
    "paperWidth": 8.27,
    "paperHeight": 11.69,
    "displayHeaderFooter": False,
}


def build_print_options(options: dict = None):
    merged = DEFAULT_PRINT_OPTIONS.copy()
    if options:
        merged.update(options)
    return merged


def check_if_tmp_directory_is_exists_and_writable() -> bool:
    """Check if /tmp directory exists and is writable"""
    try:
        with tempfile.NamedTemporaryFile(dir="/tmp") as tmp:
            tmp.write(b"test")
            tmp.flush()
        return True
    except Exception:
        return False


def generate_pdf(html: str, print_options: dict) -> str:
    """Return base64-encoded pdf"""

    if not check_if_tmp_directory_is_exists_and_writable():
        raise RuntimeError("/tmp directory does not exist or is not writable")

    with tempfile.NamedTemporaryFile(suffix=".html") as tmp:
        tmp.write(html.encode())
        tmp.seek(0)

        driver = build_driver()
        driver.get("file://{}".format(tmp.name))

        pdf = driver.execute_cdp_cmd("Page.printToPDF", print_options)["data"]
        driver.quit()

        return pdf


def build_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--single-process")
    return webdriver.Chrome(options=options)
