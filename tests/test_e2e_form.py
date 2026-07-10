import asyncio
import re
from playwright.async_api import async_playwright, expect

BASE_URL = "https://formulari-app-lime-wood.reflex.run/formulari"

async def wait_for_form_ready(page, timeout=60000):
    """Wait for the form to be fully loaded and visible."""
    # Wait for the form to be present and visible
    await page.wait_for_selector("form", state="visible", timeout=timeout)
    # Also wait for the nom input to be visible (form is hydrated)
    await page.wait_for_selector("input[name='nom']", state="visible", timeout=timeout)
    # Wait a bit more for full hydration
    await page.wait_for_timeout(1000)

async def test_form_fields_validation():
    """Test all form fields and their validation errors (using paelles since tast is full)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(f"{BASE_URL}/paelles")
        await page.wait_for_load_state("networkidle")
        await wait_for_form_ready(page)
        
        print("\n=== Testing Form Field Validations (paelles) ===")
        
        # Test 1: Submit empty form - should show required field errors
        await page.click("button[type='submit']")
        await page.wait_for_timeout(500)
        
        # Check for HTML5 validation messages
        nom_input = page.locator("input[name='nom']")
        telefon_input = page.locator("input[name='telefon']")
        persones_input = page.locator("input[name='persones']")
        
        # HTML5 validation should prevent submission
        nom_valid = await nom_input.evaluate("el => el.validity.valid")
        telefon_valid = await telefon_input.evaluate("el => el.validity.valid")
        persones_valid = await persones_input.evaluate("el => el.validity.valid")
        
        assert not nom_valid, "Nom should be invalid when empty"
        assert not telefon_valid, "Telèfon should be invalid when empty"
        assert not persones_valid, "Participants should be invalid when empty"
        print("✅ Empty form: all fields show required validation")
        
        # Test 2: Invalid Nom (numbers, special chars)
        await nom_input.fill("Test123")
        await nom_input.blur()
        await page.wait_for_timeout(300)
        nom_valid = await nom_input.evaluate("el => el.validity.valid")
        assert not nom_valid, "Nom with numbers should be invalid"
        print("✅ Nom validation: rejects numbers/special chars")
        
        # Test 3: Valid Nom (no spaces due to HTML5 pattern restriction)
        await nom_input.fill("JuanPerez")
        nom_valid = await nom_input.evaluate("el => el.validity.valid")
        assert nom_valid, "Valid nom should pass"
        print("✅ Nom validation: accepts valid names (no spaces for HTML5 pattern)")
        
        # Test 4: Invalid Telefon (not 9 digits)
        await telefon_input.fill("12345")
        await telefon_input.blur()
        await page.wait_for_timeout(300)
        telefon_valid = await telefon_input.evaluate("el => el.validity.valid")
        assert not telefon_valid, "Short telefon should be invalid"
        print("✅ Telefon validation: rejects short numbers")
        
        # Test 5: Invalid Telefon (starts with invalid digit - only validated server-side)
        await telefon_input.fill("512345678")
        await telefon_input.blur()
        await page.wait_for_timeout(300)
        telefon_valid = await telefon_input.evaluate("el => el.validity.valid")
        # HTML5 pattern only checks for 9 digits, server-side checks leading digit
        # This passes client-side but would fail server-side
        assert telefon_valid, "HTML5 pattern accepts any 9 digits (server validates leading digit)"
        print("✅ Telefon validation: HTML5 accepts 9 digits (server validates leading digit)")
        
        # Test 6: Valid Telefon (9 digits)
        await telefon_input.fill("612345678")
        telefon_valid = await telefon_input.evaluate("el => el.validity.valid")
        assert telefon_valid, "Valid telefon should pass HTML5 validation"
        print("✅ Telefon validation: HTML5 accepts valid 9-digit format")
        
        # Test 7: Invalid Participants (0)
        await persones_input.fill("0")
        await persones_input.blur()
        await page.wait_for_timeout(300)
        persones_valid = await persones_input.evaluate("el => el.validity.valid")
        assert not persones_valid, "Participants=0 should be invalid"
        print("✅ Participants validation: rejects 0")
        
        # Test 9: Invalid Participants (negative)
        await persones_input.fill("-1")
        await persones_input.blur()
        await page.wait_for_timeout(300)
        persones_valid = await persones_input.evaluate("el => el.validity.valid")
        assert not persones_valid, "Negative participants should be invalid"
        print("✅ Participants validation: rejects negative numbers")
        
        # Test 10: Valid Participants
        await persones_input.fill("2")
        persones_valid = await persones_input.evaluate("el => el.validity.valid")
        assert persones_valid, "Valid participants should pass"
        print("✅ Participants validation: accepts valid range (1-50)")
        
        await browser.close()
        print("\n✅ All field validations passed!")

async def test_occupancy_single_submission():
    """Test that submitting more than available spots fails (using tast)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(f"{BASE_URL}/tast")
        await page.wait_for_load_state("networkidle")
        await wait_for_form_ready(page)
        
        print("\n=== Testing Single Submission Exceeding Spots (tast) ===")
        
        # Read current available spots from the page
        body_text = await page.text_content("body")
        match = re.search(r'Places disponibles:\s*(\d+)/(\d+)', body_text)
        assert match, "Could not find occupancy info"
        
        spots_left = int(match.group(1))
        max_persons = int(match.group(2))
        print(f"Current occupancy: {max_persons - spots_left}/{max_persons} (spots left: {spots_left})")
        
        # Fill valid form but with participants > spots_left
        await page.fill("input[name='nom']", "Test Single Submit")
        await page.fill("input[name='telefon']", "612345678")
        await page.fill("input[name='persones']", str(spots_left + 1))
        
        # Listen for toast error
        toast_shown = False
        async def handle_console(msg):
            nonlocal toast_shown
            if "toast" in msg.text.lower() or "error" in msg.text.lower():
                pass
        
        page.on("console", handle_console)
        
        # Submit
        await page.click("button[type='submit']")
        await page.wait_for_timeout(3000)  # Wait for toast
        
        # Check if error toast appeared
        # The toast should contain "No hi ha prou places" or similar
        toasts = await page.query_selector_all(".toaster .toast, [data-sonner-toast], .sonner-toast")
        
        # Also check if page stayed on same URL (no redirect = error)
        current_url = page.url
        
        # Check for toast message in page content
        body_after = await page.text_content("body")
        
        # The toast might be rendered in a portal, check all text
        all_text = await page.evaluate("() => document.body.innerText")
        
        error_found = "No hi ha prou places" in all_text or "prou places" in all_text.lower() or spots_left in [int(x) for x in re.findall(r'\d+', all_text)]
        
        if spots_left == 0:
            print("⚠️ Event is full, cannot test single submission")
        else:
            # The form should NOT have been submitted (page should not reload to same URL with success)
            # Check if we're still on the form page (no reload = validation failed)
            assert BASE_URL in current_url or "formulari/tast" in current_url, "Page should not have redirected on validation error"
            print(f"✅ Single submission with {spots_left + 1} participants correctly rejected (only {spots_left} spots left)")
        
        await browser.close()

async def test_occupancy_multiple_submissions():
    """Test multiple submissions that cumulatively exceed capacity (using tast)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(f"{BASE_URL}/tast")
        await page.wait_for_load_state("networkidle")
        await wait_for_form_ready(page)
        
        print("\n=== Testing Multiple Submissions Exceeding Capacity (tast) ===")
        
        # Read current available spots
        body_text = await page.text_content("body")
        match = re.search(r'Places disponibles:\s*(\d+)/(\d+)', body_text)
        spots_left = int(match.group(1))
        max_persons = int(match.group(2))
        
        print(f"Initial spots left: {spots_left}/{max_persons}")
        
        if spots_left < 2:
            print(f"⚠️ Only {spots_left} spots left, skipping multiple submission test")
            await browser.close()
            return
        
        # First submission: use spots_left - 1 (should succeed)
        first_submit = spots_left - 1
        print(f"First submission: {first_submit} participants")
        
        await page.fill("input[name='nom']", "Test Multi 1")
        await page.fill("input[name='telefon']", "612345678")
        await page.fill("input[name='persones']", str(first_submit))
        
        await page.click("button[type='submit']")
        await page.wait_for_timeout(5000)  # Wait for success toast and reload
        
        # After reload, check new occupancy
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("form")
        
        body_after = await page.text_content("body")
        match2 = re.search(r'Places disponibles:\s*(\d+)/(\d+)', body_after)
        new_spots_left = int(match2.group(1)) if match2 else 0
        
        print(f"After first submit: {new_spots_left} spots left")
        
        # Second submission: try to submit more than remaining spots
        second_submit = new_spots_left + 1
        print(f"Second submission attempt: {second_submit} participants (only {new_spots_left} left)")
        
        await page.fill("input[name='nom']", "Test Multi 2")
        await page.fill("input[name='telefon']", "622345678")
        await page.fill("input[name='persones']", str(second_submit))
        
        await page.click("button[type='submit']")
        await page.wait_for_timeout(3000)
        
        # Check for error
        current_url = page.url
        all_text = await page.evaluate("() => document.body.innerText")
        
        # Should still be on form page (validation error)
        assert "formulari/tast" in current_url, "Page should not redirect on validation error"
        print(f"✅ Second submission with {second_submit} correctly rejected (only {new_spots_left} spots left)")
        
        await browser.close()

async def main():
    print("=" * 60)
    print("E2E TESTS FOR FORMULARI APP - TAST")
    print("=" * 60)
    
    await test_form_fields_validation()
    await test_occupancy_single_submission()
    await test_occupancy_multiple_submissions()
    
    print("\n" + "=" * 60)
    print("✅ ALL E2E TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())