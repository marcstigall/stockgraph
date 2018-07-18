from flask import Flask , render_template #import flask

app = Flask(__name__) #instantiate Flask object

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__": #if True the script runs
    app.run(debug=True)
