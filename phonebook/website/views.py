from unicodedata import category
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Entry
from . import db
import json
from flask.json import jsonify



views = Blueprint('views', __name__)

@views.route("/", methods=['POST', 'GET'])
def home():
    return render_template("home.html")

@views.route("/entries")
@login_required
def entries():
    if request.method == 'POST':
        entry = request.form.get('entry')

        if len(entry) < 1:
            flash('Entry is invalid', category='error')
        else:
            new_entry = Entry(data=entry, user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry is invalid', category='error')

    return render_template("entries.html")

@views.route('/delete-entry', methods=['POST'])
def delete_entry():
    entry = json.loads(request.data)
    entryid = entry['entryid']
    entry = Entry.query.get(entryid)
    if entry:
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commit()
            
    return jsonify({})

