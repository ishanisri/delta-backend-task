from flask import render_template,redirect, request, flash,g,session,url_for,Flask

import sqlite3 as sql
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key="why would i tell my secret key?"


from flask import g

DATABASE = '/path/to/task.db'
  




@app.route("/")
def main():
    return render_template('index.html')
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html') 
@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html') 

@app.route('/showAppointmentsPage')
def showCreateNotes():
    return render_template('appointments.html') 
   

@app.route('/signUp',methods=['GET','POST'])
def signedUp():
    if(request.method=='POST'):
        username= request.form.get('inputName')
        email = request.form.get('inputEmail')
        password=request.form.get('inputPassword')
        
        print(username+" "+email+" "+password)
        hashed_password = generate_password_hash(password)
        print(hashed_password)
        
        print("hi")	
        
        with sql.connect("task.db") as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS account_holder( user_id INTEGER NOT NULL AUTOINCREMENT,user_email TEXT DEFAULT NULL,username TEXT NOT NULL PRIMARY KEY,password TEXT DEFAULT NULL)")
            cur.execute("INSERT INTO account_holder (user_email,username,password) VALUES (?,?,?)", (email,username,hashed_password))
            cur.execute("CREATE TABLE IF NOT EXISTS APPOINTMENTS(id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,ap_username TEXT  ,title TEXT DEFAULT NULL,description TEXT DEFAULT NULL,apDate TEXT DEFAULT NULL,startTime TEXT DEFAULT NULL,endTime TEXT DEFAULT NULL,FOREIGN KEY(ap_username) REFERENCES account_holder(username))")
            
            
            
            cur.execute("SELECT * FROM account_holder where username=?",(username,))
            data=cur.fetchall()
            print(data)
            con.commit()

                                                                                         
        session['user']=username

        
 
           
    return redirect('/userHome') 
      
@app.route('/userHome')
def userHome():
	if session.get('user'):
	    conn = sql.connect("task.db")
	    cursor = conn.cursor()
	    _user=session.get('user')
	    
	    
	    cursor.execute("SELECT * FROM APPOINTMENTS where ap_username=(?) ORDER BY apDate",(_user,))
	    result = cursor.fetchall()
	    print(result)
	    result_dict=[]

	    i=1
	    for data in result:
			        data_dict= {
			                    'Date':data[4],
			                    'Title':data[2],
			                    'Description':data[3],
			                    
			                    'StartTime':data[5],
			                    'EndTime':data[6]}
		                     
			        result_dict.append(data_dict)
			        i=i+1

	            #if len(data) is 0:
	    
	    return render_template('userHome.html',result_dict=result_dict)
	else:
	    return render_template('error.html',error = 'Unauthorized Access')



@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')






  
@app.route('/createAppointment',methods=['GET','POST'])
def addWish():
    if(request.method=='POST'):
	    conn = sql.connect("task.db")
	    cursor = conn.cursor()
	    print(session.get('user'))
	    try:
	        if session.get('user'):
	            _title = request.form['inputTitle']
	            _description = request.form['inputDescription']
	            _date=request.form['inputDate']
	            _startTime=request.form['inputStartTime']
	            _endTime=request.form['inputEndTime']
	            _user = session.get('user')
	            print(_user)
	 
	            
	            #cursor.execute("CREATE TABLE IF NOT EXISTS APPOINTMENTS(id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,ap_username TEXT  ,title TEXT DEFAULT NULL,description TEXT DEFAULT NULL,apDate TEXT DEFAULT NULL,startTime TEXT DEFAULT NULL,endTime TEXT DEFAULT NULL)")
	            cursor.execute("INSERT INTO APPOINTMENTS(title,description,ap_username,apDate,startTime,endTime) VALUES(?,?,?,?,?,?)",(_title,_description,_user,_date,_startTime,_endTime))
	            

	            #if len(data) is 0:
	            conn.commit()
	            print("user in session"+_user)
	            
	            
	           # else:
	            #    return render_template('error.html',error = 'An error occurred!')
	 
	        
	           
	        else:
	           return render_template('error.html',error = 'An error occurred!')
	    except Exception as e:
	        return render_template('error.html',error = str(e))
	    finally:
	        cursor.close()
	        conn.close()       
    return redirect('/userHome')  



@app.route('/validateLogin',methods=['GET','POST'])
def validateLogin():
	if(request.method=='POST'):
	    con = sql.connect("task.db")
	    cur=con.cursor()
	    
	    try:
	        
	        username = request.form['inputName']
	        password = request.form['inputPassword']
	        cur.execute("SELECT * FROM account_holder where username=?",(username,))
	        print("hi")
	        data = cur.fetchall()
	        print(data)
	        if len(data) > 0:

	            if check_password_hash(str(data[0][3]),password):
	                print("inside check")
	                session['user'] = data[0][2]
	                
	            else:
	                return render_template('error.html',error = 'Wrong Email address or Password.')
	        else:
	            return render_template('error.html',error = 'Wrong Email address or Password!!!!')                  

	 
	    except Exception as e:
	        return render_template('error.html',error = str(e))
	    finally:
	        cur.close()
	        con.close()
	return redirect('/userHome')  




@app.route('/getList')
def getCheckedList():
	
	return redirect('/userHome')  

if __name__ == "__main__":
     app.run(debug=True)  											