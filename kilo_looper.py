import argparse
import asyncio
from playwright.async_api import async_playwright

COOKIES = [
  {"domain": "app.kilo.ai", "hostOnly": True, "httpOnly": True, "name": "__Host-next-auth.csrf-token", "path": "/", "sameSite": "Lax", "secure": True, "session": True, "storeId": "0", "value": "0555d8751835dc23c83f4fa6182b67f01189f17a6af8b7f14550a5caac3a929b%7C7f091ec706bd86b4021bf8c6c1852fa8ea30f2accd2d82c42709ec6a2f346d73"},
  {"domain": "app.kilo.ai", "hostOnly": True, "httpOnly": True, "name": "__Secure-next-auth.callback-url", "path": "/", "sameSite": "Lax", "secure": True, "session": True, "storeId": "0", "value": "https%3A%2F%2Fapp.kilo.ai%2Fusers%2Fafter-sign-in%3FcallbackPath%3D%252Forganizations%252Fnew"},
  {"domain": "app.kilo.ai", "hostOnly": True, "httpOnly": True, "name": "_vcrr_99197b56da7577df", "path": "/", "sameSite": "None", "secure": True, "session": True, "storeId": "0", "value": "dpl_Gdigwv88LvHB5PXyGnGMN9sgf1EU|0.9569"},
  {"domain": "app.kilo.ai", "expirationDate": 1778919804.797917, "hostOnly": True, "httpOnly": False, "name": "sidebar_state", "path": "/", "sameSite": "Lax", "secure": False, "session": False, "storeId": "0", "value": "true"},
  {"domain": "app.kilo.ai", "expirationDate": 1781018088.239968, "hostOnly": True, "httpOnly": True, "name": "__Secure-next-auth.session-token", "path": "/", "sameSite": "Lax", "secure": True, "session": False, "storeId": "0", "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..-r2uvvFBV3P_LGfA.UYd5Kj6W9FcN0R8Wad0VBPJTJoyNmOJd2OppO7pn03rx2gNQ-NjBWKLIC179qoJr9M5FB6D3hotsjQsjj2X214pnPpt3F5ATdQ5FF2Wh2wT1YJrjy4t2JFeGZ1e0AfqziMYmt-v89yHjQtZffvFHORurpAYiB0TNJT0-UqstQA5X9gearaewU2GWWskNjZx4NSGpPL5zO32sfpqUUE86511YVtss-7xpPU5QfEHfbKbx-EZLJwd9f5_KLv-Evrnd0_K3bEIhgPPhu01rYEpHkeMyp5N6OwUU681OpeJUCIRShJCZwo-Rm_6QDHPhnRSp2xutOD52LfUYiLen8yEg7g9HFemkKDdVxAoxEIpOzpOro0QGZJJRlBndO6lhwe9YM706kLxvMwcXDcTEhAzPVx1SMZbGBsdC5T-RHbIMUkieWVCMj2XxUtdtwj_dmP0fTWUeVaLKSTU.2PJhpcbvKQD2b92wvAy_gw"},
]

URLS = [
    "https://app.kilo.ai/app-builder/9251d86b-5f55-4929-be1a-4e8c73b9b4ce",
    "https://app.kilo.ai/app-builder/270d6dde-6734-48a8-bf60-ec8c2f36f153",
    "https://app.kilo.ai/app-builder/8ec50bc1-6e95-4f41-8a1d-cbbb197357cf",
    "https://app.kilo.ai/app-builder/b11a420f-e511-4d8e-ac2d-2f94c32d6278",
    "https://app.kilo.ai/app-builder/2a9476e1-0f52-4da6-a44a-0ef9db6481ee",
    "https://app.kilo.ai/app-builder/5d5d2765-de18-4d3d-afd7-6bc8f0c842e0",
    "https://app.kilo.ai/app-builder/f82bf59d-065f-471d-bc90-9f524aefe616",
]

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("-h", type=int, default=0, choices=[0, 1], help="0=headed, 1=headless")
ap.add_argument("--help", action="help", default=argparse.SUPPRESS, help="show this help")
args = ap.parse_args()

launch_args = [
    "--no-sandbox", "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--js-flags=--max_old_space_size=512",
    "--disable-field-trial-config",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
]
if args.h:
    launch_args += ["--disable-gpu", "--process-per-site"]


async def try_goto(page, url, retries=3):
    for a in range(retries):
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)
            return True
        except Exception as e:
            print(f"  Retry {a+1}/{retries} for {url}: {e}", flush=True)
            await asyncio.sleep(10)
    return False


async def open_tab(context, url, retries=3):
    page = await context.new_page()
    if await try_goto(page, url):
        return page
    try:
        await page.close()
    except Exception:
        pass
    return None


async def start_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=bool(args.h), args=launch_args)
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
        reduced_motion="reduce",
    )
    await context.add_cookies(COOKIES)
    pages = []
    for i, url in enumerate(URLS):
        page = await open_tab(context, url)
        if not page:
            continue
        pages.append(page)
        print(f"Tab {i+1}: {url}", flush=True)
        await asyncio.sleep(15)
    if not pages:
        try:
            await browser.close()
        except Exception:
            pass
        try:
            await p.stop()
        except Exception:
            pass
        return None, None, None, None
    return p, browser, context, pages


async def main_loop():
    while True:
        try:
            p, browser, context, pages = await start_browser()
            if not pages:
                print("Browser failed to start, retrying in 30s...", flush=True)
                await asyncio.sleep(30)
                continue
            print("All tabs open. Reloading every 5min...", flush=True)
            cycle = 1
            while True:
                await asyncio.sleep(300)
                print(f"=== Reload cycle {cycle} ===", flush=True)
                for page in pages:
                    try:
                        await page.close()
                    except Exception:
                        pass
                pages = []
                crashed = False
                for i, url in enumerate(URLS):
                    page = await open_tab(context, url)
                    if not page:
                        crashed = True
                        break
                    pages.append(page)
                    print(f"  Tab {i+1} reloaded", flush=True)
                    await asyncio.sleep(10)
                if crashed:
                    raise Exception("browser crashed")
                cycle += 1
        except Exception as e:
            print(f"Error: {e}, restarting in 10s...", flush=True)
            try:
                if browser:
                    await browser.close()
            except Exception:
                pass
            try:
                if p:
                    await p.stop()
            except Exception:
                pass
            await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main_loop())
