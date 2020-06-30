from bs4 import BeautifulSoup
import requests
import pymysql
import requests
import xlsxwriter
import matplotlib
import matplotlib.pyplot as plt
import lxml
import html5lib

import pandas as pd


class Jewellery:
    def __init__(self, title, price,type):
        self.title = title
        self.price = price
        self.type = type


    def __str__(self):
        return '%s; %s; %s' % (self.title, self.price, self.type)

class PandoraScrapping:
    pandoraMainUrl = 'https://uk.pandora.net/'

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
        # print(types)
        children = grid.findChildren("a", recursive=False)
        for child in children:
            link = child['href']
            linksplit= link.split('/')
            type=linksplit[len(linksplit)-2]
            self.getJewelleryByType(link, type)


    def getJewelleryByType(self, url, type):
        TypeJewellery = requests.get(self.pandoraMainUrl + url)
        details_html = BeautifulSoup(TypeJewellery.content, 'html.parser')
        titles = details_html.find_all('a', class_='product-name js-name-link')
        prices = details_html.find_all('span', attrs={'class': 'price-sales ProdPrice__regularPrice'})
        JewelleryList = []
        for index, title in enumerate(titles):
            titles[index] = titles[index].text.replace('\n', '')
            prices[index] = prices[index].text.replace('\n', '')
            currentTitle = titles[index]
            currentPrice = prices[index]
            DataJewellery = Jewellery(titles[index], prices[index], type) #one record
            self.jewellery.append(DataJewellery)  #self.jewellery is a list of records, so adding one record each time to DataJewellery

            # print(str(DataJewellery))
        return JewelleryList


class ExportController(PandoraScrapping):
    def exportToXlsx(self):
        tableTitle = [
            "TITLE",
            "PRICE",
            "TYPE"]
        workbook = xlsxwriter.Workbook('ProductData.xlsx')    # utworzenie pliku excel
        worksheet = workbook.add_worksheet()                    # utworzenie arkusz
        tableFormat = workbook.add_format({'border': 1})
        headerFormat = workbook.add_format({'bold': True, 'bg_color': 'yellow', 'border': 1})
        worksheet.set_column(0, 0, 100)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 30)

        row = 0
        column = 0
        while(column < len(tableTitle)):
            worksheet.write(row, column, tableTitle[column], headerFormat)
            column += 1
        row = 1
        while(row - 1 < len(self.jewellery)):        # petla iterujaca po wierszach
            column = 0
            while(column < len(tableTitle)):    # petla iterujaca po kolumnach
                worksheet.write(row, column, str(self.jewellery[row - 1]).split("; ")[column], tableFormat)
                column += 1
            row += 1
        workbook.close()


    def exportToDatabase(self):
        conn = pymysql.connect("localhost", "pm_user", "pandora", "pandora_db")
        self.connection  = conn.cursor()
        conn.autocommit(True)
        self.connection.execute("DROP TABLE product_list")
        self.connection.execute("CREATE TABLE product_list ("
                   "product_id int primary key auto_increment, "
                   "title varchar(255), "
                   "price varchar(512), "
                   "type varchar(255) "
                   ")")

        for row in self.jewellery:
            self.connection.execute("INSERT INTO product_list VALUES (default, %s,%s,%s)",
                       (row.title, row.price, row.type))



    def generatePieChart(self):
        self.c.execute("SELECT price, (count(*)/(SELECT count(*) FROM product_list))*100 AS count "
                       "FROM product_list GROUP BY price order by count desc limit 10")
        result = self.c.fetchall()
        agg_df = pd.DataFrame(result, columns=['price','count'])
        prices = agg_df['price'].tolist()
        contribution = agg_df['count'].tolist()
        explode = (0.3, 0.2, 0.1, 0, 0, 0, 0, 0,0,0)
        fig1, ax1 = plt.subplots()
        ax1.set_title('Business prices analysis')
        ax1.pie(contribution, explode = explode,  labels=prices, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()


class CLI:
    def __init__(self):
        self.controller = ExportController()
        self.controller.getJewellery()
        self.controller.exportToDatabase()
        # self.pandora = PandoraScrapping()
        while(True):
            print("Welcome to application where you can find title of product: ")
            decision = input("Search for the title of product: \n(Q) - quit").upper()
            if(decision == "Q"):
               break

            else:
               print("Searching for name...")
               self.controller.connection.execute('select * from product_list where title LIKE \'%' +  decision + '%\'')
               rows = (self.controller.connection.fetchall())
               for row in rows:
                   print(row[1])



pandora = PandoraScrapping()
pandora.getJewellery()
CLI()





cs = ExportController()
cs.getTablesByPandas()

cs.getJewellery()
cs.exportToXlsx()

cs.exportToDatabase()

cs.generatePieChart()


