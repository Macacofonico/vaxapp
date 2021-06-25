import sys
from flask import Flask, request, jsonify
import sqlite3
import os
import mysql.connector

# Init app
app = Flask(__name__)

#generate dictionary from db results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_cursor():
    if os.getenv("MYSQL_HOST", None) is not None:
        mydb = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "mydb"),
            password=os.getenv("MYSQL_PASSWORD", "password"),
            user=os.getenv("MYSQL_USER", "dev-user"),
            database=os.getenv("MYSQL_DATABASE", "cocktails")
        )
        return mydb
    elif os.getenv("SQLITE3_PATH", "cocktail.db") is not None:
        return sqlite3.connect(os.getenv("SQLITE3_PATH", "cocktail.db"))
    else:
        sys.exit("Errors: app.py needs DB parameters (MYSQL or SQLITE).")




@app.route('/', methods=['GET']) #http://mysite.com/
def home():
    return """
<h1>Questo è un progetto di esempio. Le api sono disponibili a /api/v1/</h1>

<ul>
<li>Sviluppo di una applicazione web (RESTful) che permetta la prenotazione di un vaccino e che supporti l&rsquo;utilizzo di almeno due diversi sistemi di backend (es. Mysql eSqlite).</li>
<li>Devono essere sviluppati entrambi i container e, nel caso si utilizzino docker disponibili online (presi direttamente da dockerhub), si descriva in dettaglio come questo viene configurato (ad esempio come caricare lo schema).</li>
<li><strong>Risorse base</strong>: Vaccini, Punto di Vaccino, Utente, Prenotazione,&nbsp;</li>
<li><strong>Ruoli Base</strong>
<ul>
<li><strong>Admin</strong>
<ol>
<li>Pu&ograve; aggiungere e cancellare punti vaccino</li>
<li>Pu&ograve; aggiungere le tipologie di vaccino</li>
<li>Pu&ograve; modificare una prenotazione di qualsiasi utente</li>
<li>Pu&ograve; chiedere statistiche (a vostra scelta) sui punti di vaccino e sulle tipologie di vaccino</li>
</ol>
</li>
<li><strong>Utente</strong>
<ol>
<li>Pu&ograve; iscriversi al servizio.</li>
<li>Pu&ograve; effettuare una prenotazione in un determinato giorno e ora per una tipologia di vaccino (pu&ograve; fare una sola prenotazione per vaccino) un punto di vaccinazione</li>
<li>Pu&ograve; modificarla</li>
</ol>
</li>
</ul>
</li>
</ul>
<p>Tutto deve essere implementato secondo lo schema REST con scambio di informazioni in json.</p>
"""


# return all items and create new ones
@app.route('/api/v1/cocktails/', methods=['GET','POST']) #http://mysite.com/api/v1/cocktails/
def cocktail():
    if request.method == "GET":
        conn = get_db_cursor()
        # returns items from the database as dictionaries rather than lists
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cocktails = cur.execute('SELECT * FROM cocktail;').fetchall()
        for cocktail in cocktails:
            id=cocktail["cocktail_id"]
            ingridients = cur.execute('SELECT name,size FROM ingridients WHERE cocktail=' + str(id) + ';').fetchall()
            spiritis = cur.execute('SELECT name FROM suggested_spirits WHERE cocktail=' + str(id) + ';').fetchall()
            cocktail["ingridients"] = ingridients
            cocktail["suggested_spirits"] = spiritis
        return jsonify(cocktails), 200
    elif request.method == "POST":
        if not request.is_json:
            return {"error": "only json accepted"}, 400
        content = request.get_json()

    #{
	#"name":"gin tonic",
	#"ingridients":[
    #	{"name":"gin",
	#		"size":"6cl"
	#	}
	#	,
	#		{"name":"tonic",
	#		"size":"12cl"
    #		}],
	# "suggested_spirits":["gingarby","hendrix"],
	# "instructions":"versalo molto bene",
	#"author":"Luca"
    # }


        name = content.get('name')
        author = content.get('author')
        ingridients = content.get('ingridients')
        instructions= content.get('instructions')
        suggested_spirits = content.get('suggested_spirits')
        conn = get_db_cursor()
        cur = conn.cursor()
        try:
            query = 'INSERT INTO cocktail (name, author, instructions) VALUES ("' + name + '","' + author + '","' + instructions + '");'
            cur.execute(query)
        except sqlite3.IntegrityError as err:
            return jsonify({"error":"name must be unique"}),409
        id=cur.lastrowid
        for ingridient in ingridients:
            try:
                query = 'INSERT INTO ingridients (name, size, cocktail) VALUES ("' + ingridient["name"] + '","' + ingridient["size"] + '",' + str(id) + ');'
                cur.execute(query)
            except sqlite3.IntegrityError as err:
                return jsonify({"error": "name must be unique"}), 409
        for spirit in suggested_spirits:
            try:
                query = 'INSERT INTO suggested_spirits (name,cocktail) VALUES ("' + spirit + '",' + str(id) + ');'
                cur.execute(query)
            except sqlite3.IntegrityError as err:
                return jsonify({"error": "name must be unique"}), 409
        conn.commit()
        return jsonify({"id":id}),201


@app.route('/api/v1/cocktails/<id>', methods=['GET','PUT','DELETE']) #http://mysite.com/api/v1/cocktails/202
def single_cocktail(id):
    if request.method == "GET":
        conn = get_db_cursor()
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cocktail = cur.execute('SELECT * FROM cocktail WHERE cocktail_id='+str(id)+';').fetchall()
        if len(cocktail) == 0 :
            return "",404
        cocktail=cocktail[0]
        ingridients = cur.execute('SELECT name,size FROM ingridients WHERE cocktail='+str(id)+';').fetchall()
        spiritis = cur.execute('SELECT name FROM suggested_spirits WHERE cocktail='+str(id)+';').fetchall()
        cocktail["ingridients"]=ingridients
        cocktail["suggested_spirits"]=spiritis
        return jsonify(cocktail), 200
    elif request.method == "PUT":
        return "",200
    elif request.method == "DELETE":
        conn = get_db_cursor()
        cur = conn.cursor()
        cur.execute('DELETE FROM cocktail WHERE cocktail_id=' + str(id) + ';').fetchall()
        conn.commit()
        return "",204

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found</p>", 404



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", '0.0.0.0')
    app.run(host=host, port=port)