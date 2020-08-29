import smtplib
import ssl
from re import findall
from bs4 import BeautifulSoup
from requests import get


def getPosts(request_info):
    page_response = get(request_info.page_url, headers=request_info.headers, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    return soup.find_all('section', class_='listing-item featured')


def sendEmail(posts, email_address):
    sender_email = email_address
    receiver_email = email_address
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with open("password", 'r') as passFile:
        password = passFile.readline()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_address, password)
        server.sendmail(sender_email, receiver_email, message)


class RequestInfo:
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def __init__(self, query, zip_code, distance, price_range):
        self.query = query
        self.zip_code = zip_code
        self.distance = distance
        self.price_range = price_range
        self.price_range_list = findall('[0-9]+', price_range)
        self.page_url = ("https://classifieds.ksl.com/search/keyword/" + query +
                         "/zip/" + zip_code + "/miles/" + distance + "/priceFrom/" +
                         self.price_range_list[0] + "/priceTo/" + self.price_range_list[1] + "/Sale/perPage/96")

    @classmethod
    def from_input(cls):
        return cls(
            input("What are you searching for?\n"),
            input("What is your zip code?\n"),
            input("What is your range in miles?\n"),
            input("What is your price range (in whole dollars, ex. $5-$40)\n"),
        )


def main():
    request_info = RequestInfo.from_input()
    email_address = input("What is your email?\n")
    posts = getPosts(request_info)
    sendEmail(posts, email_address)


if __name__ == "__main__":
    main()
