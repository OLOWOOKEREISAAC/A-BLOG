from flask import Blueprint, request, render_template
from datetime import datetime
from app.models import Post


main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.posted.desc()).paginate(per_page= 4, page = page ) 
    return render_template('main/index.html', current_time=datetime.utcnow(), posts = posts )