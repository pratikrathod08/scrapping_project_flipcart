

# !pip install flask
# !pip install flask_cors
# !pip install requests
# !pip install urllib.request
# !pip install logging
# !pip install pymongo

from  flask import Flask ,request,render_template,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import logging
import pymongo
logging.basicConfig(filename="scrapper.log",level=logging.INFO)

app=Flask(__name__)
@app.route("/")
def homepage():
    return render_template("index.html")


def index():
    if request.method == "POST":
        try:
            custsearch= request.form['content'].replace(" ","")
            flipcart="https://www.flipkart.com/search?q="+custsearch
            flipcart1=ureq(flipcart)
            flipcart_page=flipcart1.read()
            flipcart1.close()
            flipcart_html=bs(flipcart_page,"html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            box = bigboxes[0]
            product="https://www.flipkart.com/search?q="+bigboxes[0].div.div.div.a["href"]
            prodres=requests.get(product)
            prodres.encoding='utf-8'
            prod_html=bs(prodres.text,"html.parser")
            commentboxes=prod_html.find_all("div",{"class":"col _2wzgFH"})

            filename=custsearch+".csv"
            fw=open(filename,"w")
            headers="Product,Customer Name,Ratings,Heading,Comment \n"
            fw.write(headers)
            reviews=[]
            for commentbox in commentboxes:
                try:
                    product_name=prod_html.find_all("span",{"class":"B_NuCI"})[0].text
                except:
                    logging.info("name")
                try:
                    rating=commentbox.div.div.text
                except:
                    rating="no rating"
                    logging.info(rating)
                try:
                    commenthead=commentbox.div.p.text
                except:
                    commenthead="no comment"
                    logging.log(commenthead)
                try:
                    comtag=commentbox.find_all('div',{"class":""})[0].text
                except:
                    comtag="no comments "
                    logging.log(comtag)
                mydict={"Product":custsearch,"Name":product_name,"Rating":rating,"CommentHead":commenthead,"Comment":comtag}
                reviews.append(mydict)
            logging.info("log my final result {}".format(reviews))


            return render_template("result.html",reviews[0:len(review)-1])
        except Exception as e:
            logging.info(e)
            return "something is wrong"
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")

        
        
        
        
        