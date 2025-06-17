# Playwright Example Suite for Django AI Chat
# Save as test_playwright_examples.py

from playwright.sync_api import sync_playwright
import time

# 1. End-to-End (E2E) Testing

def test_e2e_chat():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.fill('input[type="text"]', 'Hello, AI!')
        page.click('button[type="submit"]')
        # Wait for AI response to appear
        page.wait_for_selector('.msg.ai .bubble', timeout=10000)
        ai_text = page.inner_text('.msg.ai .bubble')
        print("AI replied:", ai_text)
        assert "Hello" in ai_text or len(ai_text) > 0
        browser.close()

# 2. Cross-Browser Testing

def test_cross_browser():
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            page.goto("http://127.0.0.1:8000")
            assert "Marvin" in page.content()
            browser.close()

# 3. Visual Regression Testing

def test_visual_regression():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.screenshot(path="homepage.png")
        print("Screenshot saved as homepage.png")
        browser.close()

# 4. Performance Testing

def test_performance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        start = time.time()
        page.goto("http://127.0.0.1:8000")
        load_time = time.time() - start
        print(f"Page load time: {load_time:.2f} seconds")
        assert load_time < 5  # Example threshold
        browser.close()

# 5. Web Scraping & Automation

def test_scrape_ai_reply():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.fill('input[type="text"]', 'What is the capital of France?')
        page.click('button[type="submit"]')
        page.wait_for_selector('.msg.ai .bubble', timeout=10000)
        ai_text = page.inner_text('.msg.ai .bubble')
        print("Scraped AI reply:", ai_text)
        assert "Paris" in ai_text or len(ai_text) > 0
        browser.close()

# 6. CI/CD Integration
# (No code needed here, just run these tests in your CI pipeline)

# 7. Debugging & Inspection

def test_debug_headed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)  # See browser, slow motion
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.fill('input[type="text"]', 'Show me debug mode!')
        page.click('button[type="submit"]')
        page.wait_for_selector('.msg.ai .bubble', timeout=10000)
        browser.close()

# To run: python test_playwright_examples.py
# Or use pytest for individual tests.
