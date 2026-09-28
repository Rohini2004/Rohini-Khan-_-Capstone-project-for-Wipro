from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from datetime import datetime



#READ TEST DATA FROM JSON


with open("test_data/test_data.json", "r") as file:
    test_data = json.load(file)

username_data = test_data["username"]
password_data = test_data["password"]
product_data = test_data["product"]

print("Test data loaded successfully!")


# CREATE FOLDERS AND REPORT


os.makedirs("reports", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

report_path = "reports/execution_report.txt"

with open(report_path, "w") as report:
    report.write("SELENIUM CAPSTONE ASSIGNMENT 1 - EXECUTION REPORT\n")
    report.write("=" * 60 + "\n")
    report.write(f"Execution Date: {datetime.now()}\n")
    report.write("Application: SauceDemo\n")
    report.write("Browser: Google Chrome\n")
    report.write("=" * 60 + "\n\n")


def write_report(test_name, status, details=""):
    with open(report_path, "a") as report:
        report.write(f"{test_name:<35} : {status}\n")
        if details:
            report.write(f"Details: {details}\n")
        report.write("-" * 60 + "\n")


print("Execution report created!")


# LAUNCH BROWSER


driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 10)

driver.get("https://www.saucedemo.com/")

write_report(
    "Browser Launch",
    "PASS",
    "SauceDemo opened successfully"
)



#LOGIN

try:
    username = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    username.send_keys(username_data)

    password = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password.send_keys(password_data)

    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )
    login_button.click()

    products_title = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    if products_title.text == "Products":
        print("LOGIN SUCCESSFUL!")
        print("Products page opened successfully.")
        write_report("Login", "PASS", "Products page opened successfully")
    else:
        print("LOGIN FAILED!")
        write_report("Login", "FAIL", "Products page was not opened")

except Exception as e:
    print("LOGIN FAILED!")
    print("Error:", e)
    write_report("Login", "FAIL", str(e))


# FIND PRODUCT


try:
    product = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[text()='{product_data}']")
        )
    )

    print("Product found:", product.text)

    write_report(
        "Product Search",
        "PASS",
        f"Product found: {product.text}"
    )

except Exception as e:
    print("Product search failed!")
    write_report("Product Search", "FAIL", str(e))



#ADD PRODUCT TO CART

try:
    add_to_cart_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//div[text()='{product_data}']"
                "/ancestor::div[@class='inventory_item']"
                "//button"
            )
        )
    )

    add_to_cart_button.click()

    print(f"{product_data} added to cart!")

    write_report(
        "Add Product to Cart",
        "PASS",
        f"{product_data} added successfully"
    )

except Exception as e:
    print("Failed to add product to cart!")
    write_report("Add Product to Cart", "FAIL", str(e))


#VERIFY CART


try:
    cart_badge = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    if cart_badge.text == "1":
        print("CART VERIFICATION SUCCESSFUL!")
        print("Cart contains 1 product.")

        write_report(
            "Cart Verification",
            "PASS",
            "Cart contains 1 product"
        )
    else:
        print("CART VERIFICATION FAILED!")
        print("Cart badge shows:", cart_badge.text)

        write_report(
            "Cart Verification",
            "FAIL",
            f"Cart badge shows {cart_badge.text}"
        )

except Exception as e:
    print("CART VERIFICATION FAILED!")
    print("Error:", e)

    write_report(
        "Cart Verification",
        "FAIL",
        str(e)
    )



#OPEN CART


try:
    cart_icon = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    cart_icon.click()

    print("Cart page opened successfully.")

    write_report(
        "Open Cart",
        "PASS",
        "Cart page opened successfully"
    )

except Exception as e:
    print("Failed to open cart!")
    write_report("Open Cart", "FAIL", str(e))


#VERIFY PRODUCT


try:
    cart_product = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    if cart_product.text == product_data:
        print("PRODUCT VERIFICATION SUCCESSFUL!")
        print("Product in cart:", cart_product.text)

        write_report(
            "Product Verification",
            "PASS",
            f"Product in cart: {cart_product.text}"
        )
    else:
        print("PRODUCT VERIFICATION FAILED!")

        write_report(
            "Product Verification",
            "FAIL",
            f"Unexpected product: {cart_product.text}"
        )

except Exception as e:
    print("Product verification failed!")
    write_report("Product Verification", "FAIL", str(e))


#VERIFY PRODUCT QUANTITY

try:
    quantity = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart_quantity"))
    )

    current_quantity = quantity.text

    print("Product quantity:", current_quantity)

    if current_quantity == "1":
        print("QUANTITY VERIFICATION SUCCESSFUL!")
        print("Note: SauceDemo does not provide an option to manually update")
        print("the quantity of the same product in the cart.")

        write_report(
            "Quantity Verification",
            "PASS",
            "Product quantity verified as 1. "
            "SauceDemo does not provide an editable quantity control."
        )
    else:
        print("QUANTITY VERIFICATION FAILED!")

        write_report(
            "Quantity Verification",
            "FAIL",
            f"Expected quantity 1, but found {current_quantity}"
        )

except Exception as e:
    print("Quantity verification failed!")
    print("Error:", e)

    write_report(
        "Quantity Verification",
        "FAIL",
        str(e)
    )

#CART SCREENSHOT


try:
    screenshot_path = "screenshots/cart_page.png"

    driver.save_screenshot(screenshot_path)

    print("Screenshot captured successfully!")
    print("Screenshot saved at:", screenshot_path)

    write_report(
        "Cart Screenshot",
        "PASS",
        screenshot_path
    )

except Exception as e:
    print("Screenshot failed!")
    write_report("Cart Screenshot", "FAIL", str(e))


#CHECKOUT


try:
    checkout_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "checkout")
        )
    )

    checkout_button.click()

    print("Checkout page opened successfully.")

    write_report(
        "Open Checkout",
        "PASS",
        "Checkout page opened successfully"
    )

except Exception as e:
    print("Failed to open checkout!")
    write_report("Open Checkout", "FAIL", str(e))


#ENTER CUSTOMER INFORMATION

checkout_info_success = False

try:
    first_name = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "first-name")
        )
    )
    first_name.clear()
    first_name.send_keys("Rohini")

    last_name = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "last-name")
        )
    )
    last_name.clear()
    last_name.send_keys("Khan")

    postal_code = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "postal-code")
        )
    )
    postal_code.clear()
    postal_code.send_keys("700001")

    print("Customer information entered successfully.")

    write_report(
        "Customer Information",
        "PASS",
        "First name, last name and postal code entered"
    )

    checkout_info_success = True

except Exception as e:
    print("Failed to enter customer information!")
    print("Error:", e)

    write_report(
        "Customer Information",
        "FAIL",
        str(e)
    )


#CONTINUE TO OVERVIEW

checkout_overview_success = False

if checkout_info_success:

    try:
        continue_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "continue")
            )
        )

        continue_button.click()

        # Wait for the checkout overview product to appear
        checkout_product = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "inventory_item_name")
            )
        )

        print("Checkout overview opened successfully.")
        print("Checkout product:", checkout_product.text)

        write_report(
            "Checkout Overview",
            "PASS",
            "Checkout overview displayed successfully"
        )

        checkout_overview_success = True

    except Exception as e:

        print("Checkout overview verification failed!")
        print("Error:", e)

        write_report(
            "Checkout Overview",
            "FAIL",
            str(e)
        )

else:

    print("Checkout overview skipped.")

    write_report(
        "Checkout Overview",
        "SKIPPED",
        "Customer information was not entered"
    )

#VERIFY PRODUCT ON CHECKOUT OVERVIEW

checkout_product_success = False

if checkout_overview_success:

    try:

        if checkout_product.text == product_data:

            print("CHECKOUT PRODUCT VERIFICATION SUCCESSFUL!")

            write_report(
                "Checkout Product Verification",
                "PASS",
                f"Product verified: {checkout_product.text}"
            )

            checkout_product_success = True

        else:

            print("CHECKOUT PRODUCT VERIFICATION FAILED!")

            write_report(
                "Checkout Product Verification",
                "FAIL",
                f"Expected: {product_data}, Found: {checkout_product.text}"
            )

    except Exception as e:

        print("Checkout product verification failed!")

        write_report(
            "Checkout Product Verification",
            "FAIL",
            str(e)
        )

else:

    print("Checkout product verification skipped.")

    write_report(
        "Checkout Product Verification",
        "SKIPPED",
        "Checkout overview was not reached"
    )

#FINISH ORDER


order_completed = False

if checkout_product_success:

    try:
        finish_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "finish")
            )
        )

        finish_button.click()

        confirmation = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "complete-header")
            )
        )

        if confirmation.text == "Thank you for your order!":

            print("ORDER COMPLETED SUCCESSFULLY!")
            print("Confirmation:", confirmation.text)

            write_report(
                "Complete Order",
                "PASS",
                "Order completed successfully"
            )

            order_completed = True

        else:

            print("ORDER COMPLETION VERIFICATION FAILED!")

            write_report(
                "Complete Order",
                "FAIL",
                f"Unexpected confirmation: {confirmation.text}"
            )

    except Exception as e:

        print("Order completion failed!")
        print("Error:", e)

        write_report(
            "Complete Order",
            "FAIL",
            str(e)
        )

else:

    print("Order completion skipped.")

    write_report(
        "Complete Order",
        "SKIPPED",
        "Checkout product verification was not completed"
    )



#FINAL SCREENSHOT


if order_completed:

    try:
        final_screenshot = "screenshots/order_confirmation.png"

        driver.save_screenshot(final_screenshot)

        print("Final screenshot captured successfully!")
        print("Screenshot saved at:", final_screenshot)

        write_report(
            "Order Confirmation Screenshot",
            "PASS",
            final_screenshot
        )

    except Exception as e:

        print("Final screenshot failed!")

        write_report(
            "Order Confirmation Screenshot",
            "FAIL",
            str(e)
        )

else:

    print("Final order screenshot skipped because order was not completed.")

    write_report(
        "Order Confirmation Screenshot",
        "SKIPPED",
        "Order was not completed"
    )


#HANDLE ALERT IF PRESENT

try:
    alert = WebDriverWait(driver, 3).until(
        EC.alert_is_present()
    )

    print("Alert detected!")
    print("Alert message:", alert.text)

    alert.accept()

    print("Alert handled successfully!")

    write_report(
        "Alert Handling",
        "PASS",
        "Alert detected and accepted"
    )

except Exception:
    print("No alert appeared during the test.")

    write_report(
        "Alert Handling",
        "PASS",
        "No alert appeared during the test"
    )



#COMPLETE REPORT

with open(report_path, "a") as report:
    report.write("\n")
    report.write("=" * 60 + "\n")
    report.write("TEST EXECUTION COMPLETED\n")
    report.write("=" * 60 + "\n")

print("Execution report saved at:", report_path)


#CLOSE BROWSER


time.sleep(3)

driver.quit()

print("Browser closed.")