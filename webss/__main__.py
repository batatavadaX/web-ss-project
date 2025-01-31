import re
import sys
import pyppeteer
from fastapi.responses import FileResponse
from temp import tempfile
import uvicorn
import os 

from .import app

port = int(os.environ.get('PORT', 6969))

browser = None
is_browser_started = False

async def start_browser():
    global browser, is_browser_started
    browser = await pyppeteer.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
            )
    is_browser_started = True


@app.get("/")
async def endpoint(site: str):
    """__[Web-SS Endpoint]__
    __Args:__
        `site (str)`: `[website url]`
    __Returns:__
        `[type]`: `[FileResponse]` = image: mime_type: image/png
    
    __Exception:__
        `[error]`: `[pyppeteer.errors]`
    """
    global browser, is_browser_started
    if not is_browser_started:
        print("started")
        await start_browser()
        is_browser_started = True
    page = await browser.newPage()
    if re.match(r'^https?://', site):
        url = site
    else:
        url = 'http://' + site
    page = await browser.newPage()
    file = tempfile() + ".png"
    try:
        await page.goto(url)
        await page.setViewport({'width': 1280, 'height': 720})
    except (
        pyppeteer.errors.NetworkError,
        pyppeteer.errors.PageError
    ) as e:
        return {"error": str(e)}
    await page.screenshot({'path': file})
    return FileResponse(file)


if __name__ == "__main__":
    try:
        uvicorn.run(app=app, host='0.0.0.0', port=port)
    except (KeyboardInterrupt, RuntimeError, RuntimeWarning):
        sys.exit(0)
