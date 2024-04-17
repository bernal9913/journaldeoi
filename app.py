import csv
import os
import time
import pandas as pd
import random

import requests
import schedule
from flask import Flask, render_template, request, redirect, url_for
from string import ascii_uppercase

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

def check_country_rank():
    if not os.path.exists('country_rank.csv'):
        url = "https://www.scimagojr.com/countryrank.php?out=xls"
        response = requests.get(url)
        if response.status_code == 200:
            with open('country_rank.xlsx', 'wb') as f:
                f.write(response.content)
            print("Descarga exitosa de xlss")

            # convertir el archivo xlsx a csv
            df = pd.read_excel('country_rank.xlsx')
            df.to_csv('country_rank.csv', sep=';', index=False)
            print("Conversion exitosa de xlsx a csv")
        else:
            print("Alguito mal")
    else:
        print("File already exists")
def check_countries():
    if not os.path.exists('world_population.csv'):
        print("Descargando archivo de población mundial")
        print("Error descargando el archivo, lol")
def background_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
def obtener_detalle_articulo(sourceid):
    detalle_articulo = None
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Sourceid'] == sourceid:
                detalle_articulo = row
                break
    return detalle_articulo
def obtener_palabras_con_letra(letra):
    palabras = []
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Title'].startswith(letra):
                palabras.append(row['Title'])
    return palabras

def obtener_revistas_con_palabra(palabra):
    revistas = []
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if palabra.lower() in row['Title'].lower():
                revistas.append(row)
    return revistas
def obtener_ranking_paises():
    data = []
    if not os.path.exists('country_rank.csv'):
        check_country_rank()
    with open("country_rank.csv", 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            data.append(row)
    return data
def read_countries():
    countries = []
    with open('world_population.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            countries.append(row)
    return countries
def read_counry_details(country):
    country_details = None
    with open('world_population.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row['Country/Territory'] == country:
                country_details = row
                break
    return country_details
def read_country_journals(country):
    country_journals = []
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Country'] == country:
                country_journals.append(row)
                if len(country_journals) >= 100:
                    break
    return country_journals
@app.route('/')
def index():  # put application's code here
    top_journals = []
    countries = []
    if not os.path.exists('country_rank.csv'):
        check_country_rank()
    if not os.path.exists('journal.csv'):
        check_journal()

    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for idx, row in enumerate(reader):
            # Detener la lectura después de las primeras 10 revistas
            if idx >= 10:
                break
            top_journals.append({
                'Title': row['Title'],
                'Rank': row['Rank'],
                'SJR': row['SJR'],
                'Publisher': row['Publisher'],
                'Total Refs': row['Total Refs.'],
                'Source ID': row['Sourceid']
            })
    with open('country_rank.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for idx, row in enumerate(reader):
            # Detener la lectura después de las primeras 10 revistas
            if idx >= 10:
                break
            countries.append({
                'Country': row['Country'],
                'Documents': row['Documents'],
                'Citable documents': row['Citable documents'],
                'Citations': row['Citations'],
                'Self-citations': row['Self-citations'],
                'Citations per document': row['Citations per document'],
                'H index': row['H index']
            })

    return render_template('index.html', top_journals=top_journals, countries=countries)
@app.route('/paises', methods=['GET'])
def ranking_paises():
    data = obtener_ranking_paises()
    return render_template('ranking_paises.html', country_rank_data=data)
@app.route('/pais')
def country_details():
    country = request.args.get('country')
    print(f"country: {country}")  # print the country
    country_data = read_counry_details(country)
    print(f"country_data: {country_data}")  # print the country_data

    if country_details:
        country_journals = read_country_journals(country)
        print(f"country_journals: {country_journals}")  # print the country_journals
        return render_template('country_details.html', country_details=country_data, country_journals=country_journals)
    else:
        return render_template('not_steph.html'), 404

@app.route('/search_advance', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        term = request.args.get('term', '').lower()
    elif request.method == 'POST':
        term = request.form['search_term'].lower()
    results = []
    if not os.path.exists('journal.csv'):
        check_journal()
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if term in row['Title'].lower():
                results.append(row)
    return render_template('results_advance.html', results=results, term=term)
@app.route('/detalle')
def detalle():
    sourceid = request.args.get('sourceid')
    print(f"sourceid: {sourceid}")  # print the sourceid
    detalle_articulo = None
    if not os.path.exists('journal.csv'):
        check_journal()
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Sourceid'] == sourceid:
                detalle_articulo = row
                break
    print(f"detalle_articulo: {detalle_articulo}")  # print the detalle_articulo
    if detalle_articulo:  # Check if detalle_articulo is not None
        return render_template('detalle.html', detalle_articulo=detalle_articulo)
    else:
        return render_template('not_steph.html'), 404
@app.route('/revista/<sourceid>')
def detalle_revista(sourceid):
    detalle_articulo = obtener_detalle_articulo(sourceid)  # Función para obtener los detalles del artículo del CSV
    return render_template('detalle.html', detalle_articulo=detalle_articulo)
@app.route("/revista-random")
def revista_random():
    # Genera un número aleatorio entre 1 y 10,000
    random_sourceid = str(random.randint(1, 100000))
    print(f"random_sourceid: {random_sourceid}")
    # Redirige al usuario a la página de detalle con el sourceid aleatorio
    return redirect(url_for("detalle", sourceid=random_sourceid))

@app.route('/acercade', methods=['GET'])
def acercade():
    return render_template('acercade.html')
@app.route('/contacto', methods=['GET'])
def contacto():
    return render_template('contacto.html')
@app.route('/abecedario')
def abecedario():
    return render_template('abecedario.html', letras=ascii_uppercase)
@app.route('/letra/<letra>')
def palabras_con_letra(letra):
    palabras = obtener_palabras_con_letra(letra)  # Función para obtener las palabras del CSV
    return render_template('palabras.html', letra=letra, palabras=palabras)
@app.route('/revistas/<letra>/<palabra>')
def revistas_con_palabra(letra, palabra):
    revistas = obtener_revistas_con_palabra(palabra)  # Función para obtener las revistas del CSV
    return render_template('revistas.html', letra=letra, palabra=palabra, revistas=revistas)
@app.route('/search', methods=['GET','POST'])
def search_test():
    if request.method == 'GET':
        term = request.args.get('term', '').lower()
    elif request.method == 'POST':
        term = request.form['search_term'].lower()

    results = []
    if not os.path.exists('journal.csv'):
        check_journal()
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if term in row['Title'].lower():
                # Make sure the fields exist in your CSV file and their names match exactly
                #catalogo = row.get('Catalog', 'N/A')  # Use get method to avoid KeyError if the field doesn't exist
                factor_impacto = row.get('SJR', 'N/A')
                cuartil = row.get('SJR Best Quartile', 'N/A')
                publisher = row.get('Publisher', 'N/A')
                total_citas = row.get('Total Cites (3years)', 'N/A')

                # Add the additional information to the row
                #row['Catalogo'] = catalogo
                row['Factor Impacto'] = factor_impacto
                row['Publisher'] = publisher
                row['Cuartil'] = cuartil
                row['Total Citas'] = total_citas

                results.append(row)
    return render_template('results_simple.html', results=results, term=term)

@app.route('/explorar', methods=['GET'])
def explorar():
    return render_template('explorar.html')
@app.route('/categorias', methods=['GET'])
def categorias():
    with open ('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        categorias = []
        for row in reader:
            if row['Categories'] not in categorias:
                categorias.append(row['Categories'])
    return render_template('categorias.html', categories = categorias)
@app.route('/filter')
def filter_categories():
    category = request.args.get('category')
    print(f"category: {category}")
    results = []
    with open('journal.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if category in row['Categories']:
                results.append(row)
    return render_template('results_simple.html', results=results, term=category)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_steph.html'), 404



if __name__ == '__main__':
    import threading
    background_thread = threading.Thread(target=background_scheduler)
    background_thread.start()
    app.debug = True
    app.run()
    check_journal()
    check_country_rank()
