from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from datetime import datetime
import pandas as pd
import random
from time import sleep


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

#Dataframe creation
data = pd.DataFrame()

#App routes

#Home
@app.route('/')
def root():

    #Query of table Demands
    demands = Demands.query.all()
    demands2 = []
    date = []
    lvl_current = []
    lvl_rest = []
    lvl_object = []
    id = []
      
    #Build summary of each demand and create dataframe
    for demand in demands:
        
        if demand.id > 1:
            demands2.append(str(demand.lvl_date.strftime("%m/%d/%Y, %H:%M:%S")) + " Elevator resting on "+ str(demand.lvl_rest) +" and demand from level " + str(demand.lvl_current) + " to level " + str(demand.lvl_object)) 
 
        else :
            demands2.append("Initial level is 1")
    
        #list to dataframe
        date.append(demand.lvl_date.strftime("%m/%d/%Y, %H:%M:%S"))
        lvl_current.append(demand.lvl_current)
        lvl_rest.append(demand.lvl_rest)
        lvl_object.append(demand.lvl_object)
        id.append(demand.id)

    #Create
    demands = pd.DataFrame()
    demands['id'] = id
    demands['date'] = date
    demands['resting lvl'] = lvl_rest
    demands['current lvl'] = lvl_current
    demands['target lvl'] = lvl_object

    #Write to csv format
    demands.to_csv('demands.csv', index=False)      
                   
    return render_template('index.html', demands2 = demands2)       


#Demand of people
@app.route('/demand', methods=['POST'])
def demand():
    
    #Number o demands
    n_demands = request.form['demands_number']
    
    #Create initial elevator state (The elevator is suppossed to start in lvl 1)
    temp = Demands.query.first()
    if not temp:
        demand_0 = Demands()
        db.session.add(demand_0)
        db.session.commit()    
         
    for i in range(int(n_demands)):
        
        rest = Demands.query.all()
        
        #Create lvl_current (random number between [1-10])
        lvl_curr = np.random.randint(1, high=11, size=1, dtype=int)
        lvl_current = int(lvl_curr[0])
        
        list = np.array(np.linspace(1,10,10))
        idx = np.where(list == lvl_current)
        
        #Array without lvl_current
        list = np.delete(list,idx[0][0])
        
        #Create lvl_object(different to lvl_current) 
        lvl_object = random.choice(list)
        
        #lvl_rest
        lvl_rest = rest[-1].lvl_object
        
        #Create a random delay
        sleep(random.randint(3,15))
        lvl_date = datetime.now()
        
        demand = Demands(lvl_object = lvl_object, lvl_current = lvl_current, lvl_rest = lvl_rest, lvl_date = lvl_date)
        db.session.add(demand)
        
    
    db.session.commit()
       
    return redirect(url_for('root'))

#Execute program
if __name__ == '__main__':
    #Run app 
    app.run(debug=True)
    

    