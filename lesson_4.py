from flask import Flask, render_template, request, flash, url_for, redirect
from peewee import IntegrityError, fn

from config_data import DEBUG, SECRET_KEY
from models import English

app = Flask(__name__)
app.config.from_object(__name__)

lst_main_menu = [{"name": "Главная", "url": "/"},
                 {"name": "Добавить", "url": "/add"},
                 {"name": "Обновить", "url": "/update"},
                 {"name": "Удалить", "url": "/delete"},
                 {"name": "Просмотр", "url": "/show"}]


@app.route('/')
def index():
    return render_template('index.html', title='Главная', lst_main_menu=lst_main_menu)


# ADD
@app.route('/add')
def add():
    return render_template('add.html', title='Добавить', lst_main_menu=lst_main_menu)


@app.route('/add_word', methods=['POST'])
def input_data():
    if request.method == 'POST':
        word = request.form['word'].capitalize()
        translate = request.form['translate'].capitalize()
        try:
            if English.create(word=word, translate=translate):
                flash(f'Слово <b>{word}</b> и его перевод <b>{translate}</b> добавлены', category='success')

        except IntegrityError:
            flash(f'Слово <b>{word}</b> в базе существует!', category='attention')

        return render_template('add.html', lst_main_menu=lst_main_menu)

    else:
        return redirect(url_for('add_word'))


@app.route('/update')
def update():
    return render_template('update.html', title='Обновить', lst_main_menu=lst_main_menu)


@app.route('/delete')
def delete():
    return render_template('delete.html', title='Удалить', lst_main_menu=lst_main_menu)


@app.route('/show')
def show():
    return render_template('show.html', title='Просмотр', lst_main_menu=lst_main_menu)


# SHOW
@app.route('/show')
def all_notes_page():
    count_words = len(English.select())
    return render_template('show.html', count_words=count_words, lst_main_menu=lst_main_menu)


@app.route('/random_note')
def random_note():
    count_words = len(English.select())
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('random_note.html', random_query=one_obj, count_words=count_words, lst_main_menu=lst_main_menu)


@app.route('/all_notes', methods=['get'])
def all_notes():
    query_all = English.select()
    count_words = len(English.select())
    return render_template('all_notes.html', query_all=query_all, count_words=count_words, lst_main_menu=lst_main_menu)


@app.route('/count_notes', methods=['post'])
def count_notes():
    if request.method == 'POST':
        count = request.form['count']
        query_count = English.select().limit(count)
        return render_template('count_notes.html', query_count=query_count, lst_main_menu=lst_main_menu)


if __name__ == '__main__':
    app.run(debug=DEBUG, port=5555)
