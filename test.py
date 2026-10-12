from playwright.sync_api  import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page =browser.new_page()
    page.goto("https://www.ubuy.co.in/search/?q=shoes")
    with page.expect_popup() as popup_info:
         page.locator(".product-image").nth(1).click()
         popup = popup_info.value
         print(popup.title())
         print(popup.url)
         popup.locator("#add-to-cart-btn").click()
         popup.screenshot(path="add_to_cart.png")
         popup.locator("#add-to-cart-view-cart").click()
         popup.screenshot(path="view_cart.png")
         popup.locator("#proceed-to-checkout").click()
         popup.screenshot(path="checkout.png")
         

    browser.close()
  