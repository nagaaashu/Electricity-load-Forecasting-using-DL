import mysql
from flask import Flask,render_template,request
from mysql import connector
import pandas as pd
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine
import numpy as np
from numpy import array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import GRU
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import math
app=Flask(__name__)
mydb = mysql.connector.connect(host='localhost',user='root',password="",port='3307',database='electricity')

@app.route('/')
def index():
    return render_template('index.html')
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


@app.route('/load', methods=["GET", "POST"])
def load():
    df = pd.read_csv(r'energy_dataset.csv')
    dummy = df.head(100)
    table_html = dummy.to_html(classes='table table-striped')  
    return render_template('load.html', msg='Dataset Uploaded Successfully to the Database', table=table_html)



@app.route('/uhome')
def uhome():
    return render_template('uhome.html')


@app.route('/forecast', methods=["POST", "GET"])
def forecast():
    if request.method == 'POST':
        # Retrieve the forecast horizon
        abc = int(request.form['forecast'])

        # Load and preprocess the dataset
        df = pd.read_csv(r'energy_dataset.csv')
        df1 = df.reset_index()['total load forecast']

        scaler = MinMaxScaler(feature_range=(0, 1))
        df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))

        # Split into train and test sets
        training_size = int(len(df1) * 0.65)
        train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]

        # Define function to create dataset matrices based on time_step
        def create_dataset(dataset, time_step=22690):
            dataX, dataY = [], []
            for i in range(len(dataset) - time_step - 1):
                dataX.append(dataset[i:(i + time_step), 0])
                dataY.append(dataset[i + time_step, 0])
            return np.array(dataX), np.array(dataY)

        # Using time_step = 22690 as expected by the model
        # Using time_step = 22690 as expected by the model
        time_step = 22690
        if len(train_data) > time_step and len(test_data) > 0 :
            X_train, y_train = create_dataset(train_data, time_step)
            # X_test, y_test = create_dataset(test_data, time_step)

            # Reshape for the model input
            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
            # X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

            # Load the pre-trained model
            new_model = load_model('model.h5')
            
            # Generate predictions and inverse transform to original scale
            train_predict = new_model.predict(X_train)
            # test_predict = new_model.predict(X_test)

            train_predict = scaler.inverse_transform(train_predict)
            # test_predict = scaler.inverse_transform(test_predict)

            # Calculate RMSE
            train_rmse = math.sqrt(mean_squared_error(y_train, train_predict))
            # test_rmse = math.sqrt(mean_squared_error(y_test, test_predict))

            # Forecast future values
            x_input = train_data[-time_step:].reshape(1, -1)
            temp_input = x_input[0].tolist()
            
            lst_output = []
            i = 0
            while i < 5:
                x_input = np.array(temp_input[-time_step:]).reshape((1, time_step, 1))
                yhat = new_model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                lst_output.append(yhat[0][0])
                i += 1

            # Inverse transform the forecasted results
            result = scaler.inverse_transform(np.array(lst_output).reshape(-1, 1))
            # Return the result to the template
            return render_template('forecast.html', msg="success", result=result)
        else:
            return render_template('forecast.html', msg="Insufficient data for the required time_step.")

    return render_template('forecast.html')
@app.route('/about')
def about():
    return render_template('about.html')
if __name__=="__main__":
    app.run(debug=True)
