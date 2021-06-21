from flask import Flask, render_template
from scrapinghub import ScrapinghubClient
import pandas as pd

app = Flask(__name__)

apikey = '42ec2a2514134e4096d3b2ff6b65231d'
client = ScrapinghubClient(apikey)
project = client.get_project(527753)

@app.route("/")
def index():

    data = []

    books = client.get_job('527753/3/2').items.iter()
    quotes = client.get_job('527753/1/10').items.iter()

    for elem in quotes:
      data.append(elem)
      
    for elem in books:
      data.append(elem)

    df = pd.DataFrame(data=data, columns=['text', 'author', 'tags'])

    return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

@app.route("/ebay")
def ebay():
  
  ebay = client.get_job('529389/3/2').items.iter()
  df = pd.DataFrame(data=ebay, columns=['text', 'author', 'tags'])
  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

@app.route("/craigslist")
def craigslist():

  craigslist = client.get_job('529389/3/2').items.iter()
  df = pd.DataFrame(data=craigslist, columns=['text', 'author', 'tags'])
  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

@app.route("/amazon")
def amazon():

  amazon = client.get_job('529389/3/2').items.iter()
  df = pd.DataFrame(data=amazon, columns=['text', 'author', 'tags'])
  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

if __name__ == "__main__":
  app.run()
