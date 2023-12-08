from flask import Flask, request, jsonify, make_response

from operators.Hotels import Hotels
from operators.Tatilbudur import Tatilbudur

app = Flask(__name__)


@app.route('/operators', methods=['GET'])
def operator_translator():
    # Requestten gelen url alalım
    url = request.args.get('url')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    adult = request.args.get('adult')
    children = request.args.get('children')
    withPerPerson = request.args.get('withPerPerson')
    currency = request.args.get('currency')
    try:
        if url.find("tatilbudur") != -1:
            response = Tatilbudur(url, checkin, checkout, adult, children, withPerPerson).get_hotel_info()
            return jsonify(response)
        elif url.find("hotels.com") != -1:
            response = Hotels(url, checkin, checkout, adult, children, currency, withPerPerson ).get_hotel_info()
            return jsonify(response)
        else:
            return jsonify({"result": "No operator selected"}, 404)
    except BaseException as e:
        return jsonify({"result": "System Error", "error": e}, 500)


if __name__ == '__main__':
    # Ayağa kaldır
    app.debug = False
    app.run(host="0.0.0.0", port=5011)
