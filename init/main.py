import folium
from folium import plugins
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Connection import Error, get_db, close_db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cb02820a3e94d72c9f950ee10ef7e3f7a35b3f5b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questionnaire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    xCoor = db.Column(db.Float, nullable=False)
    yCoor = db.Column(db.Float, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    popup = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    m = folium.Map(location=[51.656859, 39.205926],
                   tiles='openstreetmap',
                   zoom_start=12)
    draw = plugins.Draw(export=True)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('CartoDB Positron').add_to(m)
    measure_control = plugins.MeasureControl(position='topleft',
                                             active_color='red',
                                             completed_color='red',
                                             primary_length_unit='miles')

    all_subgroups = folium.FeatureGroup(name='Хорошее место')
    group1 = plugins.FeatureGroupSubGroup(all_subgroups, 'Организации')
    group2 = plugins.FeatureGroupSubGroup(all_subgroups, 'Кафе')
    m.add_child(group1)
    m.add_child(group2)
    m.add_child(all_subgroups)

    tooltip = 'ВГУ'
    tooltip_2 = 'Oscar beef'
    tooltip_3 = 'Biga'
    tooltip_4 = 'Chayhona'
    tooltip_5 = 'Сулико'

    folium.Marker([51.656859, 39.205926], popup=('<a href="http://www.vsu.ru/"> Link </a>'), tooltip=tooltip,
                  icon=folium.Icon(color="red")).add_to(group1)
    folium.Marker([51.666888, 39.205913], popup=('<a href="https://oscarbeef.business.site/"> Link </a>'),
                  tooltip=tooltip_2, icon=folium.Icon(color="red")).add_to(group2)
    folium.Marker([51.674031, 39.208084], popup=('<a href="https://bigapizza.ru/"> Link </a>'), tooltip=tooltip_3,
                  icon=folium.Icon(color="red")).add_to(group2)
    folium.Marker([51.668914, 39.198823], popup=('<a href="https://chaihona.ru/vrg/> Link </a>'), tooltip=tooltip_4,
                  icon=folium.Icon(color="red")).add_to(group2)
    folium.Marker([51.658568, 39.204931], popup=('<a href="https://suliko-belucci.ru/> Link </a>'),
                  tooltip=tooltip_5,
                  icon=folium.Icon(color="red")).add_to(group2)

    draw.add_to(m)
    folium.LayerControl().add_to(m)
    m.add_child(measure_control)
    #    m.add_child(folium.LatLngPopup()) Под вопросом, иногда мешается
    m.save('name.html')
    return m._repr_html_()


@app.route('/register', methods=['GET', 'POST'])
def register():
    current_user = get_params_user()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter(User.name == name).first()

        if user is not None:
            return render_template('register.html', message="Пользователь уже существует", **current_user)

        admin = False
        if 'admin' in request.form:
            admin = True

        user = User(name=name, password=password, admin=admin)

        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('name'))
        except:
            return render_template('register.html', message="Неправильный ввод", **current_user)
    return render_template('register.html', **current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user = get_params_user()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter(User.name == name).first()

        if user is None or user.password != password:
            return render_template('login.html', message="Неверные данные", **current_user)
        else:
            session['user_id'] = user.id
            return redirect(url_for('name'))
    return render_template('login.html', **current_user)

def get_params_user():
    name = None
    status = None
    if 'user_id' in session:
        connection, cursor = get_db
        cursor.execute(
            f'''
                        SELECT name, status_id
                        FROM user
                        WHERE id_user = %(id_user)s;
                    '''
            , {'id_user': session['user_id']}
        )
        user = cursor.fetchall()
        if len(user) > 0:
            name = user[0][0]
            status = user[0][1]
        close_db(connection, cursor)
    return dict(name=name, admin=status == 1)


# 51.656859, 39.205926
# 51.666888, 39.205913 Oscar beef
# 51.674031, 39.208084 Biga
# 51.668914, 39.198823 Chayhona
# 51.658568, 39.204931 Сулико

if __name__ == "__main__":
    app.run(debug=True)
