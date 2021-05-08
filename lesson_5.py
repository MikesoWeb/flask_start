from flask import Flask, render_template, request, redirect, url_for, flash
from peewee import IntegrityError, fn
from models import English
from config_data import DEBUG, SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

lst_main_menu = [{"name": "Главная", "url": "/"},
                 {"name": "Добавить", "url": "/add"},
                 {"name": "Обновить", "url": "/update_page"},
                 {"name": "Удалить", "url": "/delete_page"},
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


# UPDATE
@app.route('/update_page')
def update():
    count_words = len(English.select())
    return render_template('update.html', title='Обновить', lst_main_menu=lst_main_menu, count_words=count_words)


@app.route('/update', methods=['post', 'get'])
def update_data():
    if request.method == 'POST':
        words = request.form['word'].capitalize()
        if English.select().where(English.word == words):
            word_upd = request.form['translate'].capitalize()
            q = English.update(translate=word_upd).where(English.word == words)
            q.execute()
            flash(f'У слова <b>{words}</b> был обновлен перевод на <b>{word_upd}</b>!', category='attention')
        else:
            flash(f'Слово <b>{words}</b> не найдено в базе!', category='error')

        return render_template('update.html', lst_main_menu=lst_main_menu)


# DELETE
@app.route('/delete_page')
def delete():
    count_words = len(English.select())
    return render_template('delete.html', title='Удалить', lst_main_menu=lst_main_menu, count_words=count_words)


@app.route('/delete', methods=['post', 'get'])
def delete_data():
    if request.method == 'POST':
        word = request.form['word'].capitalize()
        del_word = English.select().where(English.word == word)
        if not del_word:
            flash(f'Слово <b>{word}</b> в базе не найдено!', category='error')
        else:
            English.delete_by_id(del_word)
            flash(f'Слово <b>{word}</b> удалено!', category='success')

    return render_template('delete.html', lst_main_menu=lst_main_menu)


# SHOW
@app.route('/show')
def show():
    count_words = len(English.select())
    return render_template('show.html', title='Просмотр', lst_main_menu=lst_main_menu, count_words=count_words)


@app.route('/random_note')
def random_note():
    count_words = len(English.select())
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('random_note.html', random_query=one_obj, count_words=count_words,
                           lst_main_menu=lst_main_menu)


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
