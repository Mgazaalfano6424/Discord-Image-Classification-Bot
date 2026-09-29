#Import
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Menghubungkan SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Membuat sebuah DB
db = SQLAlchemy(app)

# Membuat sebuah tabel card
class Card(db.Model):
    # Membuat kolom-kolom
    # id(kolom #1)
    id = db.Column(db.Integer, primary_key=True)
    # Judul
    email = db.Column(db.String(100), nullable=False)
    # Teks up to 30 000 char
    text = db.Column(db.Text, nullable=False)

    #Parameterized Constructor accepts additional arguments
    def __init__(self, email, text):
        self.email = email
        self.text = text

    # Menampilkan objek dan id
    # The __repr__ method is a special method in Python that defines how an object 
    # should be represented as a string. 
    # It is used to provide a human-readable representation of the object, typically 
    # for debugging purposes.
    def __repr__(self):
        return f'<Card {self.id}>'

#Halaman Konten Berjalan
@app.route('/')
def index():
    return render_template('index.html')


#Keterampilan Dinamis
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    button_discord = request.form.get('button_discord')
    button_html = request.form.get('button_html')
    
    

# Formulir entri
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        email =  request.form['email']
        text =  request.form['text']

        # Membuat objek yang akan dikirim ke DB
        card = Card(email=email, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
