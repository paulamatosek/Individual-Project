from bs4 import BeautifulSoup
import requests
import pymysql
import requests
import xlsxwriter
import matplotlib
import matplotlib.pyplot as plt
import lxml
import html5lib


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

pandora = PandoraScrapping()  # creating the object
pandora.getJewellery()


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
        self.c = conn.cursor()
        conn.autocommit(True)
        self.c.execute("CREATE TABLE product_list ("
                   "product_id int primary key auto_increment, "
                   "title varchar(255), "
                   "price varchar(512), "
                   "type varchar(255), "
                   ")")

        for row in self.jewellery:
            self.c.execute("INSERT INTO product_list VALUES (default, %s,%s,%s)",
                       (row.title, row.price, row.type))


  # def generatePlots(self):
  #       self.c.execute("SELECT title, price, type FROM product_list")
  #       product_list = self.c.fetchall()
  #       product_df = pd.DataFrame(product, columns=['title','price','type'])
  #       counties = risk_df['country'].tolist()[:5]
  #       areas = risk_df['area'].tolist()[:5]
  #       risks = risk_df['risk'].tolist()[:5]
  #       climates = risk_df['climate'].tolist()[:5]
  #
  #       x = pd.np.arange(len(counties))  # the label locations
  #       width = 0.35  # the width of the bars
  #       risks_cat = []
  #       climates_cat = []
  #       for v in risks:
  #           risks_cat.append(categories[v])
  #       for v in climates:
  #           climates_cat.append(categories[v])
  #       fig, ax = plt.subplots()
  #       rects1 = ax.bar(x - width / 2, risks_cat, width, label='Business Risk Asesm.')
  #       rects2 = ax.bar(x + width / 2, climates_cat, width, label='Business Climate Asesm.')
  #       ax.set_ylabel('Categories')
  #       ax.set_title('Business risk & climate assesments')
  #       ax.set_xticks(x)
  #       ax.set_xticklabels(counties)
  #       ax.legend()
  #       fig.tight_layout()
  #       plt.show()



  #
  #   def generatePieChart(self):
  #       self.c.execute("SELECT climate, (count(*)/(SELECT count(*) FROM business_risk))*100 "
  #                      "FROM business_risk GROUP BY climate ORDER BY climate")
  #       result = self.c.fetchall()
  #       agg_df = pd.DataFrame(result, columns=['climate', 'count'])
  #       climates = agg_df['climate'].tolist()
  #       contribution = agg_df['count'].tolist()
  #       explode = (0.1, 0, 0, 0, 0, 0, 0, 0)
  #       fig1, ax1 = plt.subplots()
  #       ax1.set_title('Business climate assesments')
  #       ax1.pie(contribution, explode = explode, labels=climates, autopct='%1.1f%%', shadow=True, startangle=90)
  #       ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  #       plt.show()


cs = ExportController()      # utworzenie obiektu i wywolanie konstruktora domyslnego
# cs.getTablesByPandas()      # wywolanie metody

cs.getJewellery()
cs.exportToXlsx()

cs.exportToDatabase()

# cs.generatePlots()
# cs.generatePieChart()


