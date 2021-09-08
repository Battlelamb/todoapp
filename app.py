from typing import Optional
from flask import Flask, render_template, redirect, url_for, jsonify
from flask.globals import request
from wtforms import Form, StringField, validators, DateField
from flask_mongoengine import MongoEngine
from uuid import uuid4
from datetime import date, datetime

app = Flask(__name__)

# Veritabanı bağlantısı
app.config['MONGODB_SETTINGS'] = {
    "db": "todo_app_data",
    "host": "localhost",  # 196.15.16.287
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

# Kullanıcı Sınıfı


class User(db.Document):
    _id = db.StringField()
    uuid = db.StringField()
    firstname = db.StringField()
    lastname = db.StringField()
    adres = db.StringField()

    def to_json(self):
        return {
            "_id": self._id,
            "uuid": self.uuid,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "adres": self.adres
        }  # json Object


# class Task
class Task(db.Document):
    uuid = db.StringField()
    taskname = db.StringField()
    taskduration = db.StringField()
    taskstate = db.StringField()
    taskstart = db.StringField()
    taskend = db.StringField()

    def to_json(self):
        return {
            "uuid": self.uuid,
            "taskname": self.taskname,
            # Json objelerinde boşluk bırakmadan camelcase veya alttan çizgi ile ayırabiliriz
            "taskduration": self.taskduration,
            "taskstate": self.taskstate,
            "taskstart": self.taskstart,
            "taskend": self.taskend
        }

# Kayıt Formu


class RegisterForm(Form):
    firstname = StringField(u'First Name', validators=[
                            validators.input_required()])
    lastname = StringField(u"Last Name", validators=[validators.optional()])
    adres = StringField(u'Adres', validators=[validators.optional()])


# Task Formu
class TaskForm(Form):
    taskname = StringField(u'Task Name', validators=[
                           validators.input_required()])
    taskduration = StringField(u'Task Duration', validators=[
                               validators.optional()])
    taskstart = StringField(u'Task Start Date', validators=[
                            validators.input_required()], default=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    taskstate = StringField(u'Task State', validators=[
                            validators.optional()], default="Aktif")
    taskend = StringField(u'Task End Date', validators=[validators.optional()])


@app.route("/")  # => http://127.0.0.1:5000/ = https://www.hepsiburada.com/
def index():

    number = 10
    sayilar = [1, 2, 3, 4, 5]
    isim = "Ömer"

    return render_template("index.html", number=number, sayilar=sayilar, isim=isim)


# => http://127.0.0.1:5000/about = https://www.hepsiburada.com/about
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/article/<string:id>")
def article(id):
    return "Article Id = " + id
    # UID => unique identifier => Eşsiz tanımlama

# Register Page Start


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == "POST":  # Sunucuya Gönderme İşlemi

        firstname = form.firstname.data  # data == text == değeri
        lastname = form.lastname.data
        adres = form.adres.data
        uuid = uuid4().hex

        # now_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # taskcreatedate = now_time

        user = User(firstname=firstname, lastname=lastname,
                    adres=adres, uuid=uuid)
        user.save()

        return redirect(url_for("register"))
    else:
        users = list(User.objects.all())

        return render_template("register.html", form=form, users=users)

# /tasksave, /tasks, /addtask, /taskadd


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    form = TaskForm(request.form)

    if request.method == "POST":
        taskname = form.taskname.data
        taskduration = form.taskduration.data
        taskstart = form.taskstart.data
        # taskstart = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        taskstate = form.taskstate.data
        taskend = form.taskend.data
        uuid = uuid4().hex

        task = Task(taskname=taskname, taskduration=taskduration,
                    taskstart=taskstart, taskstate=taskstate, taskend=taskend, uuid=uuid)

        task.save()

        return redirect(url_for("tasks"))

    else:
        tasks = list(Task.objects.all())
        activeTasks = []
        finishedTasks = []
        canceledTasks = []

        for task in tasks:
            if task.taskstate == "Aktif":
                activeTasks.append(task)
        for task in tasks:
            if task.taskstate == "Pasif":
                canceledTasks.append(task)
        for task in tasks:
            if task.taskstate == "Done":
                finishedTasks.append(task)

        return render_template("tasks.html", form=form, tasks=tasks, activeTasks=activeTasks, canceledTasks=canceledTasks)


@app.route("/delete-task/<id>", methods=["GET"])
def delete_task(id):
    try:
        task = Task.objects(uuid=str(id)).delete()
        if(task):
            print("Görev başarı ile silindi")
            return redirect(url_for("tasks"))
        else:
            print("Bir sorun oluştu")

    except Exception as ex:
        print("((((", ex, "))))")

    return redirect(url_for("tasks"))


@app.route("/passive-task/<id>", methods=["GET"])
def passive_task(id):
    try:
        task = Task.objects(uuid=str(id)).update(taskstate="Pasif")
        if(task):
            print("Görev başarı ile pasif yapıldı")
            return redirect(url_for("tasks"))
        else:
            print("Bir sorun oluştu")
    except Exception as ex:
        print("((((", ex, "))))")


@app.route("/delete-user/<id>", methods=["GET"])
def delete_user(id):
    try:
        # print("ID: ", id)
        # user = User.objects(uuid=str(id)).first()
        # usermuser = User.objects.get_or_404(uuid=str(id))
        # body = jsonify(usermuser)
        # print("Body", body)

        # for i in usermuser:
        #     print(i, ":", usermuser[i])

        # someObjectWithNewData = {
        #     "firstname": "pato", "lastname": usermuser.lastname, "uuid": usermuser.uuid, "adres": usermuser.adres
        # }
        # usermuser.save(firstname="pato")

        # patos = usermuser.update(firstname="pato")

        # print("PATOS", patos)

        # for i in usermuser:
        #     print(i, ":", usermuser[i])

        # usermuser.firstname = "pato"

        # patos = usermuser.update(**{"firstname":"pato"})

        # print("Muer:", usermuser.firstname)
        # print("PATOS", patos)
        # if(usermuser):
        # patos = usermuser.update(firstname="pato")
        # print("PATOS", patos)
        # usermuser.firstname = "pato"
        # usermuser.save()
        # return redirect(url_for("register"))

        # 0 veya 1 döndürüyor # 0 == false, 1 == true
        user = User.objects(uuid=str(id)).delete()

        if(user):
            print("Tamamdır, kullanıcı silindi")
        else:
            print("Silme sırasında bir hata oluştu.")

    except Exception as ex:
        # ex Örnekleri => 1- Sunucu ile bağlantı kurulamadı 2- Versiyon uyuşmazlığı 3- hatalı kayıt
        print("((((", ex, "))))")

    return redirect(url_for("register"))

# Register Page End

# @app.route("/layout") # => http://127.0.0.1:5000/layout
# def layout():
#     return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
