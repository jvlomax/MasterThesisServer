from flask import jsonify, render_template
from MasterServer.utils.exceptions import DatabaseError

from MasterServer import app






from MasterServer.resources.beacons import Beacons_view




def register_api(view, endpoint, url, pk="id", pk_type="int"):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=["GET",])
    app.add_url_rule(url, view_func=view_func, methods=["POST"])
    app.add_url_rule("{0}<{1}:{2}>".format(url, pk_type, pk), view_func=view_func, methods=["GET", "PUT", "DELETE"])


register_api(Beacons_view, "beacons_view", "/beacons/", pk="id", pk_type="path")



@app.route('/')
def hello_world():
    return render_template("index.html")

@app.errorhandler(DatabaseError)
def handle_database_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#if __name__ == '__main__':

  #  print(app.url_map)
  #  app.run(debug=True)
