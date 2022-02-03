from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from datetime import datetime

#App initialization
app = Flask(__name__)

#Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/elevator.db'

#Database cursor
db = SQLAlchemy(app)

#Database entity - demands
class Demands(db.Model):
    #Primary Key - integer value of demands
    id = db.Column(db.Integer, primary_key=True)
    #Objective level
    lvl_object = db.Column(db.Integer, default = 1)
    #Current level (random number)
    lvl_current = db.Column(db.Integer, default = 1)
    #Resting_lvl
    lvl_rest = db.Column(db.Integer, default = 1)
    #Demand date
    lvl_date = db.Column(db.DateTime, default = datetime.now())

#Demands table creation
db.create_all()

#App routes

#Home
@app.route('/')
def root():

    demands = Demands.query.all()
    demands2 = []
    
    #Build summary of each demand
    for demand in demands:
        
        if demand.id > 1:
            demands2.append(str(demand.lvl_date.strftime("%m/%d/%Y, %H:%M:%S")) + " Elevator resting on "+ str(demand.lvl_rest) +" and demand from level " + str(demand.lvl_current) + " to level " + str(demand.lvl_object))  
        else :
            demands2.append("Initial level is 1")
        
    global lvl_curr
    lvl_curr = np.random.randint(11, size=1)
    return render_template('index.html', demands2 = demands2, lvl_curr = (lvl_curr[0]))

#Demand of people
@app.route('/demand', methods=['POST'])
def demand():
    
    #Create initial elevator state (The elevator is suppossed to start in lvl 1)
    temp = Demands.query.first()
    if not temp:
        demand_0 = Demands()
        db.session.add(demand_0)
        db.session.commit()    
    
             
    #Query of resting level (The objective level of last demand)
    rest = Demands.query
   
    demand = Demands(lvl_object = int(request.form['lvl_object']), lvl_current = int(lvl_curr[0]), lvl_rest = str(rest[-1].lvl_object), lvl_date = datetime.now())
    db.session.add(demand)
    db.session.commit()
    init = False
    
    return redirect(url_for('root'))

#Execute program
if __name__ == '__main__':
    #Run app 
    app.run(debug=True)
    

    