import flask
import re
from flask import request, jsonify
import datetime
from decimal import Decimal
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# @app.route('/', methods=['GET'])
# def processpayment():
#     #return not_found(error="not good request")
#     return '''Process Payment Main Page'''

@app.route('/processpayment', methods=['POST'])
#assume data input is formdata
def processpayment():
    ccnum = request.form['ccnum']
    ccnum = ccnum.strip().replace(" ", "")
    cardholder = request.form['cardholder']
    cardholder=cardholder.strip()
    expdate = request.form['expdate']
    expdate=expdate.strip()
    cvv = request.form['cvv']
    cvv=cvv.strip()
    amount = request.form['amount']
    amount=amount.strip()
    print(ccnum+" "+cvv+" "+cardholder+" "+amount+" "+expdate)
    if(ccnum and cardholder and expdate and amount is not None):
        if(is_valid_cardnum(ccnum) and is_valid_cholder_name(cardholder) and is_valid_amount(amount) and is_valid_cvv(cvv) and is_valid_exp_date(expdate)):
            amount=Decimal(re.sub(r'[^\d.]', '', amount))
            exp_date_obj = datetime.datetime.strptime(expdate, '%Y-%m-%d')
            exp_date_indtform = exp_date_obj.date()
            dict={"ccnum":ccnum,"cvv":cvv,"amount":amount,"expdate":exp_date_indtform,"cardholder":cardholder}
            if(amount>=0 and amount<=20):
                response=cheap_payment_gateway(dict)
            elif(amount>20 and amount<=500):
                if(check_expensive_payment_exist()):
                    response = expensive_payment_gateway(dict)
                else:
                    response = cheap_payment_gateway(dict)
            else:
                response=premium_payment_gateway(dict)
            return response
        else:
            return bad_request()
    else:
        return bad_request()
# - Payment is processed: 200 OK
# - The request is invalid: 400 bad request
# - Any error: 500 internal server error
def cheap_payment_gateway(dict):
    print("call cheap payment gateway with prameters " +str(dict))
    print("assign gateway response to varible and return")
    gateway_response = jsonify({"status_id": 200,"status":"success","gate_way_type":"cheap_payment_gateway"})
    #gateway_response=jsonify({"status_id": 400,"status":"bad request","gate_way_type":"cheap_payment_gateway"})
    #gateway_response = jsonify({"status_id": 500,"status_string":"internal server error","gate_way_type":"cheap_payment_gateway"})
    return gateway_response

def check_expensive_payment_exist():
    return True

def expensive_payment_gateway(dict):
    print("call expensive payment gateway with prameters " +str(dict))
    print("assign gateway response to varible and return")
    gateway_response = jsonify({"status_id": 200, "status": "success", "gate_way_type": "expensive_payment_gateway"})
    # gateway_response=jsonify({"status_id": 400,"status":"bad request","gate_way_type":"expensive_payment_gateway"})
    # gateway_response = jsonify({"status_id": 500,"status_string":"internal server error","expensive_way_type":"cheap_payment_gateway"})
    return gateway_response

def premium_payment_gateway(dict):
    for _ in range(3):
        print("call premium payment gateway with prameters " +str(dict))
        print("assign gateway response to varible and return")
        gateway_response = jsonify(
            {"status_id": 200, "status": "success", "gate_way_type": "premium_payment_gateway"})
        # gateway_response=jsonify({"status_id": 400,"status":"bad request","gate_way_type":"premium_payment_gateway"})
        # gateway_response = jsonify({"status_id": 500,"status_string":"internal server error","expensive_way_type":"premium_payment_gateway"})
        x=gateway_response.get_json()
        if(x["status_id"]==200):
            return gateway_response
    return gateway_response


def is_valid_cardnum(ccnum):
    #credit card number validation function using luhn algorithm
    if not ccnum.isnumeric():
        return False
    card_number = list(ccnum.strip())
    # Remove the last digit from the card number
    check_digit = card_number.pop()
    # Reverse the order of the remaining numbers
    card_number.reverse()
    processed_digits = []
    for index, digit in enumerate(card_number):
        if index % 2 == 0:
            doubled_digit = int(digit) * 2
            if doubled_digit > 9:
                doubled_digit = doubled_digit - 9
            processed_digits.append(doubled_digit)
        else:
            processed_digits.append(int(digit))
    total = int(check_digit) + sum(processed_digits)
    if total % 10 == 0:
        return True
    else:
        return False

def is_valid_cholder_name(cardholdername):
    # check for valid chname
    return bool(re.fullmatch('[A-Za-z]{1,25}( [A-Za-z]{2,25}){0,2}?',str(cardholdername)))

def is_valid_cvv(cvv):
    #check for valid cvv
    if cvv is None or cvv is "":
        return True
    return bool(re.fullmatch("^[0-9]{3}$",str(cvv)))


def is_valid_amount(amount):
    #check amount is valid
    try:
        Decimal(re.sub(r'[^\d.]', '', amount))
        return True
    except:
        return False



def is_valid_exp_date(expdate):
    # YYYY-MM-DD
    try:
        exp_date_obj = datetime.datetime.strptime(str(expdate), '%Y-%m-%d')
    except:
        return False
    exp_date_indtform = exp_date_obj.date()
    Todays_date = datetime.datetime.now().date()
    if (exp_date_indtform >= Todays_date):
        return True
    else:
        return False


@app.errorhandler(500)
def not_found():
    #overides default 500 error
    return jsonify([{"status_code":500}])

@app.errorhandler(400)
    #overides default 400 error
def bad_request():
    return jsonify([{"status_code":400}])

# A route to return all of the available entries in our catalog.
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)




app.run()