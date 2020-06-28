from bs4 import BeautifulSoup
import requests
from Model import Jewellery
import xlsxwriter

class PandoraScrapping:
    pandoraMainUrl = 'https://uk.pandora.net/en/'

    def __init__(self):
        self.jewellery = []

    def getJewellery(self):  # method with self argument
        try:
            self.page = requests.get(self.pandoraMainUrl)
            print("Request is correct")

        except:
            print("Ups! Something is wrong")

        details_html = BeautifulSoup(self.page.content, 'html.parser')
        types = details_html.find_all('div', class_='ci-button-large-fix ci-button-text-black-pink-underlined')
        links = []
        grid = details_html.find('div', class_='ci-m38-categories-teaser-grid')
        children = grid.findChildren("a", recursive=False)
        for child in children:
            print(child['href'])




    def getJewelleryByType(self, url, type):
        TypeJewellery = requests.get(url)
        details_html = BeautifulSoup(TypeJewellery.content, 'html.parser')
        titles = details_html.find_all('a', class_='product-name js-name-link')
        prices = details_html.find_all('span', attrs={'class': 'price-sales ProdPrice__regularPrice'})
        JewelleryList = []
        for index, title in enumerate(titles):
            titles[index] = titles[index].text.replace('\n', '')
            prices[index] = prices[index].text.replace('\n', '')
            # currentTitle = titles[index]
            # currentPrice = prices[index]
            DataJewellery = Jewellery(titles[index], prices[index], type)
            JewelleryList.append(DataJewellery)  # add to the list data

        return JewelleryList

class ExportController(PandoraScrapping):
    def exportToDatabase(self):
        pass
    def exportToXLSX(self):
        tableTitle = [
            "Type",
            "Title",
            "Price"]
        workbook = xlsxwriter.Workbook("ProductAnalysis.xlsx")
        worksheet = workbook.add_worksheet()
        row = 0
        column = 0
        while (column<len(tableTitle)):
            worksheet.write(row, column, tableTitle[column])
            column += 1

        for


        workbook.close()


# pandora = PandoraScrapping()  # creating the object
pandora = ExportController()
pandora.getJewellery()

pandora.exportToXLSX()

