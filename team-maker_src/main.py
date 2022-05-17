from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def image_number(hero):
    n = hero % 10
    m = hero // 10
    first_part = str(m) + "0"
    second_part = str(n)
    if m < 10:
        first_part = "0" + first_part
    return "/static/Images/Unit_10" + first_part + "_" + second_part + ".png"


class Saves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, primary_key=True)
    code = db.Column(db.String(60), primary_key=True)

    def __repr__(self):
        return '<Saves %r>' % self.id


class Barraks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(60), primary_key=True)
    href_1 = db.Column(db.String(60), primary_key=True)
    href_2 = db.Column(db.String(60), primary_key=True)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(60), primary_key=True)
    href_1 = db.Column(db.String(60), primary_key=True)


class Heroes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(60), primary_key=True)
    href_1 = db.Column(db.String(60), primary_key=True)


count_skins = [0, 4, 9, 14, 19, 25, 31, 35, 39, 43, 47, 50, 54, 58, 62, 68, 74, 80, 84, 88, 92, 97, 101, 106, 108, 112, 115, 118, 121, 125, 127, 130, 131, 133]
position = 0
hero = 0

barraks_list = Barraks.query.order_by(Barraks.id).all()
hero_list = Heroes.query.order_by(Heroes.id).all()
team_list = Team.query.order_by(Team.id).all()


@app.route('/')
def index():
    return render_template('main_page.html', team_list=team_list, barraks_list=barraks_list)


@app.route('/save', methods=['POST', 'GET'])
def index_save():
    if request.method == "POST":
        name = request.form['name']
        code = ""
        for i in range(6):
            code += team_list[i].image[22] + team_list[i].image[23] + team_list[i].image[26]
        save = Saves(id=Saves.__repr__(Saves), name=name, code=code)
        db.session.add(save)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('save_page.html', team_list=team_list)


@app.route('/load', methods=['POST', 'GET'])
def index_load():
    if request.method == "POST":
        code = request.form['code']
        return redirect('/' + code)
    else:
        saves = Saves.query.order_by(Saves.id).all()
        return render_template('load_page.html', saves=saves)


@app.route('/<int:code>')
def index_craft(code):
    k = code
    for i in range(5, -1, -1):
        team_list[i].image = image_number(k % 1000)
        k //= 1000
    return redirect('/')


@app.route('/position/<int:number>')
def index_position(number):
    global position
    position = number
    return render_template('position_page.html', team_list=team_list, barraks_list=barraks_list, pos=number + 1)


@app.route('/position/change/<int:hero>')
def index_position_change(hero):
    team_list[position].image = barraks_list[hero].image
    href = '/position/' + str(position)
    return redirect(href)


@app.route('/hero/<int:number>')
def index_hero(number):
    global hero
    hero = number
    return render_template('hero_page.html', barraks_list=barraks_list[number], hero_list=hero_list[count_skins[number]:count_skins[number + 1]], hero_name=barraks_list[number].name)


@app.route('/hero/change/<int:hero_id>')
def index_hero_change(hero_id):
    barraks_list[hero].image = image_number(hero_id)
    href = '/hero/' + str(hero)
    return redirect(href)


if __name__ == "__main__":
    app.run(debug=True)
