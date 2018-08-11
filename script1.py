from flask import Flask , render_template #import flask

app = Flask(__name__) #instantiate Flask object

@app.route("/plot/")
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN



    start=datetime.datetime(2018,7,2)
    end=datetime.datetime(2018,8,9)

    #using the DataReader method to find the stock of Apple from google
    df=data.DataReader(name="AMZN", data_source="yahoo",start=start,end=end)


    date_increase=df.index[df.Close>df.Open]
    date_decrease=df.index[df.Close<df.Open]

    def inc_dec(c,o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)

    p=figure(x_axis_type="datetime", width=1000, height=300, sizing_mode='stretch_both')
    p.title.text="Candlestick Chart"
    #makes the grid lines transparent
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.Status == "Increase"],df.Middle[df.Status=="Increase"],
           hours_12,df.Height[df.Status=="Increase"],fill_color="green",line_color="black")

    p.rect(df.index[df.Status == "Decrease"],df.Middle[df.Status=="Decrease"],
           hours_12,df.Height[df.Status=="Decrease"],fill_color="red",line_color="black")

    #the script and html for the bokeh chart
    script1, div1 = components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    return render_template("plot.html", script1=script1, div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__": #if True the script runs
    app.run(debug=True)
