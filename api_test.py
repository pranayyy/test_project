import requests
#payload1:tested with differnt types of amount in payload1 all passed
#payload2:tested by making changes in strings and removing non mandatory values
#payload3:testcases need to recive bad request
payload1 = [{'ccnum': '4111111111111111',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '10'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '100'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '1000'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '-000'}]

payload2=[{'ccnum': '4111 11111 1111 111',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '10'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv':'',
           'amount': '1000'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '1000'}]


payload3=[{'ccnum': '4111 11111 1111 101',
           'cardholder': 'pranai reddy somannagari',
           'expdate': '2022-01-13',
           'cvv': '123',
           'amount': '10'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai .reddy somannagari',
           'expdate': '2022-01-13',
           'cvv':'',
           'amount': '1000'},{'ccnum': '4111111111111111',
           'cardholder': 'pranai',
           'expdate': '2022-01-13',
           'cvv': '12a',
           'amount': '1000'}]


def payment_process_check_status_code_equals_200(payload):
    url = "http://127.0.0.1:5000/processpayment"

    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response_json=response.json()
    print(response.text)
    assert response.status_code == 200

def payment_process_check_status_code_equals_400(payload):
    url = "http://127.0.0.1:5000/processpayment"

    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    #print(response.text)
    response_body=response.json()
    assert response_body[0]["status_code"] == 400




# for test_variables in payload2:
#     payment_process_check_status_code_equals_200(test_variables)

for test_variables in payload3:
    payment_process_check_status_code_equals_400(test_variables)
