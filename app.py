from flask import Flask, render_template
from scrapinghub import ScrapinghubClient
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    apikey = '42ec2a2514134e4096d3b2ff6b65231d'
    client = ScrapinghubClient(apikey)
    job = client.get_job('527753/2/1')
    df = pd.DataFrame(data=job.items.iter(), columns=['Title', 'Address', 'URL'])

    return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

if __name__ == "__main__":
  app.run()
