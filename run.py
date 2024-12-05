from app import create_app, db
from app.models.user import User
from app.utils.aes import AESCipher

app = create_app()

if __name__ == '__main__':
   with app.app_context():
    #    db.create_all()
       
    #    # Update admin password dengan enkripsi
    #    admin = User.query.filter_by(role='admin').first()
    #    if admin:
    #        aes = AESCipher()
    #        admin.password = aes.encrypt('your_admin_password')
    #        db.session.commit()
    #        print("Admin password updated successfully")
           
    app.run(debug=True)