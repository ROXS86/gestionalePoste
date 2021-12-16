from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import time
from werkzeug.exceptions import abort

from schedePoste.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        if(request.form['cognome'] != '' and request.form['nome'] != ''):
            db = get_db()
            results = db.execute(
                'SELECT *'
                ' FROM user'
                ' WHERE cognome= ? AND nome= ?',
                (str(request.form['cognome']),str(request.form['nome']))
            ).fetchall()
        elif(request.form['cognome'] != ''):
            db = get_db()
            results = db.execute(
                'SELECT *'
                ' FROM user'
                ' WHERE cognome= ?',
                (str(request.form['cognome']),)
            ).fetchall()
        elif(request.form['matricola'] != ''):
            db = get_db()
            results = db.execute(
                'SELECT *'
                ' FROM user'
                ' WHERE matricola= ?',
                (str(request.form['matricola']),)
            ).fetchall()
        else:
            if(request.form['cf'] != ''):
                db = get_db()
                results = db.execute(
                    'SELECT *'
                    ' FROM user'
                    ' WHERE cf= ?',
                    (str(request.form['cf']),)
                ).fetchall()
            else:
                return render_template('blog/index.html',num=0)

        print(type(results))
        print(len(results))

        return render_template('blog/index.html', results=results, num=len(results),get=0)

    else:
        return render_template('blog/index.html',num=0, get=1)

@bp.route('/<int:id>/scheda', methods=('GET', 'POST'))
def scheda(id):
    db = get_db()
    scheda = db.execute(
        'SELECT *'
        ' FROM user'
        ' WHERE id= ?',
        (str(id),)
    ).fetchone()

    mansioni = db.execute(
        'SELECT descrizione, dal, al, ufficio'
        ' FROM mansioni'
        ' WHERE mansioni_id= ?',
        (str(id),)
    ).fetchall()

    corsi = db.execute(
        'SELECT descrizione, dal, al, valutazione, data_val, esito'
        ' FROM corsi'
        ' WHERE corsi_id= ?',
        (str(id),)
    ).fetchall()
    return render_template('blog/scheda.html', scheda=scheda, mansioni=mansioni, corsi=corsi)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        keys = ""
        values = ""
        append = ""
        num = 1
        for k, v in request.form.items():
            if k != 'descrizione_m[]' and k != 'ufficio_m[]' and k != 'dal_m[]' and k != 'al_m[]' and k != 'descrizione_cc[]'  and k != 'dal_cc[]'  and k != 'al_cc[]'  and k != 'valutazione[]'  and k != 'data_valutazione[]'  and k != 'esito[]':
                keys += str(k)
                val = "'"+str(v)+"'"
                values += val
                append += '?'

                if(num < 21):
                    keys += ","
                    values += ","
                    append += ","

                num +=1

        db = get_db()
        lastRowId = db.execute(
            'INSERT INTO user ('+keys+')'
            ' VALUES ('+values+')'
            ).lastrowid

        db.commit()




        #add mansioni
        ts = time.time()
        desc_list = list(request.form.getlist('descrizione_m[]'))
        if len(desc_list) > 0:
            uff_list = list(request.form.getlist('ufficio_m[]'))
            dal_list = list(request.form.getlist('dal_m[]'))
            al_list = list(request.form.getlist('al_m[]'))
            for i in range(len(desc_list)):
                if al_list[i] == "":
                    al_list[i] = "0"
                db.execute(
                    'INSERT INTO mansioni (mansioni_id, created, descrizione, dal, al, ufficio) '
                    'VALUES ("'+str(lastRowId)+'","111111","'+str(desc_list[i])+'","'+str(dal_list[i])+'","'+str(al_list[i])+'","'+str(uff_list[i])+'")'
                )
                db.commit()

        # add corsi
        desc_list_c = list(request.form.getlist('descrizione_cc[]'))
        if len(desc_list_c) > 0:
            dal_list_c = list(request.form.getlist('dal_cc[]'))
            al_list_c = list(request.form.getlist('al_cc[]'))
            valutazione = list(request.form.getlist('valutazione[]'))
            data_valutazione = list(request.form.getlist('data_valutazione[]'))
            esito = list(request.form.getlist('esito[]'))
            for i in range(len(desc_list_c)):
                if al_list_c[i] == "":
                    al_list_c[i] = "0"
                if valutazione[i] == "":
                    valutazione[i] = "0"
                if data_valutazione[i] == "":
                    data_valutazione[i] = "0"
                if esito[i] == "":
                    esito[i] = "0"

                db.execute(
                    'INSERT INTO corsi (corsi_id, created, descrizione, dal, al, valutazione, data_val, esito) '
                    'VALUES ("' + str(lastRowId) + '","112222111","' + str(
                        desc_list_c[i]) + '","' + str(dal_list_c[i]) + '","' + str(al_list_c[i]) + '","' + str(valutazione[i]) + '","' + str(data_valutazione[i]) + '","' + str(esito[i]) + '")'
                )
                db.commit()

        return redirect(url_for('blog.scheda', id=lastRowId))

    else:
        return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        keys = ""
        values = ""
        append = ""
        num = 1
        for k, v in request.form.items():
            if k != 'descrizione_m[]' and k != 'ufficio_m[]' and k != 'dal_m[]' and k != 'al_m[]' and k != 'descrizione_cc[]' and k != 'dal_cc[]' and k != 'al_cc[]' and k != 'valutazione[]' and k != 'data_valutazione[]' and k != 'esito[]' and k != 'id_mansioni[]' and k != 'id_corsi[]':

                val = "'" + str(v) + "'"
                keys += str(k) + "= " +val
                values += val
                append += '?'

                if (num < 21):
                    keys += ","
                    values += ","
                    append += ","

                num += 1

        db = get_db()
        db.execute(
            'UPDATE user SET ' + keys + ''
            ' WHERE id = ? ',
            (str(id),)
        )
        db.commit()

        # update/add mansioni
        ts = time.time()
        desc_list = list(request.form.getlist('descrizione_m[]'))
        if len(desc_list) > 0:
            uff_list = list(request.form.getlist('ufficio_m[]'))
            dal_list = list(request.form.getlist('dal_m[]'))
            al_list = list(request.form.getlist('al_m[]'))
            id_mansioni = list(request.form.getlist('id_mansioni[]'))
            print(id_mansioni)
            print(desc_list)
            for i in range(len(desc_list)):
                if al_list[i] == "":
                    al_list[i] = "0"
                if (i < len(id_mansioni)):
                    db.execute(
                        'UPDATE mansioni SET mansioni_id = ?, created = ? , descrizione= ?, dal= ?, al= ?, ufficio = ?'
                        ' WHERE id = ?',
                        (str(id),"111111",str(desc_list[i]),str(dal_list[i]),str(al_list[i]),str(uff_list[i]),id_mansioni[i])
                    )
                else:
                    db.execute(
                        'INSERT INTO mansioni (mansioni_id, created, descrizione, dal, al, ufficio) '
                        'VALUES ("' + str(id) + '","111111","' + str(desc_list[i]) + '","' + str(
                            dal_list[i]) + '","' + str(al_list[i]) + '","' + str(uff_list[i]) + '")'
                    )
                db.commit()

        # add/update corsi
        desc_list_c = list(request.form.getlist('descrizione_cc[]'))
        if len(desc_list_c) > 0:
            dal_list_c = list(request.form.getlist('dal_cc[]'))
            al_list_c = list(request.form.getlist('al_cc[]'))
            valutazione = list(request.form.getlist('valutazione[]'))
            data_valutazione = list(request.form.getlist('data_valutazione[]'))
            esito = list(request.form.getlist('esito[]'))
            id_corsi = list(request.form.getlist('id_corsi[]'))
            for i in range(len(desc_list_c)):
                if al_list_c[i] == "":
                    al_list_c[i] = "0"
                if valutazione[i] == "":
                    valutazione[i] = "0"
                if data_valutazione[i] == "":
                    data_valutazione[i] = "0"
                if esito[i] == "":
                    esito[i] = "0"

                if (i < len(id_corsi)):
                    db.execute(
                        'UPDATE corsi SET corsi_id = ?, created = ?, descrizione = ?, dal= ?, al= ?, valutazione= ?, data_val= ?, esito = ?'
                        ' WHERE id = ?',
                        (str(id),"112222111",str(desc_list_c[i]) ,str(dal_list_c[i]) ,str(al_list_c[i]),str(valutazione[i]),str(data_valutazione[i]),str(esito[i]), id_corsi[i])
                    )
                else:
                    db.execute(
                        'INSERT INTO corsi (corsi_id, created, descrizione, dal, al, valutazione, data_val, esito) '
                        'VALUES ("' + str(id) + '","112222111","' + str(
                            desc_list_c[i]) + '","' + str(dal_list_c[i]) + '","' + str(al_list_c[i]) + '","' + str(
                            valutazione[i]) + '","' + str(data_valutazione[i]) + '","' + str(esito[i]) + '")'
                    )
                db.commit()

        return redirect(url_for('blog.scheda', id=id))
    else:
        db = get_db()
        scheda = db.execute(
            'SELECT *'
            ' FROM user'
            ' WHERE id= ?',
            (str(id),)
        ).fetchone()

        mansioni = db.execute(
            'SELECT descrizione, dal, al, ufficio, id'
            ' FROM mansioni'
            ' WHERE mansioni_id= ?',
            (str(id),)
        ).fetchall()

        corsi = db.execute(
            'SELECT descrizione, dal, al, valutazione, data_val, esito, id'
            ' FROM corsi'
            ' WHERE corsi_id= ?',
            (str(id),)
        ).fetchall()
        return render_template('blog/update.html', scheda=scheda, mansioni=mansioni, corsi=corsi)
