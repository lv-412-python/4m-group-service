""" app runner """
from groups_service import APP

@APP.route('/')
def hello_world():
    """ root view """
    return 'Hello, World!'

if __name__ == '__main__':
    APP.run(debug=True)
