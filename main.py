from flask import Flask, request, make_response, render_template
from googletrans import Translator
import sqlite3
import wikipediaapi
from connect import db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app = Flask(__name__, template_folder="templates")
app = Flask(__name__, static_folder="static")
db = db('db/notebook.db')

def sql_select():
    with sqlite3.connect('db/notebook.db', check_same_thread=False) as con:
        cursor = con.cursor()
        cursor.execute("""SELECT User.fio, Notes.note, Notes.link_site FROM Link_Obj
INNER JOIN User ON Link_Obj.id_obj1 = User.id_obj
INNER JOIN Notes ON Link_Obj.id_obj2 = Notes.id_obj""")
        all_result = cursor.fetchall()
        print(all_result)
        con.commit()
        return all_result

@app.route('/')
def index():
    id_zap, name, text = "link", "Zhenya", "Мама мыла раму!!! А сын бегал по улице."
    temp_context = dict(id_zap = id_zap, user = name, text_sub = text)
    res = sql_select()
    for r in res:
        name = r[0]
        text = r[1]
        link = r[2]
        temp_context.update(id_zap = str(link), user = name, text_sub = text)
    return render_template('index.html', **temp_context)

def http_404_handler():
    return make_response("<h2>404 Error</h2>", 400)

@app.route('/<page>/')
def not_list(page):
    translator = Translator(service_urls=['translate.googleapis.com'])
    translation = translator.translate('{}'.format(str(page)), src='en',dest='ru')
    wiki_wiki = wikipediaapi.Wikipedia('ru')


    page_ru = wiki_wiki.page("{}".format(str(translation.text)))

    return render_template('error.html', name=page, info=str(page_ru.summary[0:1000]) )

@app.route('/notebooks/<genre>')
def books(genre):
    res = make_response("Все записи в записной книги {}".format(genre))
    res.headers['Content-Type'] = 'text/paint'
    res.headers['Server'] = 'Foobar'


if __name__ == '__main__':
    app.run()