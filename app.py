from flask import Flask,render_template,request
import pymysql as sql
import requests

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/afterlogin/',methods=['POST','GET'])
def after_login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Email:",email,"Password:",password)

        db = sql.connect(host='localhost',port=3306,user='root',password='',database='flask_1')
        cursor=db.cursor()
        quary = "select * from signup where email=%s and password=%s"
        cursor.execute(quary,(email,password))
        data = cursor.fetchone()
        if data is None:
            error="invaild email or password"
            return render_template('login.html',e=error)
        else:
            return render_template('afterlogin.html')
            
    else:
        return render_template('login.html')
    
@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/aftersignup',methods=['POST','GET'])
def after_sign():
    if request.method =='POST':
        name    = request.form.get('username')
        email   = request.form.get('email')
        password= request.form.get('password')
        re_pass = request.form.get('confirm')
        

        if password == re_pass:
            try:
                db = sql.connect(host='localhost',port=3306,user='root',password='',database='flask_1')
                cursor=db.cursor()
                quary = f"insert into signup values('{name}','{email}','{password}','{re_pass}')"
                cursor.execute(quary)
                db.commit()
                return render_template('login.html')
            except Exception as e:
                return e

        else:
            return 'password not match'
    return f"{name},{email},{password},{re_pass}"

@app.route('/todayweather/',methods=['POST','GET'])
def get_weather():
    city= request.form.get('City')
    api_key= 'fc0eb4fa32d87eb09209f188fa5e4cc0'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        tempreture = data['main'] ['temp']
        pressure   = data['main'] ['pressure']
        humidity   = data['main'] ['humidity']
        min_temp   = data['main'] ['temp_min']
        max_temp   = data['main'] ['temp_max']
    
        weather = {
        'Tempreture' :tempreture,
        'Pressure'   :pressure,
        'Humidity'   :humidity,
        'Min_temp'   :min_temp,
        'Max_temp'   :max_temp
        }
        return render_template('weather.html',weather=weather)
    else:
        return "Not found any data"        





 
app.run(debug=True)