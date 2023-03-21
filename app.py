from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging
import pymongo
import pandas as pd
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app=Flask(__name__)

@app.route("/",methods=["GET"])
def homepage():
    return render_template("index.html")
@app.route("/review",methods = ["POST","GET"])
def index():
    if request.method == "POST":
        try:
            item_search=request.form['content'].replace(" ","")    # taken input of item get here.
            # search homepage of product
            flipkart_search="https://www.flipkart.com/search?q="
            search_pagehome=flipkart_search+item_search # url for search page 
            home_page_product=urlopen(search_pagehome)   # open here url
            home_page_html=bs(home_page_product.read(),"html.parser")  # parsed open homepage in html code
            boxes=home_page_html.find_all('div',{"class":"_2kHMtA"})  # taken boxes of product and than taken first product
            box=boxes[0]
            product_url_home=box.a['href']                       # taken link of open first product page
            first_product=flipkart_search+product_url_home        # make url for open first product page
            product_page=urlopen(first_product)                           # opened first product page
            product_page_html=bs(product_page.read(),"html.parser")       # taken first product html code 
            comment_boxes=product_page_html.find_all("div",{"class":"col _2wzgFH"})      #taken all commentboxes
            
            reviews=[]                          #we have taken a blank list for append all values received.
            
            
            # now we put here function of getting all values.
            for i in range(len(comment_boxes)):
                try:
                    rating=comment_boxes[i].text[0]
                    commenthead=comment_boxes[i].div.p.text
                    comment=comment_boxes[i].find("div",{"class":"t-ZTKy"}).div.div.text
                    name=comment_boxes[i].find("p", {"class":"_2sc7ZR _2V5EHH"}).text
                except Exception as e:
                    logging.info(e)

                mydict = {"Product": item_search, "Name": name, "Rating": rating, "CommentHead": commenthead,"Comment": comment}
                reviews.append(mydict)
                    
            logging.info("log my final result".format(reviews))
            
            df = pd.DataFrame(reviews)
            df.to_csv(f"{item_search}.csv",index=False)
            
            return render_template('result.html', reviews=reviews[0:len(reviews)-1])
        except Exception as e:
            logging.info(e)
            print(e,"something went wrong")
    else:
        return render_template("index.html")
            
if __name__ == "__main__":
    app.run(host="0.0.0.0")
            

        
        
        
        
        