import os
from time import sleep
from random import uniform
from datetime import datetime
from fake_useragent import UserAgent
from colorama import Fore, init, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchWindowException,
    TimeoutException,
    ElementClickInterceptedException,
)
from twilio.rest import Client
import pyautogui

# بيانات Twilio
account_sid = 'NQDCNLQSNCLSDKDFSKFLKFDLKSDFKJLN'
auth_token = 'ijqdioslfioqnoQNVLNVCLDLVCQVMLV'
twilio_number = '+14235654jj'
your_phone_number = '+212RE'

# عميل Twilio
client = Client(account_sid, auth_token)

# روابط الصفحات المستهدفة
target = "https://admission.1337.ma/candidature/piscine"
target_signin = "https://admission.1337.ma/en/users/sign_in"

# بيانات تسجيل الدخول
email = "exampelemail@gmail.com"
password = "**************"

# تهيئة colorama لإعادة تعيين الألوان تلقائيًا بعد كل عملية طباعة
init(autoreset=True)
print(
    """
{dim}{blue}

LeetPoolBot v1.2 (تم اختباره فقط في بيئة محاكاة، شغّله على مسؤوليتك الخاصة)
تم إنشاؤه بواسطة {bright}{red}♥{blue} من إسماعيل
""".format(
        red=Fore.RED, blue=Fore.BLUE, dim=Style.DIM, bright=Style.BRIGHT
    )
)

# إنشاء وكيل مستخدم عشوائي
ua = UserAgent(
    os=["android", "ios"],
    platforms="mobile",
    browsers=["edge", "chrome"],
    min_version=120.0,
)

# تهيئة خيارات Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disk-cache-size=0")
options.add_argument("--start-maximized")
options.add_argument(f"--user-agent={ua.random}")
options.add_extension(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "Buster-Captcha-Solver-for-Humans.zip",
    )
)

def sign_in():
    """
    دالة لتسجيل الدخول إلى الموقع باستخدام بيانات تسجيل الدخول
    """
    try:
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//form/div/button").click()
        WebDriverWait(driver, 2).until(EC.url_changes(target_signin))
        print(f"[{datetime.now()}] {Fore.GREEN}Log in succeeded")
    except:
        print(f"[{datetime.now()}] {Fore.RED}Error: Password or email not verified")

def call_user():
    """
    دالة لإجراء مكالمة هاتفية باستخدام Twilio لإعلام المستخدم بالتحديثات
    """
    message = client.calls.create(
        to=your_phone_number,
        from_=twilio_number,
        twiml="<Response><Say>يوجد أماكن شاغرة الآن في الحرم الجامعي المفضل لديك. يرجى التحقق من الموقع فوراً.</Say></Response>"
    )
    print(f"[{datetime.now()}] {Fore.GREEN}تم إجراء المكالمة لإعلام المستخدم")

def random_scroll():
    """
    دالة لتنفيذ تمرير عشوائي داخل الصفحة لجعل النشاط يبدو أكثر طبيعية
    """
    scroll_amount = uniform(0, 1000)  # قيمة عشوائية للتمرير
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    print(f"[{datetime.now()}] {Fore.CYAN}Scrolled by {scroll_amount} pixels")

def minimize_other_windows(target_window_title):
    """
    تقليص جميع النوافذ إلى شريط المهام ما عدا النافذة التي تحتوي على الصفحة المستهدفة
    """
    all_windows = pyautogui.getWindowsWithTitle("")
    for window in all_windows:
        if window.title != target_window_title:
            window.minimize()

def check_for_updates():
    """
    دالة للتحقق من وجود تحديثات في الصفحة المستهدفة
    """
    global driver

    # إذا كان المستخدم غير مسجل الدخول، قم بتسجيل الدخول
    if driver.current_url == target_signin:
        sign_in()

    # إذا كانت الصفحة الحالية هي الصفحة المستهدفة، قم بإعادة تحميل الصفحة
    if driver.current_url == target:
        driver.get(target)

    try:
        # البحث عن الكلمات المحددة في النص الكامل للصفحة
        words_to_check = ["places", "Places", "Date", "gps", "GPS", "ben", "Ben", "guerir", "Guerir", "Med", "Khouribga", "Tétouan", "robot", "juin", "sept"]
        page_text = driver.find_element(By.XPATH, "//*").text
        if any(word in page_text for word in words_to_check):
            call_user()  # إجراء مكالمة إذا تم العثور على الكلمات المحددة
            minimize_other_windows(driver.title)  # تقليص جميع النوافذ ما عدا النافذة التي تحتوي على الصفحة المستهدفة
        else:
            print(f"[{datetime.now()}] {Fore.YELLOW}No updates found")
        
        # تغيير وكيل المستخدم بعد كل عملية تحقق
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua.random})
        random_scroll()  # تنفيذ تمرير عشوائي داخل الصفحة
    except TimeoutException:
        print(f"[{datetime.now()}] {Fore.YELLOW}The pool not launched now")
    except NoSuchWindowException:
        print(f"[{datetime.now()}] {Fore.RED}Unexpected error: NoSuchWindowException")
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.set_page_load_timeout(30)
        driver.get(target)
        check_for_updates()
    except Exception as e:
        print(f"[{datetime.now()}] {Fore.RED}An error occurred: {str(e)}")

# تشغيل WebDriver وتعيين مهلة لتحميل الصفحة
driver = webdriver.Chrome(service=Service(), options=options)
driver.set_page_load_timeout(30)
driver.get(target)

# حلقة التحقق الرئيسية
while True:
    current_time = datetime.now()
    if current_time.hour >= 3 or current_time.hour < 2:  # التحقق من التوقيت (من الساعة 3 صباحًا حتى الساعة 2 صباحًا)
        check_for_updates()
        sleep(uniform(6, 7))  # فترة الانتظار بين كل عملية تحقق (2 إلى 3 ثوانٍ)
    else:
        driver.quit()
        if current_time.hour < 3:
            until_3am = (
                current_time.replace(hour=3, minute=0, second=0, microsecond=0)
                - current_time
            ).total_seconds()
            print(
                f"[{datetime.now()}] بعد منتصف الليل، سيتم التحقق مرة أخرى حتى الساعة 3 صباحًا في غضون:",
                until_3am,
                "ثوانٍ",
            )
            sleep(until_3am)
        elif current_time.hour >= 2:
            until_3am_tomorrow = (
                current_time.replace(hour=3, minute=0, second=0, microsecond=0)
                - current_time
            ).total_seconds() + 86400  # إضافة عدد الثواني في اليوم للتأكد من التحقق في اليوم التالي
            print(
                f"[{datetime.now()}] بعد الثانية صباحًا، سيتم التحقق مرة أخرى في اليوم التالي في غضون:",
                until_3am_tomorrow,
                "ثوانٍ",
            )
            sleep(until_3am_tomorrow)
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.set_page_load_timeout(30)
        driver.get(target)
