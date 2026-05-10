import time, argparse
from playwright.sync_api import sync_playwright

COOKIES = [
  {"domain": "app.kilo.ai", "hostOnly": True, "httpOnly": True, "name": "__Host-next-auth.csrf-token", "path": "/", "sameSite": "Lax", "secure": True, "session": True, "storeId": "0", "value": "0555d8751835dc23c83f4fa6182b67f01189f17a6af8b7f14550a5caac3a929b%7C7f091ec706bd86b4021bf8c6c1852fa8ea30f2accd2d82c42709ec6a2f346d73"},
  {"domain": "app.kilo.ai", "hostOnly": True, "httpOnly": True, "name": "__Secure-next-auth.callback-url", "path": "/", "sameSite": "Lax", "secure": True, "session": True, "storeId": "0", "value": "https%3A%2F%2Fapp.kilo.ai%2Fusers%2Fafter-sign-in%3FcallbackPath%3D%252Forganizations%252Fnew"},
  {"domain": "app.kilo.ai", "hostOnly": True, "httpOnly": True, "name": "_vcrr_99197b56da7577df", "path": "/", "sameSite": "None", "secure": True, "session": True, "storeId": "0", "value": "dpl_Gdigwv88LvHB5PXyGnGMN9sgf1EU|0.9569"},
  {"domain": "app.kilo.ai", "expirationDate": 1778919804.797917, "hostOnly": True, "httpOnly": False, "name": "sidebar_state", "path": "/", "sameSite": "Lax", "secure": False, "session": False, "storeId": "0", "value": "true"},
  {"domain": "app.kilo.ai", "expirationDate": 1781018088.239968, "hostOnly": True, "httpOnly": True, "name": "__Secure-next-auth.session-token", "path": "/", "sameSite": "Lax", "secure": True, "session": False, "storeId": "0", "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..-r2uvvFBV3P_LGfA.UYd5Kj6W9FcN0R8Wad0VBPJTJoyNmOJd2OppO7pn03rx2gNQ-NjBWKLIC179qoJr9M5FB6D3hotsjQsjj2X214pnPpt3F5ATdQ5FF2Wh2wT1YJrjy4t2JFeGZ1e0AfqziMYmt-v89yHjQtZffvFHORurpAYiB0TNJT0-UqstQA5X9gearaewU2GWWskNjZx4NSGpPL5zO32sfpqUUE86511YVtss-7xpPU5QfEHfbKbx-EZLJwd9f5_KLv-Evrnd0_K3bEIhgPPhu01rYEpHkeMyp5N6OwUU681OpeJUCIRShJCZwo-Rm_6QDHPhnRSp2xutOD52LfUYiLen8yEg7g9HFemkKDdVxAoxEIpOzpOro0QGZJJRlBndO6lhwe9YM706kLxvMwcXDcTEhAzPVx1SMZbGBsdC5T-RHbIMUkieWVCMj2XxUtdtwj_dmP0fTWUeVaLKSTU.2PJhpcbvKQD2b92wvAy_gw"},
  {"domain": ".kilo.ai", "expirationDate": 1793978393.343434, "hostOnly": False, "httpOnly": False, "name": "ph_phc_GK2Pxl0HPj5ZPfwhLRjXrtdz8eD7e9MKnXiFrOqnB6z_posthog", "path": "/", "sameSite": "Lax", "secure": True, "session": False, "storeId": "0", "value": "%7B%22%24device_id%22%3A%22019df819-6339-7105-b771-8d79648892b5%22%2C%22distinct_id%22%3A%22karenpeters65%40my.healingheartmission.org%22%2C%22%24sesid%22%3A%5B1778426393341%2C%22019e1270-ecd1-7455-9f72-6d5d24925dca%22%2C1778425851068%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fkilo.ai%2F%22%7D%2C%22%24user_state%22%3A%22identified%22%7D"}
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
    launch_args += ["--disable-gpu", "--single-process"]

def start_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=bool(args.h), args=launch_args)
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
        reduced_motion="reduce",
    )
    context.add_cookies(COOKIES)
    pages = []
    for i, url in enumerate(URLS):
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        pages.append(page)
        print(f"Tab {i+1}: {url}", flush=True)
    return p, browser, context, pages

p, browser, context, pages = start_browser()
print("All tabs open. Reloading every 5min...", flush=True)
cycle = 1

while True:
    time.sleep(300)
    print(f"=== Reload cycle {cycle} ===", flush=True)
    crashed = False
    for i, page in enumerate(pages):
        try:
            page.reload(wait_until="domcontentloaded", timeout=60000)
            print(f"  Tab {i+1} reloaded", flush=True)
            time.sleep(10)
        except Exception as e:
            print(f"  Tab {i+1} failed: {e}", flush=True)
            crashed = True
            break
    if crashed:
        print("  Browser crashed, restarting...", flush=True)
        try:
            browser.close()
        except:
            pass
        try:
            p.stop()
        except:
            pass
        time.sleep(5)
        p, browser, context, pages = start_browser()
        print("  Browser restarted.", flush=True)
    cycle += 1
