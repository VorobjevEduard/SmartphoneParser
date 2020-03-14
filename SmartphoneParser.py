import re
import xlsxwriter
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

if __name__ == "__main__":
    workbook = xlsxwriter.Workbook('top10smartphones.xlsx')
    worksheet = workbook.add_worksheet('Топ 10 смартфонов')
    
    worksheet.write('A1', 'Наименование')
    worksheet.write('B1', 'Код товара')
    worksheet.write('C1', 'Цена')
    worksheet.write('D1', 'Ссылка на картинку')
    
    worksheet.set_column('A:A', 60)
    worksheet.set_column('B:C', 10)
    worksheet.set_column('D:D', 150)
    
    url = 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/'
    opts = Options()
    opts.set_headless()
    assert opts.headless
     
    browser = Firefox(options=opts)
    browser.get(url)
    
    results = browser.find_elements_by_class_name('product-info__title-link')
    for i in range(10):
        worksheet.write(i + 1, 0, results[i].text)
    
    soup = BeautifulSoup(browser.page_source, 'lxml')
    product_codes = re.findall(r'\>\d\d\d\d\d\d\d', str(soup))
    for i in range(10):
        worksheet.write(i + 1, 1, int(product_codes[i][1:]))
    
    links = re.findall(r'/product/[a-zA-Z0-9-/]*"', str(soup.find_all(class_ = 'product-info__image')))
    for i in range(10):
        url = 'https://technopoint.ru' + links[i][:-1]
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        worksheet.write(i + 1, 2, int(str(re.findall('"price":[0-9]*,', str(soup)))[10:-3]))
        worksheet.write(i + 1, 3, str(re.findall('href="https://s.technopoint.ru/[a-z0-9/]*/800/650/[a-z0-9/.]*"', str(soup))[0])[6:-1])

    browser.close()
    workbook.close()