from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Go to the app
    page.goto("http://localhost:8501")

    # Fill out the form for a critical patient
    page.get_by_label("Full Name").fill("Critical Patient")
    page.get_by_label("Age").fill("50")

    # Open the critical symptoms expander
    page.get_by_text("Critical Emergency Symptoms").click()

    # Click the multiselect input to open the dropdown
    page.locator('[data-testid="stMultiSelect"]').first.click()

    # Select the "Severe chest pain" option
    page.get_by_text("Severe chest pain").click()

    # Click the expander title again to close the dropdown
    page.get_by_text("Critical Emergency Symptoms").click()

    # Submit the form
    page.get_by_role("button", name="Complete Medical Check-in").click()

    # Wait for the dashboard header to appear
    dashboard_header = page.get_by_role("heading", name="🩺 Triage Dashboard")
    expect(dashboard_header).to_be_visible(timeout=15000)

    # Now that the dashboard is visible, let's take the screenshot.
    page.screenshot(path="jules-scratch/verification/final_dashboard.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)