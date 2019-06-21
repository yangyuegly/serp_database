import sqlite3
from flask import g, Flask, render_template
app = Flask(__name__)



@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    return render_template('search.html', form=form)