import json
import logging
from datetime import datetime

from flask import Flask, Response, request

app = Flask(__name__)


def get_response(iin: int = 0, is_request_data=False):
    try:
        if is_request_data:
            iin = int(json.loads(request.data.decode()).get("iin"))

        iin_date = int(iin / 1000000)
        if not 100000 < iin_date < 999999:
            raise Exception("Invalid IIN")

        # I do not know the correct way to get 'birth-year' of the Person from IIN
        year = int((iin_date / 10000) % 100)
        year = (year + 2000) if datetime.now().year % 100 >= year else (year + 1900)
        date = datetime(day=iin_date % 100, month=int((iin_date / 100) % 100), year=year)

        if date > datetime.now():
            date = datetime(day=iin_date % 100, month=int((iin_date / 100) % 100),
                            year=int((iin_date / 10000) % 100) + 1900)

        print(f"{iin} {date.date()}")
        result = datetime.now().year - date.year
        status = 201 if is_request_data else 200
        response = Response(json.dumps({"iin": iin, "age": result - 1}), status=status, mimetype='application/json')
        if datetime.now().year > date.year:
            return response
        elif datetime.now().month > date.month:
            return response
        elif datetime.now().day > date.day:
            return response

        return Response(json.dumps({"iin": iin, "age": result}), status=status, mimetype='application/json')

    except BaseException as exception:
        logging.error(exception)
        status = 400 if is_request_data else 404
        return Response(status=status, mimetype='application/json')


@app.route('/people/', methods=('POST',))
def person():
    return get_response(is_request_data=True)


@app.route('/people/<int:iin>/', methods=('GET',))
def person2(iin):
    return get_response(iin)


if __name__ == '__main__':
    app.run()
