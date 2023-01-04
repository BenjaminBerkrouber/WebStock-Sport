from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(    #pymysql.connect remplace mysql.connector
        host="localhost",   #localhost sur les machines perso.
        user="benjamin",
        password="1605",
        database="BDD_benjamin",
        charset='utf8mb4',                      # 2 attributs à ajouter
        cursorclass=pymysql.cursors.DictCursor  # 2 attributs à ajouter
)
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_layout():
    return render_template('layout.html')

#---------------------------Type Sport-------------------------#

@app.route('/type-sport/show')
def show_type_sport():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM type_sport ORDER BY id_type_sport;"
    mycursor.execute(sql)
    types_sports = mycursor.fetchall()
    results = []
    for type_sport in types_sports:
        id = type_sport['id_type_sport']
        sql = "SELECT COUNT(*) as nbr_sport FROM sport WHERE type_sport_id = %s"
        mycursor.execute(sql, (id,))
        nbr_sport = mycursor.fetchone()
        results.append({'type_sport': type_sport, 'nbr_sport_by_cat': nbr_sport})
    return render_template('type_sport/show_type_sport.html',results=results)

@app.route('/type-sport/add', methods=['GET'])
def add_type_sport():
    return render_template('type_sport/add_type_sport.html')

@app.route('/type-sport/add' , methods=['POST'])
def valid_add_type_sport():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle','')
    tuple_insert = (libelle,)
    sql = "INSERT INTO type_sport(libelle) VALUES (%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libelle :'+ libelle
    flash(message, 'alert-success')
    return redirect('/type-sport/show')


@app.route('/type-sport/edit', methods=['GET'])
def edit_type_sport():
    mycursor = get_db().cursor()
    id_type_sport = request.args.get('id_type_sport', '')
    sql = "SELECT * FROM type_sport WHERE id_type_sport=%s"
    mycursor.execute(sql, (id_type_sport,))
    type_sport = mycursor.fetchone()
    return render_template('type_sport/edit_type_sport.html', type_sport=type_sport)

@app.route('/type-sport/edit', methods=['POST'])
def valid_edit_type_sport():
    mycursor = get_db().cursor()
    id_type_sport = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql ="UPDATE type_sport SET id_type_sport=%s, libelle=%s WHERE id_type_sport=%s;"
    mycursor.execute(sql, (id_type_sport, libelle, id_type_sport))
    get_db().commit()
    print(u'type sport modifié, id: ' + id_type_sport +' = ' + libelle)
    message=u' type sport  modifié, id: ' + id_type_sport +' = ' +libelle
    flash(message, 'alert-success')
    return redirect('/type-sport/show')

@app.route('/type-sport/delete', methods=['GET'])
def delete_type_sport():
    # Get database cursor
    mycursor = get_db().cursor()

    # Get the id of the type of sport to delete from the request query string
    id_type_sport = request.args.get('id_type_sport', '')

    # Check if there are any sports that use this type of sport
    sql = "SELECT COUNT(id_sport) AS sport_count FROM sport WHERE type_sport_id=%s"
    mycursor.execute(sql, (id_type_sport,))
    sport_count = mycursor.fetchone()['sport_count']

    if sport_count == 0:
        sql = "DELETE FROM type_sport WHERE id_type_sport = %s"
        mycursor.execute(sql, (id_type_sport,))
        get_db().commit()
        message = u'La catégorie sport n° ' + id_type_sport + ' à était supprimé.'
        flash(message, 'alert-warning')
        return redirect('/type-sport/show')

    sql = "SELECT * FROM sport WHERE type_sport_id = %s"
    mycursor.execute(sql, (id_type_sport,))
    sports = mycursor.fetchall()

    sql = "SELECT * FROM type_sport WHERE id_type_sport = %s"
    mycursor.execute(sql, (id_type_sport,))
    types_sports = mycursor.fetchall()

    message = u'La catégorie sportive n° ' + id_type_sport + ' n as pas pue être supprimé.'
    flash(message, 'alert-warning')

    return render_template('type_sport/show_error_del.html', sports=sports, types_sports=types_sports, sport_count=sport_count)

@app.route('/type-sport/error_del', methods=['GET'])
def delete_error_type_sport():
    # Get database cursor
    mycursor = get_db().cursor()
    id_sport = request.args.get('id_sport', '')
    id_type_sport = request.args.get('id_type_sport', '')

    sql = "DELETE FROM sport WHERE id_sport = %s"
    mycursor.execute(sql, (id_sport,))
    get_db().commit()

    sql = "SELECT COUNT(id_sport) AS sport_count FROM sport WHERE type_sport_id=%s"
    mycursor.execute(sql, (id_type_sport,))
    sport_count = mycursor.fetchone()['sport_count']

    if sport_count == 0:
        message = u'Plus aucun sport dans cette catégorie'
        flash(message, 'alert-warning')
        return redirect('/type-sport/show')

    sql = "SELECT * FROM type_sport WHERE id_type_sport = %s"
    mycursor.execute(sql, (id_type_sport,))
    types_sports = mycursor.fetchall()

    sql = "SELECT * FROM sport WHERE type_sport_id = %s"
    mycursor.execute(sql, (id_type_sport,))
    sports = mycursor.fetchall()

    message = u'La sport n° ' + id_type_sport + ' n as pas pue être supprimé. '+id_sport
    flash(message, 'alert-warning')

    return render_template('type_sport/show_error_del.html', sports=sports, types_sports=types_sports, sport_count=sport_count)


#------------------------------Sport---------------------------#

@app.route('/sport/show')
def show_sport():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM sport ORDER BY id_sport;"
    mycursor.execute(sql)
    sports = mycursor.fetchall()
    sql = "SELECT * FROM type_sport ORDER BY id_type_sport;"
    mycursor.execute(sql)
    types_sports = mycursor.fetchall()
    return render_template('sport/show_sport.html', sports=sports, types_sports=types_sports)

@app.route('/sport/add', methods=['GET'])
def add_sport():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM type_sport"
    mycursor.execute(sql)
    types_sports = mycursor.fetchall()
    return render_template('sport/add_sport.html', types_sports=types_sports)

@app.route('/sport/add' , methods=['POST'])
def valid_add_sport():
    mycursor = get_db().cursor()
    nomSport = request.form.get('nomSport', '')
    typeSport_id = request.form.get('typeSport_id', '')
    prixInscription = request.form.get('prixInscription', '')
    dateLimiteInscription = request.form.get('dateLimiteInscription', '')
    nbPratiquant = request.form.get('nbPratiquant', '')
    image = request.form.get('image', '')
    tuple_insert = (nomSport, prixInscription, dateLimiteInscription, typeSport_id, image, nbPratiquant)
    sql = "INSERT INTO sport(nom_sport,prix_inscription,date_limite_inscription,type_sport_id,image,nb_pratiquant) VALUES (%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'Nouveau sport ajouter :' + nomSport
    flash(message, 'alert-success')
    return redirect('/sport/show')

@app.route('/sport/edit', methods=['GET'])
def edit_sport():
    id = request.args.get('id_sport', '')
    id=int(id)
    mycursor = get_db().cursor()
    sql = "SELECT * FROM sport WHERE id_sport=%s;"
    mycursor.execute(sql, id)
    sports = mycursor.fetchall()
    sql = "SELECT * FROM type_sport"
    mycursor.execute(sql)
    types_sports = mycursor.fetchall()
    return render_template('sport/edit_sport.html', sports=sports, types_sports=types_sports)

@app.route('/sport/edit', methods=['POST'])
def valide_edit_sport():
    mycursor = get_db().cursor()
    id_sport = request.form['id_sport']
    nom_sport = request.form['nom_sport']
    type_sport_id = request.form['type_sport_id']
    prix_inscription = request.form['prix_inscription']
    date_limite_inscription = request.form['date_limite_inscription']
    nb_pratiquants = request.form['nb_pratiquants']
    image = request.form['image']
    tuple_update = (id_sport, nom_sport, prix_inscription, date_limite_inscription, type_sport_id, image, nb_pratiquants, id_sport)
    sql ="UPDATE sport SET id_sport=%s, nom_sport=%s, prix_inscription=%s, date_limite_inscription=%s, type_sport_id=%s, image=%s, nb_pratiquants=%s WHERE id_sport=%s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    message=u' sport  modifié, id: ' + id_sport +' = ' +nom_sport
    flash(message, 'alert-success')
    return redirect('/sport/show')

@app.route('/sport/delete', methods=['GET'])
def delete_sport():
    mycursor = get_db().cursor()
    id = request.args.get('id_sport')
    tuple_delete = (id,)
    sql = "DELETE FROM sport WHERE id_sport=%s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'le sport n° ' + id + ' à était supprimer '
    flash(message, 'alert-warning')
    return redirect('/sport/show')

#------------------------------Filtre---------------------------#

@app.route('/filtres/show', methods=['GET'])
def show_filtres():
    #session.clear()
    mycursor = get_db().cursor()
    sql = """SELECT *
             FROM type_sport;"""
    mycursor.execute(sql)
    types_sports = mycursor.fetchall()

    sql="""SELECT *
           FROM sport"""

    list_param = []
    condition_and = ""

    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "

    if "filter_word" in session:
        sql = sql + "nom_sport LIKE %s"
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    # Ajoute la clause de filtre sur l'intervalle de prix si sélectionné
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " prix_inscription BETWEEN %s AND %s"
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "

    if "filter_types" in session:

        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + " type_sport_id = %s "
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)

        sql = sql + ")"
    tuple_sql = tuple(list_param)

    print(sql)
    mycursor.execute(sql,tuple_sql)
    sports = mycursor.fetchall()
    return render_template('filtres/front_sport_filtre_show.html', types_sports=types_sports, sports=sports)

@app.route('/filtres/show', methods=['POST'])
def edit_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min= request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word:" + filter_word + str(len(filter_word)))

    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'votre Mot recherché doit uniquement être composé de lettres', 'alert-info')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres', 'alert-info')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:

        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():

            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash (u'min < max', 'alert-info')
        else:
            flash(u'min et max doivent être des numériques' , 'alert-info')

    if filter_types and filter_types != []:
        session['filter_types'] = filter_types
    return redirect('/filtres/show')

@app.route('/filtres/clear')
def filtres_clear():
    session.clear()
    message = u'Filter has been successfully deleted'
    flash(message, 'alert-warning')
    return redirect('/filtres/show')


#------------------------------Etat---------------------------#

@app.route('/etat/show')
def show_etat():
    mycursor = get_db().cursor()

    sql = "SELECT t.id_type_sport as id_type_sport, t.libelle as libelle, COUNT(s.id_sport) as type_sport_count, SUM(s.prix_inscription * s.nb_pratiquants) as total_inscription_by_cat FROM type_sport t INNER JOIN sport s ON t.id_type_sport = s.type_sport_id GROUP BY t.id_type_sport, t.libelle ORDER BY t.id_type_sport;"
    mycursor.execute(sql)
    results = mycursor.fetchall()

    sql = "SELECT SUM(prix_inscription * nb_pratiquants) AS total_inscription, SUM(nb_pratiquants) as total_pratiquant FROM sport;"
    mycursor.execute(sql)
    result_tot = mycursor.fetchall()

    return render_template('show_etat.html', results=results, result_tot=result_tot)