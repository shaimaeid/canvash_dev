# routes.py
from flask import jsonify, request,  render_template
from app.routes.web import web
from app.models import db, Product 
from app.logger import mylogger
from werkzeug.utils import secure_filename
from flask_login import current_user

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/about')
def about():
    return render_template('pages/about.html')

@web.route('/contact')
def contact():
    return render_template('pages/contact.html')

@web.route('/soon')
def soon():
    return render_template('pages/soon.html')

@web.route('/editor', methods=['GET'])
def get_editor():

    #  return view
    return render_template('image_tool.html') 

# 404 fallback
@web.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404

@web.errorhandler(401)
def page_not_found(e):
    return render_template('pages/401.html'), 401

@web.route('/unauthorized')
def unauthorized_access():
    return render_template('pages/401.html')


@web.route('/editor', methods=['POST'])
def post_editor():
    mylogger.info("accessed")
    file_path = "static/user_files/"
    
    if 'image' in request.files:
        file = request.files['image']
        filename = secure_filename(file.filename)
        mylogger.info(filename)
        # Here you should save the file
        mylogger.info(file_path+filename)
        file.save(file_path+filename)
        return 'File uploaded successfully'

    return 'No file uploaded'

@web.route('/upload_image', methods=['POST'])
def upload_image():
    mylogger.info("accessed")
    file_path = "static/user_files/"
    
    if 'image' in request.files:
        file = request.files['image']
        filename = secure_filename(file.filename)
        mylogger.info(filename)
        # Here you should save the file
        mylogger.info(file_path+filename)
        file.save(file_path+filename)
        return 'File uploaded successfully'

    return 'No file uploaded'



@web.route('/pay', methods=['POST'])
def create_payment():
    # Create and redirect user to PayPal payment approval URL
    pass

@web.route('/payment/success', methods=['GET'])
def payment_success():
    # Handle successful payment
    pass

@web.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    # Handle payment cancellation
    pass
