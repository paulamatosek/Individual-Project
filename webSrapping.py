def getTop250(self):
    try:
        self.page = requests.get("https://www.imdb.com/chart/top?ref_=nv_mv_250")
        print("Wykonano poprawnie żądanie")
        # print(self.page.content)
    except:
        print("Ups! Coś poszło nie tak")


def scrappingTop250(self):
    # page.content -> zwraca zawartość żądania get
    html_content = BeautifulSoup(self.page.content, 'html.parser')
    # print(html_content.prettify())
    titles = html_content.find_all(class_="titleColumn")
    years = html_content.find_all('span', attrs={'class': 'secondaryInfo'})
    ratings = html_content.find_all(class_="ratingColumn imdbRating")
    refs = html_content.find_all(class_="titleColumn")

    for index, title in enumerate(titles):
        if (index == 10):
            break
        titles[index] = str(titles[index]).split(">")[2].replace("</a", "")
        years[index] = str(years[index]).split("(")[1].split(")")[0]
        ratings[index] = str(ratings[index]).split(">")[2].replace("</strong", "")
        refs[index] = "https://www.imdb.com" + str(refs[index]).split('href="')[1].split('"')[0]
        director, stars = self.getMovieDetails(refs[index])
        # zapis danych o filmie do obiektu modelu
        movie = top250(titles[index], years[index], director, stars, ratings[index], refs[index])
        print(movie)
        self.movies.append(movie)  # dodawanie obiektu filmu do listy