from MasterServer import app,db

db.init_app(app)
db.create_all()
print(app.url_map)
app.run()