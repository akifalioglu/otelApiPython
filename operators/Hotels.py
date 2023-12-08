import json
import time
from datetime import datetime

from seleniumbase import Driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html

import locale


class Hotels:
    hotelId = ""
    regionId = ""

    def __init__(self, url, checkin, checkout, adult, children, currency, withPerPerson=False):
        self.withPerPerson = withPerPerson
        self.url = url
        self.checkin = checkin
        self.checkout = checkout
        self.adult = adult
        self.children = children
        self.currency = currency

    def get_hotel_info(self):
        driver = Driver(uc=True, headless=True, chromium_arg="--blink-settings=imagesEnabled=false")
        driver.get(self.url)
        self.get_hotel_details(driver)

        # Otel için gerekli bilgileri alalım

        checkin_date = datetime.strptime(self.checkin, "%d.%m.%Y")
        checkout_date = datetime.strptime(self.checkout, "%d.%m.%Y")

        get_day_checkin = checkin_date.day
        get_day_checkout = checkout_date.day

        get_month_checkin = checkin_date.month
        get_month_checkout = checkout_date.month

        get_year_checkin = checkin_date.year
        get_year_checkout = checkout_date.year
        child_text = "[]"

        if self.children:
            childExplode = self.children.split(",")
            childCount = len(childExplode)

            if childCount > 0:
                child_text = []
                for i in range(childCount):
                    child_text.append({"age": int(childExplode[i])})
                child_text = json.dumps(child_text)

        driver.execute_script('''window.roomValue="";''')
        js = '''fetch("https://tr.hotels.com/graphql", {
          "headers": {
            "accept": "*/*",
            "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "client-info": "shopping-pwa,fdf8309396733c7e92eee79a70a887347067c674,us-east-1",
            "content-type": "application/json",
            "sec-ch-ua": "\\"Google Chrome\\";v=\\"119\\", \\"Chromium\\";v=\\"119\\", \\"Not?A_Brand\\";v=\\"24\\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\\"Windows\\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-page-id": "page.Hotels.Infosite.Information,H,30",
            "x-parent-brand-id": "hotels",
            "x-product-line": "lodging"
          },
          "referrer": "https://tr.hotels.com/ho276823/susesi-luxury-resort-all-inclusive-belek-turkiye/?chkin=2023-12-10&chkout=2023-12-14&x_pwa=1&rfrr=HSR&pwa_ts=1701942552642&referrerUrl=aHR0cHM6Ly90ci5ob3RlbHMuY29tL0hvdGVsLVNlYXJjaA%3D%3D&useRewards=false&rm1=a2&regionId=6157082&destination=Serik%2C+Antalya+%28b%C3%B6lge%29%2C+T%C3%BCrkiye&destType=MARKET&neighborhoodId=553248633981724295&selected=2169435&latLong=37.199355%2C30.987632&sort=RECOMMENDED&top_dp=27012&top_cur=TRY&userIntent=&selectedRoomType=461677&selectedRatePlan=207953185&expediaPropertyId=2169435&searchId=c6229925-dccd-45ff-bdc9-06f98798f297",
          "referrerPolicy": "strict-origin-when-cross-origin",
          "body": "[{\\"operationName\\":\\"PropertyOffersQuery\\",\\"variables\\":{\\"propertyId\\":\\"{hotelId}\\",\\"searchCriteria\\":{\\"primary\\":{\\"dateRange\\":{\\"checkInDate\\":{\\"day\\":{checkinDay},\\"month\\":{checkinMonth},\\"year\\":{checkinYear}},\\"checkOutDate\\":{\\"day\\":{checkoutDay},\\"month\\":{checkoutMonth},\\"year\\":{checkoutYear}}},\\"destination\\":{\\"regionName\\":\\"Serik, Antalya (bölge), Türkiye\\",\\"regionId\\":\\"6157082\\",\\"coordinates\\":{\\"latitude\\":37.199355,\\"longitude\\":30.987632},\\"pinnedPropertyId\\":\\"2169435\\",\\"propertyIds\\":null,\\"mapBounds\\":null},\\"rooms\\":[{\\"adults\\":{adult},\\"children\\":{children}}]},\\"secondary\\":{\\"counts\\":[],\\"booleans\\":[],\\"selections\\":[{\\"id\\":\\"sort\\",\\"value\\":\\"RECOMMENDED\\"},{\\"id\\":\\"privacyTrackingState\\",\\"value\\":\\"CAN_TRACK\\"},{\\"id\\":\\"useRewards\\",\\"value\\":\\"SHOP_WITHOUT_POINTS\\"}],\\"ranges\\":[]}},\\"shoppingContext\\":{\\"multiItem\\":null},\\"travelAdTrackingInfo\\":null,\\"searchOffer\\":{\\"offerPrice\\":{\\"offerTimestamp\\":\\"1701942552642\\",\\"price\\":{\\"amount\\":27012,\\"currency\\":\\"TRY\\"}},\\"roomTypeId\\":\\"461677\\",\\"ratePlanId\\":\\"207953185\\",\\"offerDetails\\":[]},\\"referrer\\":\\"HSR\\",\\"context\\":{\\"siteId\\":{siteId},\\"locale\\":\\"tr_TR\\",\\"eapid\\":{eapId},\\"currency\\":\\"TRY\\",\\"device\\":{\\"type\\":\\"DESKTOP\\"},\\"identity\\":{\\"duaid\\":\\"9e1e1b29-25da-4073-8fdb-b9ac36003bff\\",\\"expUserId\\":null,\\"tuid\\":null,\\"authState\\":\\"ANONYMOUS\\"},\\"privacyTrackingState\\":\\"CAN_TRACK\\",\\"debugContext\\":{\\"abacusOverrides\\":[]}}},\\"extensions\\":{\\"persistedQuery\\":{\\"version\\":1,\\"sha256Hash\\":\\"824ab2ae3b3c8b9b5e58af26cd7959a7e890316f603d95c7841c0f48c4dfefe0\\"}}}]",
          "method": "POST",
          "mode": "cors",
          "credentials": "include"
        })
            .then(response => response.text())
            .then(data => roomValue=data ?? "...")
            .catch(error => console.error('Error:', error)); '''
        js = js.replace('{hotelId}', self.hotelId)
        js = js.replace('{regionId}', self.regionId)
        js = js.replace('{checkinDay}', str(get_day_checkin))
        js = js.replace('{checkinMonth}', str(get_month_checkin))
        js = js.replace('{checkinYear}', str(get_year_checkin))
        js = js.replace('{checkoutDay}', str(get_day_checkout))
        js = js.replace('{checkoutMonth}', str(get_month_checkout))
        js = js.replace('{checkoutYear}', str(get_year_checkout))
        js = js.replace('{adult}', str(self.adult))
        js = js.replace('{children}', child_text)
        js = js.replace('{siteId}', self.currency_translate()[0])
        js = js.replace('{eapId}', self.currency_translate()[1])

        driver.execute_script(js)

        roomValue = driver.execute_script('''return window.roomValue;''')
        while roomValue is None or roomValue == "":
            roomValue = driver.execute_script('''return window.roomValue;''')
            time.sleep(2)

        # $resultDecode= json_decode($result,true);
        # $resultDecode = $resultDecode[0]['data']['propertyOffers']['categorizedListings'];

        resultDecode = json.loads(roomValue)
        resultDecode = resultDecode[0]['data']['propertyOffers']['categorizedListings']
        return self.hotel_with_price(resultDecode)

    def get_hotel_details(self, driver):
        try:

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'osano-cm-button--type_accept')]"))
            )
            element.click()
            # inline recursion var.

            elementRegionId = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='regionId']"))
            )

            elementHotelId = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='selected']"))
            )
            # located mümkün olduğunda çek
            hotelId = elementHotelId.get_attribute("value")
            regionId = elementRegionId.get_attribute("value")
            self.hotelId = hotelId
            self.regionId = regionId

        except BaseException as e:
            print(e)

    def currency_translate(self):
        currency = self.currency
        if currency == 'TL':
            return ['300000028', '28', 'TL']
        elif currency == 'EUR':
            return ['300000752', '752', '€']
        elif currency == 'USD':
            return ['300000001', '1', '$']
        else:
            return ['300000028', '28', 'TL']

    def hotel_with_price(self, results):
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        checkin = datetime.strptime(self.checkin, "%d.%m.%Y")
        checkout = datetime.strptime(self.checkout, "%d.%m.%Y")
        diff = (checkout - checkin).days
        rooms = []
        for result in results:
            name = result['header']['text']
            try:
                raw_price = \
                    result['primarySelections'][0]['propertyUnit']['ratePlans'][0]['priceDetails'][0][
                        'pricePresentation'][
                        'sections'][1]['header']['enrichedValue']['primaryMessage']['primary']
            except IndexError:
                continue

            discount = result['primarySelections'][0]['propertyUnit']['ratePlans'][0]['badge']['text'] if 'badge' in \
                                                                                                          result[
                                                                                                              'primarySelections'][
                                                                                                              0][
                                                                                                              'propertyUnit'][
                                                                                                              'ratePlans'][
                                                                                                              0] else None
            raw_price = int(''.join(filter(str.isdigit, raw_price)))
            description = result['primarySelections'][0]['propertyUnit']['ratePlans'][0]['amenities']
            description_column = [item['description'] for item in description]
            bool_result_for_concept = self.get_concept(description_column)
            rooms_info = [bool_result_for_concept] if bool_result_for_concept else ["Only Room"]
            new_price = str(raw_price)
            new_price = new_price.replace("₺", "")
            new_price = new_price.replace(".", "")
            new_price = float(new_price)
            new_price = locale.currency(new_price, grouping=True, symbol=False) + " " + self.currency_translate()[2]
            rooms.append(
                {
                    "name": name,
                    "newPrice": new_price,
                    "oldPrice": "",
                    "totalStay": diff,
                    "discountPercentage": discount,
                    "roomInfo": rooms_info,
                    "contracts": [],

                }
            )

            if result['primarySelections'][0]['secondarySelections'][0]['tertiarySelections'] is not None:
                value = result['primarySelections'][0]['secondarySelections'][0]['tertiarySelections']
                for i in range(1, len(value)):
                    rooms_info.append(value[i]['description'])
                    new_price = int(''.join(filter(str.isdigit,
                                                   result['primarySelections'][0]['propertyUnit']['ratePlans'][i][
                                                       'paymentPolicy'][0]['price']['displayMessages'][0]['lineItems'][
                                                       0]['price']['formatted'])))
                    discount = result['primarySelections'][0]['propertyUnit']['ratePlans'][i]['badge'][
                        'text'] if 'badge' in result['primarySelections'][0]['propertyUnit']['ratePlans'][i] else None

                    if self.currency == 'USD':
                        new_price *= diff

                    new_price = str(raw_price)
                    new_price = new_price.replace("₺", "")
                    new_price = new_price.replace(".", "")
                    new_price = float(new_price)
                    new_price = locale.currency(new_price, grouping=True, symbol=False) + " " + \
                                self.currency_translate()[2]
                    rooms.append(
                        {
                            "name": name,
                            "newPrice": new_price,
                            "oldPrice": "",
                            "totalStay": diff,
                            "discountPercentage": discount,
                            "roomInfo": rooms_info,
                            "contracts": [],
                        }
                    )

                    rooms_info = []

        return rooms

    def get_concept(self, features):
        bool_array = [
            "Her Şey Dâhil" in features,
            "Kahvaltı dâhil" in features,
            "All-inclusive" in features,
            any("kahvaltı" in feature for feature in features),
        ]
        bool_translate_array = [
            "Her Şey Dâhil",
            "Kahvaltı dâhil",
            "All-inclusive",
            "Kahvaltı dâhil",
        ]

        result = any(bool_array)
        if result:
            index = bool_array.index(True)
            concept = bool_translate_array[index]
            return concept
        else:
            return None

