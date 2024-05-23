from flask import Flask, render_template, request, redirect, url_for
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    if request.method == 'POST':
        try:
            hobby = request.form.getlist('hobbies')
            hobbies = ",".join(hobby)

            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            gender = request.form.get('gender')
            country = request.form.get('country')

            print("Données reçues du formulaire:")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print(f"Gender: {gender}")
            print(f"Hobbies: {hobbies}")
            print(f"Country: {country}")

            if not all([first_name, last_name, email, password, gender, country]):
                return "Tous les champs sont obligatoires", 400

            student = StudentModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                gender=gender,
                hobbies=hobbies,
                country=country
            )
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Erreur: {e}")
            return "Une erreur s'est produite", 500

@app.route('/', methods=['GET'])
def RetrieveList():    
    students = StudentModel.query.all()
    return render_template('index.html', students=students)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    student = StudentModel.query.filter_by(id=id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return redirect('/')
    else:
        return "L'étudiant n'existe pas", 404

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        try:
            student.first_name = request.form.get('first_name')
            student.last_name = request.form.get('last_name')
            student.email = request.form.get('email')
            student.password = request.form.get('password')
            student.gender = request.form.get('gender')
            hobby = request.form.getlist('hobbies')
            student.hobbies = ",".join(hobby)
            student.country = request.form.get('country')

            if not all([student.first_name, student.last_name, student.email, student.password, student.gender, student.country]):
                return "Tous les champs sont obligatoires", 400

            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Erreur: {e}")
            return "Une erreur s'est produite", 500

    return render_template('update.html', student=student)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        students = StudentModel.query.filter(
            (StudentModel.first_name.contains(query)) |
            (StudentModel.last_name.contains(query)) |
            (StudentModel.email.contains(query)) |
            (StudentModel.country.contains(query))
        ).all()
    else:
        students = StudentModel.query.all()
    return render_template('index.html', students=students, query=query)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
