from flask import Flask,render_template ,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import os
from flask_cors import CORS 


app=Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

username = 'root'
password="mortada$348143"
database="ticketsystem"

SQLALCHEMY_DATABASE_URI = f'mysql://{username}:{password}@localhost/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY']='your_secret_key'
# app.config['SESSION_COOKIE_SECURE'] = True


db=SQLAlchemy(app)
Login_Manager=LoginManager(app)

with app.app_context():
    db.Model.metadata.reflect(db.engine)

class Users(UserMixin, db.Model):
    __table__ = db.metadata.tables['users']

    def get_id(self):
        return self.Id


class Response(UserMixin, db.Model):
    __table__ = db.metadata.tables['ticket_response']

class Tickets(UserMixin, db.Model):
    __table__ = db.metadata.tables['tickets']



@Login_Manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/HomePage')
@login_required
def homePage(): 
    return render_template('homepage/HomePage.html')



@app.route('/' , methods=['GET','POST'])
def LoginPage():
    if current_user.is_authenticated:
        if current_user.UserTypeId==1:
            return redirect(url_for('admin_page'))
        elif current_user.UserTypeId==2:
            return redirect(url_for('employee'))
        elif current_user.UserTypeId==3:
            return redirect(url_for('homePage'))
        else:
            return redirect(url_for('homePage'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user = Users.query.filter_by(Username=username).first()
        if user and check_password_hash(user.UserPassword,password):
            login_user(user)
            if current_user.UserTypeId==1:
                return redirect(url_for('admin_page'))
            elif current_user.UserTypeId==2:
                return redirect(url_for('employee'))
            elif current_user.UserTypeId==3:
                return redirect(url_for('homePage'))
            else:
                return redirect(url_for('homePage'))    
    return render_template('logIn/index.html')

@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('LoginPage'))

@app.route('/SignUp', methods=(['GET','POST']))
def SignUpPage():
    if current_user.is_authenticated:
        return redirect(url_for('LoginPage'))
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email = request.form['email']
        birthdate=request.form['birthdate']
        username=request.form['username']
        password=request.form['password']
        new_user=Users(FirstName=firstname,LastName=lastname,Email=email,BirthDate=birthdate,Username=username , UserPassword=generate_password_hash(password),UserTypeId=3)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('LoginPage'))
    return render_template('SignUp/index.html')


@app.route('/EmployeePage')
def employee():
    return render_template('EmployeePage/employee.html')

@app.route('/EmployeeTable')
def employees():
    return render_template('adminPages/Table.html')


@app.route('/AddTicketss')
def addticket():
    return render_template('userpages/AddTicket.html')



@app.route('/Tickets')
def userTickets():
    return render_template('userpages/UserTickets.html')


@app.route('/AddEmployee')
def addemployee_form():
    return render_template('adminpages/AddEmployee.html')


@app.route('/Response')
def response():
    return render_template('employeepage/employee.html')

@app.route('/admin')
def admin_page():
    return render_template('adminPages/admin.html')

@app.route('/AddEmployees' , methods=['GET','POST'])
def add_employees():
    if request.method == 'GET':
        return render_template('adminpages/AddEmployee.html')
    else:
        data=request.form
        FirstName=data.get('fname')
        LastName=data.get('lname')
        Email=data.get('eaddress')
        UserPassword=data.get('password')
        Username=data.get('username')
        BirthDate=data.get('birthdate')
        UserTypeId=2
        departement=data.get('departements')
        IsDeleted=False
        Employee=Users(FirstName=FirstName  , LastName = LastName , Email = Email , UserPassword=generate_password_hash(UserPassword) ,
                        Username = Username , BirthDate = BirthDate,UserTypeId = UserTypeId , Departement = departement , 
                        IsDeleted = IsDeleted)
        db.session.add(Employee)
        db.session.commit()
        return redirect(url_for('addemployee_form'))


@app.route('/AddTicket' , methods=['POST'])
@login_required
def add_tickets():
    user_id=current_user.Id
    From_date=datetime.now()
    data=request.form
    Title=data.get('title')
    Ticket_description=data.get('description')
    category=data.get('categories')
    Ticket = Tickets(Title=Title, Ticket_description=Ticket_description, Category=category, 
                         User_id=user_id, Is_Deleted=False, From_date=From_date)
    
    db.session.add(Ticket)
    db.session.commit()
    return redirect(url_for('userTickets'))


@app.route('/updateTicket', methods=['POST'])
@login_required
def update_ticket():
    ticket_id = request.form.get('ticketId')
    employeeid = request.form.get('employeeId')
    if ticket_id and employeeid:
        ticket = Tickets.query.filter_by(Id=ticket_id).first()
        if ticket:
            ticket.employee_id = employeeid
            db.session.commit()
        else:
            return "Ticket not found or unauthorized", 404
    else:
        return "ticketId and employeeId are required", 400


@app.route('/GetAllEmployees' , methods=['GET'])     
def Get_employees():
    Employees=Users.query.filter_by(UserTypeId=2)
    employees_list=[]
    for employee in Employees:
        employees_list.append({
           'id':employee.Id,
           'FirstName':employee.FirstName,
           'LastName':employee.LastName,
           'Email':employee.Email,
           'Username':employee.Username,
           'BirthDate':employee.BirthDate,
           'Departement':employee.Departement
        })
    return jsonify(employees_list)


@app.route('/EmployeeInfo/<int:Employee_id>' , methods=['POST' , 'GET'])
def emp_info(Employee_id):
    Employee=Users.query.get(Employee_id)
    if request.method=='POST':
        Employee.FirstName=request.form['fname']
        Employee.LastName=request.form['lname']
        Employee.Username=request.form['username']
        Employee.UserPassword=request.form['password']
        Employee.Email=request.form['eaddress']
        Employee.BirthDate=request.form['birthdate']
        Employee.Departement=request.form['departements']
        db.session.commit()
        return redirect(url_for('employees'))
    return render_template('adminPages/EditEmployee.html',Employee=Employee)

@app.route('/GetTickets' , methods=['GET'])
@login_required
def Get_Tickets():
    user_id=current_user.Id
    if current_user.UserTypeId==1:
        tickets = Tickets.query.filter_by(employee_id = None).all()
    else:    
        tickets = Tickets.query.filter_by(User_id=user_id).all()
    tickets_list=[]
    for ticket in tickets:
        tickets_list.append({
        'id':ticket.Id,
        'title':ticket.Title,
        'description':ticket.Ticket_description,
        'category':ticket.Category
        })
    return jsonify(tickets_list)


@app.route('/EmployeeTickets' , methods=['GET'])
def emp_Tickets():
    user_id=current_user.Id
    tickets = Tickets.query.filter(
        Tickets.employee_id == user_id,
        Tickets.Id.notin_(
            db.session.query(Response.TicketId)  
        )
    ).all()    
    tickets_list=[]
    for ticket in tickets:
        tickets_list.append({
        'id':ticket.Id,
        'title':ticket.Title,
        'description':ticket.Ticket_description,
        'category':ticket.Category
        })
    return jsonify(tickets_list)


@app.route('/AddResponse', methods=['POST'])
@login_required
def add_Response():
    employee_id = current_user.Id
    data = request.form
    ticket_id = data.get('ticket_id')
    response = data.get('response')
    moredetails = data.get('moredetails')
    ticket = Tickets.query.filter_by(Id=ticket_id).first()
    if ticket:
        ticket.To_date = datetime.now()
        db.session.commit()
    ticket_response = Response(TicketId=ticket_id, Response=response, MoreDetails=moredetails, EmployeeId=employee_id)
    db.session.add(ticket_response)
    db.session.commit()
    return redirect(url_for('employee'))

@app.route('/GetTicketsWithResponse', methods=['GET'])
@login_required
def Get_Tickets_With_Response():
    user_id = current_user.Id
    if current_user.UserTypeId == 1:
        tickets = Tickets.query.filter_by(employee_id=None).all()
    else:
        tickets = Tickets.query.filter_by(User_id=user_id).all()
    tickets_with_response = []
    for ticket in tickets:
        ticket_data = {
            'id': ticket.Id,
            'title': ticket.Title,
            'description': ticket.Ticket_description,
            'category': ticket.Category,
            'Date': ticket.From_date,
            'To_Date':ticket.To_date
        }
        ticket_response = Response.query.filter_by(TicketId=ticket.Id).first()
        if ticket_response:
            response_data = {
                'response_id': ticket_response.Id,
                'response': ticket_response.Response,
                'moredetails': ticket_response.MoreDetails
            }
            ticket_data['response'] = response_data
        tickets_with_response.append(ticket_data)
    return jsonify(tickets_with_response)

if __name__ == '__main__':
    app.run(debug=True)
        

