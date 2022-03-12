import json
import pandas as pd
from newspaper import Article
import newspaper
import requests
import urllib3
import urllib
import lxml
import csv

urls = pd.read_csv("test.csv")
text_dict = {}
count = 0
img_urls = ["icedrive.com", "smugmug.com", "photos.google.com", "photoblog.com", "icloud.com","dropbox.com", "4shared.com",
            "imgshack", "flickr.com", "imgur.com", "freeimages.com", "imgbox.com","cluster.com", "postimages.org",
            "freeimagehosting.net", "deviantart.com", "unsplash.com", "500px.com", "pxhere.com", "pixabay.com"]

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0
count_7 = 0

error_file = "errors-newspaper3k.csv"


def image_download(url, img_urls, count):

    for j in range(len(img_urls)):
        if img_urls[j] in url:
            response = requests.get(url)

            file = open(str(count) + ".png", "wb")
            file.write(response.content)
            file.close()

            return -1


for i in urls["url"]:
    while True:
        try:
            flag = 0
            if i[0:7] != "http://":
                if i[0:8] == "https://":
                    flag = 1
                elif flag != 1:
                    prefix = "http://"
                    i = prefix + i

            count = count+1
            print(i, count)

            if image_download(i, img_urls, count) == -1:
                break

            response = requests.get(i)

            article = Article(i)
            article.download()
            article.parse()

            text_dict["Title"] = article.title
            text_dict["Title"] = text_dict["Title"].replace("\n","")
            text_dict["Title"] = text_dict["Title"].replace(r"\u","")
            text_dict["URL"] = article.url
            text_dict["Effective URL"] = [resp.url for resp in response.history]
            text_dict["Date"] = article.publish_date
            text_dict["Date"] = str(text_dict["Date"])
            text_dict["Authors"] = article.authors
            text_dict["Text"] = article.text
            text_dict["Text"] = text_dict["Text"].replace("\n","")
            text_dict["Text"] = text_dict["Text"].replace(r"\u","")

            file_name = str(count)
            test_json = open(file_name+".json", "w")
            json.dump(text_dict, test_json)
            test_json.close()

            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, "No errors"])

            break

        except newspaper.article.ArticleException as e:
            count_1 = count_1+1
            print(e, count_1)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_1])
            break

        except requests.exceptions.TooManyRedirects as e:
            count_2 = count_2+1
            print(e,count_2)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_2])
            break

        except UnicodeError as e:
            count_3 = count_3 + 1
            print(e, count_3)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_3])
            break

        except requests.exceptions.ConnectionError as e:
            count_4 = count_4 + 1
            print(e,count_4)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_4])
            break

        except urllib3.exceptions.LocationParseError as e:
            count_5 = count_5 + 1
            print(e, count_5)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_5])
            break

        except urllib.error.URLError as e:
            count_6 =count_6 + 1
            print(e, count_6)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_6])
            break

        except lxml.etree.ParserError as e:
            count_7 =count_7 + 1
            print(e, count_7)
            with open(error_file,"a") as errors:
                writer = csv.writer(errors)
                writer.writerow([count, i, e, count_7])
            break




