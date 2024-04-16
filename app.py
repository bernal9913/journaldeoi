import csv
import os
import time

import requests
import schedule
from flask import Flask, render_template, request

app = Flask(__name__)

def check_journal():
    if not os.path.exists('journal.csv'):
        url = "https://www.scimagojr.com/journalrank.php?out=xls"
        response = requests.get(url)
        if response.status_code == 200:
            with open('journal.csv', 'wb') as f:
                f.write(response.content)
            print("Todo bien")
        else:
            print("Alguito mal")
    else:
        print("File already exists")

schedule.every().day.at("00:00").do(check_journal)

def background_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    term = request.form['search_term'].lower()
    results = []
    if not os.path.exists('journal.csv'):
        check_journal()
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if term in row['Title'].lower():
                results.append(row)
    return render_template('results.html', results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_steph.html'), 404

if __name__ == '__main__':
    import threading
    background_thread = threading.Thread(target=background_scheduler)
    background_thread.start()
    app.run()
