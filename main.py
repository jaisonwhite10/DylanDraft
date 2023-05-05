from flask import Flask,request,render_template,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import stripe
import os

my_email = os.environ['EMAIL']
password = os.environ['EMAIL_PASSWORD']

stripe.api_key = os.environ['STRIPE_API_KEY']

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

Bootstrap(app)

YOUR_DOMAIN = os.environ['DOMAIN']
# response = request.get('')
ab_product = stripe.Product.retrieve(id=os.environ['AB_PRODUCT'])
ab_product_price_id = ab_product.default_price
bicep_product = stripe.Product.retrieve(id=os.environ['BICEP_PRODUCT'])
bicep_product_price_id = bicep_product.default_price
chest_product = stripe.Product.retrieve(id=os.environ['CHEST_PRODUCT'])
chest_product_price_id = chest_product.default_price

print(ab_product)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services', methods=['GET','POST'])
def services():

    return render_template('services.html',ab_product=ab_product,bicep_product=bicep_product,chest_product=chest_product)

@app.route('/checkout/<prod_id>',methods=['GET','POST'])
def checkout(prod_id):


    return render_template('checkout.html',prod_id=prod_id,ab_product=ab_product,bicep_product=bicep_product,chest_product=chest_product)

@app.route('/create-checkout-session/<prod_id>', methods=['GET','POST'])
def create_checkout_session(prod_id):
    checkout_id = ''
    if prod_id == '1':
        try:
            checkout_session = stripe.checkout.Session.create(
                invoice_creation={"enabled": True},

                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': ab_product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)
        checkout_id = checkout_session.id
        return redirect(checkout_session.url, code=303)

    elif prod_id == '2':
        try:
            checkout_session = stripe.checkout.Session.create(
                invoice_creation={"enabled": True},

                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': chest_product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)

    else:
        try:
            checkout_session = stripe.checkout.Session.create(
                invoice_creation={"enabled": True},

                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': bicep_product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)






@app.route('/success/',methods=['GET','POST'])
def successful_checkout():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    line_items = stripe.checkout.Session.list_line_items(request.args.get('session_id'), limit=5)

    invoice_product = line_items.data[0].price.product
    customer = stripe.Customer.retrieve(session.customer)

    print(session.payment_status)
    if session.payment_status == 'paid':
        message = MIMEMultipart()
        message["From"] = my_email
        message["To"] = customer.email
        message["Subject"] = 'Product'
        body = 'This is your product'
        message.attach(MIMEText(body, "plain"))
        if invoice_product == os.environ['AB_PRODUCT']:
            filename = '../static/files/HA RA SU90,WAITS 33-17-15 H.pdf'
        elif invoice_product == os.environ['BICEP_PRODUCT']:
            filename = '../static/files/HA RA SU90,WAITS 33-17-15 H Plat.pdf'
        else:
            filename = '../static/files/HA RA SU90.pdf'
        with open(filename, "rb") as attachment:
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
        text = message.as_string()
        with smtplib.SMTP(host='smtp.mail.yahoo.com', port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            connection.sendmail(from_addr=my_email, to_addrs=customer.email,
                                msg=text.encode(
                                    'utf-8'))
    print(customer)
    return render_template('success.html')

@app.route('/cancel')
def cancel_checkout():
    return render_template('cancel.html')

@app.route('/contact_me',methods=['GET','POST'])
def contact_me():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        print('true')
        with smtplib.SMTP(host='smtp.mail.yahoo.com', port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            connection.sendmail(from_addr=my_email, to_addrs='udemy184@yahoo.com',
                                msg=f'Subject:{subject}\n\n Name: {name}\n Email: {email}\n Message:{message}'.encode(
                                    'utf-8'))
        flash('Message successfully sent!')
        return redirect(url_for('contact_me'))
    else:
        print('fail')


    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
