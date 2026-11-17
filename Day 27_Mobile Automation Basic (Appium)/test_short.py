import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as By

FORMULA = "(15+5)/4+7*3-12/3+(10-4)*2+8"
KEYS = {
    "+": ["Plus", "+"],
    "-": ["Minus", "−", "-"],
    "*": ["Multiply", "×", "x", "*"],
    "/": ["Divide", "÷", "/"],
    "=": ["Equals", "="],
    "(": ["Parenthesis", "Parentheses", "Brackets", "( )", "("],
    ")": ["Parenthesis", "Parentheses", "Brackets", "( )", ")"],
}


def tap(d, names):
    for n in names:
        for by, v in ((By.ACCESSIBILITY_ID, n),
                      (By.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{n}")'),
                      (By.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{n}")')):
            e = d.find_elements(by, v)
            if e:
                e[0].click()
                return
    raise Exception(f"Button not found: {names}")


def test_formula():
    o = UiAutomator2Options()
    o.platform_name = "Android"
    o.udid = "R94Y30HMVCZ"
    o.app_package = "com.sec.android.app.popupcalculator"
    o.no_reset = True
    o.set_capability("appium:appWaitActivity", "*")
    d = webdriver.Remote("http://127.0.0.1:4723", options=o)
    try:
        time.sleep(2)
        tap(d, ["Clear", "C", "AC"])
        for c in FORMULA:
            tap(d, KEYS.get(c, [c]))
        d.save_screenshot("formula_entered.png")
        tap(d, KEYS["="])
        time.sleep(1)
        d.save_screenshot("final_result.png")
        print("Expected:", int(eval(FORMULA)))
    finally:
        d.quit()