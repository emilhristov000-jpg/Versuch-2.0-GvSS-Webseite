from init import app, db,session,redirect, render_template,request, slq
from sqladmin import Admin, ModelView


# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# SQLAdmin View handles all CRUD automatically
class UserAdmin(ModelView, model=User):
    # Customize List/Read View
    column_list = [User.id, User.username, User.email]
    column_searchable_list = [User.username, User.email]
    
    # Secure access using session/role checks
    def is_accessible(self, request) -> bool:
        return session.get('user_role') == 'admin'

    def inaccessible_callback(self, request, name):
        return redirect('/login')

# Bind SQLAdmin to Flask
admin = Admin(app, db.engine)
admin.add_view(UserAdmin)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)