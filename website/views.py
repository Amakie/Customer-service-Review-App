from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from .models import Review
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        review = request.form.get('review')#Gets the note from the HTML 

        if len(review) < 1:
            flash('Review is too short!', category='error') 
        else:
            new_review = Review(data=review, user_id=current_user.id)  #providing the schema for review 
            db.session.add(new_review) #adding a new review to the database 
            db.session.commit()
            flash('Review added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    review = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    reviewId = review['reviewId']
    review = Review.query.get(reviewId)
    if review:
        if review.user_id == current_user.id:
            db.session.delete(review)
            db.session.commit()

    return jsonify({})
