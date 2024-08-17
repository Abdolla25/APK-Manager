from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
import os
import base64
from datetime import datetime
from .models import App


APPIUM_HOST = os.getenv("APPIUM_HOST", "appium")
APPIUM_PORT = os.getenv("APPIUM_PORT", 4723)


def create_android_driver(custom_options=None):
    """Create an Appium driver for Android."""
    options = UiAutomator2Options()
    if custom_options is not None:
        options.load_capabilities(custom_options)
    return webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}", options=options)


def test_android_run(
    apk_path: str,
    device_id: str,
    app_package: str,
    app: App,
    screenshot_path: str,
    recording_path: str,
) -> None:
    """
    Installs an APK, starts the app, takes a screenshot, clicks an element, takes another screenshot,
    stops the recording, and saves the recordings and screenshots to the database.
    """
    recording_name = f"{app_package}_recording_{os.urandom(5).hex()}.mp4"
    first_screenshot_name = f"{app_package}_first_screenshot_{os.urandom(5).hex()}.png"
    second_screenshot_name = (
        f"{app_package}_second_screenshot_{os.urandom(5).hex()}.png"
    )

    with create_android_driver(
        {"appium:app": apk_path, "appium:udid": device_id}
    ) as driver:
        driver.start_recording_screen()
        driver.activate_app(app_package)
        sleep(5)
        first_screenshot_path = os.path.join(screenshot_path, first_screenshot_name)
        driver.save_screenshot(first_screenshot_path)

        sleep(5)
        clickable_elements = (
            driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
            + driver.find_elements(
                by=AppiumBy.CLASS_NAME, value="android.widget.TextView"
            )
            + driver.find_elements(
                by=AppiumBy.CLASS_NAME, value="android.widget.EditText"
            )
        )
        if clickable_elements:
            clickable_elements[0].click()

        sleep(5)
        second_screenshot_path = os.path.join(screenshot_path, second_screenshot_name)
        driver.save_screenshot(second_screenshot_path)

        screen_changed = first_screenshot_path != second_screenshot_path
        driver.terminate_app(app_package)
        sleep(5)

        recording_base64 = driver.stop_recording_screen()
        recording_path = os.path.join(recording_path, recording_name)
        with open(recording_path, "wb") as f:
            f.write(base64.b64decode(recording_base64))

        app.first_screen_screenshot = first_screenshot_path
        app.second_screen_screenshot = second_screenshot_path
        app.video_recording = recording_path
        app.screen_changed = screen_changed
        app.updated_at = datetime.now()
        app.save()
