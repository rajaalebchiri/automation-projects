#!/usr/bin/env python

"""Scraping Hackers News and send it as a newsletter email"""

import os
import smtplib
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hacker News URL
NEWS_URL = "https://news.ycombinator.com/"
SUBSCRIBERS = ["++++"]


def send_email(subscribers, data):
    """Send an email to subscribers using smtplib"""
    sender_email = "+++"

    for subscriber in subscribers:
        # create a message object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = subscriber
        message['Subject'] = 'Latest Hacker News'
        # Add message body
        body = f""
        for title in data:
            body += f"""<tr>
                        <td>{list(title.keys())[0]}</td>
                        <td>{list(title.values())[0]}</td>
                        </tr>"""
        html_table = f"""
        <html>
        <head></head>
        <body>
        <p>Here's an example HTML table:</p>
        <table border="1">
            <tr>
            <th>title</th>
            <th>link</th>
            </tr>
            {body}
        </table>
        </body>
        </html>
        """
        message.attach(MIMEText(html_table, 'html'))
        smtp_server = '++++++'
        smtp_port = 0000
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        password = os.environ.get('password')

        if password:
            # Open the SMTP connection
            smtp_connection.login(sender_email, password)
            # Send the email
            smtp_connection.sendmail(
                sender_email, subscriber, message.as_string())
            # Close the SMTP connection
            smtp_connection.quit()
        else:
            print("Error: Please set 'password' environment variable")

        # Just in case, wait for 3 seconds to not spam recipients
        time.sleep(3)


def scrape_data(url):
    """Function to scrame data from the news url"""
    # start the driver
    driver = webdriver.Chrome()
    driver.get(url)

    titles = []

    # get page content
    content = driver.page_source

    soup = BeautifulSoup(content, features="html.parser")

    for tr in soup.findAll("tr", attrs={"class": "athing"}):
        title = tr.find('span', attrs={'class': 'titleline'}).a.text
        link = tr.find('span', attrs={'class': 'titleline'}).a["href"]
        titles.append({title: link})

    driver.quit()
    return titles


if __name__ == "__main__":
    titles = scrape_data(url=NEWS_URL)
    send_email(subscribers=SUBSCRIBERS, data=titles)
