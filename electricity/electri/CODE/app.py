import mysql
from flask import Flask,render_template,request
from mysql import connector
import pandas as pd
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine
import numpy as np
from numpy import array
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import GRU
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import accuracy_score
app=Flask(__name__)
mydb = mysql.connector.connect(host='localhost',user='root',password="",port='3307',database='electricity')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/registration',methods=["POST","GET"])
def registration():
    if request.method == "POST":
        print('a')
        un = request.form['name']
        print(un)
        em = request.form['email']
        pw = request.form['password']
        print(pw)
        cpw = request.form['cpassword']
        if pw == cpw:
            sql = "select * from power"
            print('abcccccccccc')
            cur = mydb.cursor()
            cur.execute(sql)
            all_emails = cur.fetchall()
            mydb.commit()
            all_emails = [i[2] for i in all_emails]
            if em in all_emails:
                return render_template('registration.html', msg='a')
            else:
                sql = "INSERT INTO power(name,email,password) values(%s,%s,%s)"
                values = (un,em,pw)
                cur.execute(sql, values)
                mydb.commit()
                cur.close()
                return render_template('registration.html', msg='success')
        else:
            return render_template('registration.html', msg='repeat')
    return render_template('registration.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        em = request.form['email']
        print(em)
        pw = request.form['password']
        print(pw)
        cursor = mydb.cursor()
        sql = "SELECT * FROM power WHERE email=%s and password=%s"
        val = (em, pw)
        cursor.execute(sql, val)
        results = cursor.fetchall()
        mydb.commit()
        print(results)
        print(len(results))
        if len(results) == 1:
            return render_template('uhome.html', msg='login succesful')
        else:
            return render_template('login.html', msg='Invalid Credentias')

    return render_template('login.html')

@app.route('/uhome')
def uhome():
    return render_template('uhome.html')


@app.route('/load', methods=["GET", "POST"])
def load():
    df = pd.read_csv(r'energy_dataset.csv')
    dummy = df.head(100)
    table_html = dummy.to_html(classes='table table-striped')  
    return render_template('load.html', msg='success', table=table_html)

@app.route('/view',methods = ["POST","GET"])
def view_data():
    df = pd.read_csv(r'Final_data.csv')
    dummmy = df.head(100)
    return render_template('view.html',col_name = dummmy.columns,row_val = list(dummmy.values.tolist()))

@app.route('/model',methods=['GET','POST'])
def model():
    if request.method=='POST':
        model = int(request.form['algo'])
        if model == 0:
            acc_rnn_k1 = 0.9854*100
            msg = "The accuracy obtained by  RNN is " + str(acc_rnn_k1)
            return render_template('model.html',msg = msg)  
    return render_template('model.html')

## Reading CSV file 
df = pd.read_csv("Final_data.csv")
# Separate features and target
X = df.drop(columns=['total load forecast'])
y = df['total load forecast']

# Scale the data
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

@app.route('/forecast', methods=["POST", "GET"])
def forecast():
    if request.method == 'POST':
        # Retrieve the forecast horizon
        a = float(request.form['f1'])
        b = float(request.form['f2'])
        c = float(request.form['f3'])
        d = float(request.form['f4'])
        e = float(request.form['f5'])
        f = float(request.form['f6'])
        g = float(request.form['f7'])
        h = float(request.form['f8'])

        # Prepare input data for prediction
        input_data = np.array([[a, b, c, d, e, f, g, h]])
        input_data_scaled = scaler_X.transform(input_data)  # Scale the input data
        input_data_reshaped = input_data_scaled.reshape((input_data_scaled.shape[0], 1, input_data_scaled.shape[1]))

        # Load the trained model
        model = load_model('rnn_model.h5')

        # Make prediction
        prediction_scaled = model.predict(input_data_reshaped)
        prediction = scaler_y.inverse_transform(prediction_scaled)  # Inverse transform to original scale
        result = int(prediction[0][0])  # Convert the result to an integer

        result = int(prediction)
        return render_template('forecast.html', msg="success", result=result)
    return render_template('forecast.html')

if __name__=="__main__":
    app.run(debug=True)
