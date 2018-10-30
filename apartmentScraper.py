# Web scraper that gathers apartment availability data
# The apartment site is a single page app using Ember.js so needed to use Selenium
# to process the SPA and determine the dynamically generated links for each floorplan's inventory

# TODO Send output to JSON so that it can easily be consumed by a web app

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

baseURL = "https://www.berkshirecommunities.com/apartments/ca/san-diego/the-rey/floor-plans#/categories/all/floorplans"
floorplanList = []  # floorplans that have available units


class Unit:
    def __init__(self, rate, name, date):
        self.rate = rate
        self.name = name
        self.date = date

    def print(self):
        print(self.date + "\t" + self.name + "\t" + self.rate)


class Floorplan:
    def __init__(self, title, beds, baths, size, url):
        self.title = title
        self.beds = beds
        self.baths = baths
        self.size = size
        self.unitURL = url
        self.units = []

    def print(self):
        print(self.title + "\t" + self.beds +
              "\t" + self.baths + "\t" + self.size)

    def printAvailableUnits(self):
        for eachUnit in self.units:
            print(self.title + "\t" + eachUnit.rate + "\t" +
                  eachUnit.name + "\t" + eachUnit.date)


def getFloorplans():
    print("Getting available floorplans...")
    prefixURL = "https://www.berkshirecommunities.com/apartments/ca/san-diego/the-rey/floor-plans"
    postfixURL = "/apartments"
    floorplanGroup = browser.find_element_by_class_name("floorplans")
    floorplans = floorplanGroup.find_elements_by_class_name("floorplan-card")
    for eachFloorplan in floorplans:
        title = eachFloorplan.find_element_by_class_name(
            "floorplan-card-title").text
        beds = eachFloorplan.find_element_by_class_name("unit-beds").text
        baths = eachFloorplan.find_element_by_class_name("unit-baths").text
        size = eachFloorplan.find_element_by_class_name("unit-size").text
        link = eachFloorplan.find_element_by_class_name(
            "floorplan-card-cta").get_attribute("href")

        # Format bedroom description
        if beds == "S Studio":
            beds = "Studio"

        # Reformat available units URL for proper navigation while maintaining browser session
        length = len(link)
        index = link.find("#")
        link = link[-(length - index):]
        link = prefixURL + link + postfixURL

        floorplanList.append(Floorplan(title, beds, baths, size, link))


def getUnits():
    print("Getting available units...")
    for eachFloorplan in floorplanList:
        browser.get(eachFloorplan.unitURL)
        unitList = browser.find_elements_by_class_name("unit-numbers")
        for eachUnit in unitList:
            rate = eachUnit.find_element_by_class_name("unit-rate").text
            name = eachUnit.find_element_by_class_name("unit-name").text
            date = eachUnit.find_element_by_class_name(
                "unit-availability-date").text
            eachFloorplan.units.append(Unit(rate, name, date))


def printAvailableFloorplans():
    for eachFloorplan in floorplanList:
        eachFloorplan.print()
        eachFloorplan.printAvailableUnits()


def printAvailableUnits():
    for eachFloorplan in floorplanList:
        eachFloorplan.printAvailableUnits()


options = Options()
options.headless = True
# Logging Level:
# INFO = 0
# WARNING = 1
# ERROR = 2
# FATAL = 3
options.add_argument('log-level=2')
browser = webdriver.Chrome(options=options)
# Poll the DOM waiting up to 5 seconds for the element to be found
# The main floorplans page can take a while to load the data
browser.implicitly_wait(5)
browser.get(baseURL)

getFloorplans()
getUnits()
printAvailableUnits()
