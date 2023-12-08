import time

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import locale
from datetime import datetime
import requests
import json
from selenium.webdriver.chrome.options import Options
import os

class Tatilbudur:
    def __init__(self, url, checkin, checkout, adult, children, withPerPerson=False):
        self.withPerPerson = withPerPerson
        self.url = url
        self.checkin = checkin
        self.checkout = checkout
        self.adult = adult
        self.children = children

    def get_hotel_info(self):

        locale.setlocale(locale.LC_ALL, '')
        proxy = "eacmyfza-TR-rotate:lngjl9ol3y0vx@p.webshare.io:80"
        driver = Driver(uc=True, headless=True, proxy=proxy, chromium_arg="--blink-settings=imagesEnabled=false --no-sandbox --disable-dev-shm-usage")
        driver.get(self.url)
        time.sleep(1)

        try:
            # inline recursion var.
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='like-btn']"))
            )

            elementHotelId = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='hotelId']"))
            )

            elementProuctLot = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='productLoc']"))
            )

            # located mümkün olduğunda çek
            token = element.get_attribute("data-token")
            hotelId = elementHotelId.get_attribute("value")
            productLot = elementProuctLot.get_attribute("value")
        finally:
            print("")

        driver.execute_script('''window.roomValue="";''')
        js = ''' fetch("https://www.tatilbudur.com/hotel/calculate-room-price", { "headers": { "accept": "*/*", 
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded;charset=UTF-8", "sec-ch-ua": "\\"Google Chrome\\";v=\\"119\\", \\"Chromium\\";v=\\"119\\",\\"Not?A_Brand\\";v=\\"24\\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\\"Windows\\"", "sec-fetch-dest":"empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "x-csrf-token":"GtoGoL4Q8PPGXKKWJk3EeJw6WXIH4YIcxfULQHPp", "x-requested-with": "XMLHttpRequest" }, "referrer":"https://www.tatilbudur.com/susesi-luxury-resort", "referrerPolicy": "strict-origin-when-cross-origin", "body": "_token={token}&productType=hotel&hotelId={hotelId}&selectedRoom=&selectedPricingId=&selectedMealType=&hotelOldId=&productLoc={productLot}&productTypeId=&code=&alertRoom=0&actionPricingId=&currencyId=&actions%5B%5D=0&selectedActionCategory=&hidePrice=0&googleRemarketingCategory=&autoPost=0&isFlightPackage=0&adult={adult}&{child}&isCyprusPackageManual=0&priceConfig=&daterange-1={checkin}+-+{checkout}&checkInDate={checkin}&checkOutDate={checkout}&quickPersonCount=2+Yeti%C5%9Fkin+", "method": "POST", "mode": "cors","credentials": "include" })
          .then(response => response.text())
          .then(data => roomValue=data ?? "...")
          .catch(error => console.error('Error:', error)); '''

        # 4,6 yaşında 2 çocuk geldi diyelim

        try:
            childCount = self.children.split(',').__len__()
            childStr = "child=" + str(childCount)
            for i in range(0, childCount):
                childStr += '&childAge[]=' + str(i)
        except:
            childStr = "child=0"

        js = js.replace('{child}', childStr)
        js = js.replace('{token}', token)
        js = js.replace('{hotelId}', hotelId)
        js = js.replace('{productLot}', productLot)
        js = js.replace('{checkin}', self.checkin)
        js = js.replace('{checkout}', self.checkout)
        js = js.replace('{adult}', self.adult)

        driver.execute_script(js)
        roomValue = driver.execute_script('''return window.roomValue;''')

        while roomValue is None or roomValue == "":
            roomValue = driver.execute_script('''return window.roomValue;''')
            time.sleep(2)

        # $content = json_decode($content)->view;

        content = json.loads(roomValue)

        response = html.fromstring(content['view'])
        roomCount = response.xpath("(//div[@class='room-type-new' and @id])").__len__()
        result = []
        for i in range(1, roomCount):
            contracts = []
            roomName = \
                response.xpath("(//div[@class='room-type-new' and @id])[" + str(i) + "]/div[@class='row']/div[1]/h3")[
                    0].text
            concept = response.xpath("(//div[@class='room-type-new' and @id])[" + str(
                i) + "]//div[contains(@class,'room-detail-box')]/div[1]/div[3]/div[1]/div[1]/div[1]")[0].text or ""

            try:
                warning_div = \
                    response.xpath(
                        "(//div[@class='room-type-new' and @id])[" + str(i) + "]//div[@class='warning-red']")[
                        0].text or "null"
            except:
                warning_div = "null"

            try:
                newPrice = \
                    response.xpath("(//div[@class='room-type-new' and @id])[" + str(i) + "]//div[@class='sell-price']")[
                        0].text
                newPrice = newPrice.replace("₺", "")
                newPrice = newPrice.replace(".", "")
                newPrice = float(newPrice)
                newPrice = locale.currency(newPrice, grouping=True, symbol=False) + " TL"
                oldPrice = \
                    response.xpath("(//div[@class='room-type-new' and @id])[" + str(i) + "]//div[@class='price-real']")[
                        0].text
                oldPrice = oldPrice.replace("₺", "")
                oldPrice = oldPrice.replace(".", "")
                oldPrice = float(oldPrice)
                oldPrice = locale.currency(oldPrice, grouping=True, symbol=False) + " TL"
                totalStay = \
                    response.xpath(
                        "(//div[@class='room-type-new' and @id])[" + str(i) + "]//div[@class='sum-price-text']")[0].text
                discount = response.xpath("(//div[@class='room-type-new' and @id])//div[contains(@class,'discount')]")[
                    0].text.strip()

                if self.withPerPerson == "1" and warning_div == "null":
                    linkContract = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "((//div[@class='room-type-new' and @id])[" + str(
                            i) + "]/div[@class='row']//div[@class='room-calendar']/a)[2]"))
                    )
                    linkContract = linkContract.get_attribute("data-href")
                    contracts = self.get_room_contracts(linkContract, driver)



            except BaseException as e:
                newPrice = 0
                oldPrice = 0
                totalStay = ""
                discount = ""
                print(e)

            if warning_div == "null":
                result.append({
                    "name": roomName,
                    "newPrice": newPrice,
                    "oldPrice": oldPrice,
                    "totalStay": totalStay,
                    "discountPercentage": discount,
                    "roomInfo": [concept],
                    "contracts": contracts

                })
            else:
                result.append({
                    "name": roomName,
                    "newPrice": 0,
                    "oldPrice": 0,
                    "totalStay": totalStay,
                    "discountPercentage": 0,
                    "roomInfo": [concept],
                    "contracts": contracts
                })

        driver.quit()
        return result

    def total_days(self, url, driver):
        js = '''fetch("https://www.tatilbudur.com{url}", {
          "headers": {
            "accept": "*/*",
            "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": "\\"Google Chrome\\";v=\\"119\\", \\"Chromium\\";v=\\"119\\", \\"Not?A_Brand\\";v=\\"24\\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\\"Windows\\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-csrf-token": "GtoGoL4Q8PPGXKKWJk3EeJw6WXIH4YIcxfULQHPp",
            "x-requested-with": "XMLHttpRequest"
          },
          "referrer": "https://www.tatilbudur.com/susesi-luxury-resort",
          "referrerPolicy": "strict-origin-when-cross-origin",
          "body": null,
          "method": "GET",
          "mode": "cors",
          "credentials": "include"
        }) 
            .then(response => response.text())
            .then(data => dayValue=data ?? "...")
            .catch(error => console.error('Error:', error)); '''

        js = js.replace('{url}', url)
        driver.execute_script('''window.dayValue="";''')
        driver.execute_script(js)
        dayValue = driver.execute_script('''return window.dayValue;''')
        while dayValue is None or dayValue == "":
            dayValue = driver.execute_script('''return window.dayValue;''')
            time.sleep(2)
        response = html.fromstring(dayValue)
        return response

    def get_room_contracts(self, url, driver):

        checkin_date = datetime.strptime(self.checkin, "%d.%m.%Y")
        checkout_date = datetime.strptime(self.checkout, "%d.%m.%Y")

        get_day_checkin = checkin_date.day
        get_day_checkout = checkout_date.day
        get_month_checkin = checkin_date.month
        get_month_checkout = checkout_date.month

        total_days = self.total_days(url, driver)
        total_day = total_days.xpath("(//tr/td//span/..)").__len__()
        days = []
        contract = 0

        if get_day_checkin > get_day_checkout:
            for i in range(get_day_checkin, total_day):
                try:
                    contract = total_days.xpath('(//tr/td//span/..)[' + str(i) + ']')[0].text_content().split(' ')[4]
                except:
                    contract = 0

                days.append(contract)

            url = url.replace(f"month={get_month_checkin}", f"month={get_month_checkout}")
            total_days = self.total_days(url, driver)

            for i in range(1, get_day_checkout ):
                try:
                    contract = total_days.xpath('(//tr/td//span/..)[' + str(i) + ']')[0].text_content().split(' ')[4]
                except:
                    contract = 0

                days.append(contract)
        else:
            for i in range(get_day_checkin, get_day_checkout):
                try:
                    contract = total_days.xpath('(//tr/td//span/..)[' + str(i) + ']')[0].text_content().split(' ')[4]
                except BaseException as e:
                    contract = 0
                days.append(contract)
        contracts = days

        return contracts
