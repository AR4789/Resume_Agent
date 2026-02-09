from playwright.sync_api import sync_playwright

def apply_linkedin_job(job_url, resume_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(job_url)
        page.wait_for_timeout(3000)

        page.click("text=Easy Apply")
        page.set_input_files("input[type=file]", resume_path)

        # user completes remaining steps manually
        browser.close()
