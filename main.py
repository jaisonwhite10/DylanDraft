from flask import Flask,request,render_template,redirect,url_for,flash
from flask_bootstrap import Bootstrap
import smtplib
import stripe
import os

my_email = os.environ['EMAIL']
password = os.environ['EMAIL_PASSWORD']

stripe.api_key = os.environ['STRIPE_API_KEY']

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

Bootstrap(app)

YOUR_DOMAIN = 'http://127.0.0.1:5000'
# response = request.get('')
ab_product = stripe.Product.retrieve(id=os.environ['AB_PRODUCT'])
ab_product_price_id = ab_product.default_price
bicep_product = stripe.Product.retrieve(id=os.environ['BICEP_PRODUCT'])
bicep_product_price_id = bicep_product.default_price
chest_product = stripe.Product.retrieve(id=os.environ['CHEST_PRODUCT'])
chest_product_price_id = chest_product.default_price

# test = stripe.Product.retrieve(params={'metadata':{'product-id':'1'}}) does not work need product id
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


    return render_template('checkout2.html',prod_id=prod_id,ab_product=ab_product,bicep_product=bicep_product,chest_product=chest_product)

@app.route('/create-checkout-session/<prod_id>', methods=['GET','POST'])
def create_checkout_session(prod_id):

    if prod_id == '1':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': ab_product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)

    elif prod_id == '2':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': chest_product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)

    else:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': bicep_product_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)




@app.route('/success')
def successful_checkout():
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
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
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
