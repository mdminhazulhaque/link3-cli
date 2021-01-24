try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

from tabulate import tabulate as t
import os
import click
import requests
import json

L3_API_LOGIN   = "https://selfcare.link3.net/login"
L3_API_ACCOUNT = "https://selfcare.link3.net/account"
L3_API_PAYMENT = "https://selfcare.link3.net/mypayments"
L3_API_TICKETS = "https://selfcare.link3.net/mytickets"

@click.group()
def app():
    pass

@app.command(help='Login to portal')
@click.option('--username', '-u', type=str, required=True)
@click.option('--password', '-p', type=str, required=True)
def login(username, password):
    data = {
        'l3id': username,
        'password': password,
        'remember': 'on',
        'formSubmitted': 'Sign in'
    }
    response = requests.post(L3_API_LOGIN, data=data, allow_redirects=False)
    if response.status_code == 302:
        PHPSESSID = response.headers['Set-Cookie']\
            .split(";")[0]\
            .split("=")[1]
        print(F"Login success. Please export L3_PHPSESSID={PHPSESSID}")
    else:
        print("Login failed")
        exit(1)
        
@app.command(help='Show account information')
def account():
    phpsessid = os.environ.get("L3_PHPSESSID")
    if not phpsessid:
        print("L3_PHPSESSID not found. Try logging in.")
        exit(0)
        
    response = requests.get(L3_API_ACCOUNT, cookies={"PHPSESSID": phpsessid})
    soup = BeautifulSoup(response.text, "html5lib")
    data = []
    
    for row in soup.find_all("div", {"class": "contact-info-group"}):
        key = row.find("div", {"class": "col-lg-4"}).text.strip()
        value = row.find("div", {"class": "col-lg-7"}).text.strip()
        data.append([key, value])
        
    if len(data) == 0:
        print("Invalid L3_PHPSESSID")
        exit(1)
    else:
        print(t(data))
    
@app.command(help='Show online payment history')
def payments():
    phpsessid = os.environ.get("L3_PHPSESSID")
    if not phpsessid:
        print("L3_PHPSESSID not found. Try logging in.")
        exit(0)
        
    response = requests.get(L3_API_PAYMENT, cookies={"PHPSESSID": phpsessid})
    soup = BeautifulSoup(response.text, "html5lib")
    tbody = soup.find("tbody", {"class": "packages-box-info"})
    data = []
    
    for tr in tbody.find_all("tr"):
        td = list(tr.find_all("td"))
        date = td[1].text.strip()
        gateway = td[2].text.strip()
        amount = td[3].text.strip()
        invoice = td[4].find("a")["href"]
        data.append([date, gateway, amount, invoice])
        
    if len(data) == 0:
        print("Invalid L3_PHPSESSID")
        exit(1)
    else:
        headers = ["date", "gateway", "amount", "invoice"]
        print(t(data, headers=headers))
    
@app.command(help='Show ticket history')
def tickets():
    phpsessid = os.environ.get("L3_PHPSESSID")
    if not phpsessid:
        print("L3_PHPSESSID not found. Try logging in.")
        exit(0)
        
    response = requests.get(L3_API_TICKETS, cookies={"PHPSESSID": phpsessid})
    soup = BeautifulSoup(response.text, "html5lib")
    tbody = soup.find("tbody", {"class": "packages-box-info"})
    data = []
    
    for tr in tbody.find_all("tr"):
        td = list(tr.find_all("td"))
        date = td[1].text.strip()
        ticket = td[2].text.strip()
        category = td[3].text.strip()
        status = td[4].text.strip()
        action = td[5].find("a")["href"]
        data.append([date, ticket, category, status, action])
    
    if len(data) == 0:
        print("Invalid L3_PHPSESSID")
        exit(1)
    else:
        headers = ["date", "ticket", "category", "status", "action"]
        print(t(data, headers=headers))
        
if __name__ == "__main__":
    app()
