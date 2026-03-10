from multiprocessing import Value
from re import X
from turtle import width

from serpapi import GoogleSearch
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
c1,c2=st.columns(2)
c1.image("e-pharmacy.jpg",width=200)
c2.header("Price Comparision Tool")

def compare(med_name):
    params = {
    "engine": "google_shopping",
    "q": med_name,
    "gl": "In",
    "api_key": "d447490215b4426fa31046f6e3794dc00f8480af4b9c0b4be0b4a1ec89aac760"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get("shopping_results",[])
    return shopping_results

st.sidebar.title("Enter Name Of Medicine")
med_name=st.sidebar.text_input("Enter Name Here")
choice=st.sidebar.text_input("Enter numner of options")

option= int(choice) if choice else 1
med_company=[]
med_price=[]

if med_name is not None :
    
    st.sidebar.button("Show Comparision")
    shopping_results=compare(med_name)
    #cleaned_string = shopping_results[0].get('price').replace('₹', '')
    if shopping_results:
        lowest_price = float(shopping_results[0].get('price').replace('₹','').replace(',',''))
    else:
        print("No shopping results found")
        lowest_price = None
    
    #lowest_price = float(shopping_results[0].get('price').replace('₹','').replace(',',''))
    lowest_price_index=0
    for i in range(option):

        st.title(f"Option{i+1}")
        c1,c2,c3=st.columns(3)
        if i<len(shopping_results):
             
             price_str = shopping_results[i].get('price')
             price = float(price_str.replace('₹','').replace(',',''))
             med_company.append(shopping_results[i].get("source"))
             med_price.append(price)
             if price < lowest_price:
                 lowest_price = price
                 lowest_price_index = i
             
             
        

             c1.write("Company :")
             c2.write(shopping_results[i].get("source"))
             c1.write("Title :")
             c2.write(shopping_results[i].get("title"))
             c1.write("Price :")
             c2.write(shopping_results[i].get("price"))
             url=shopping_results[i].get("product_link")

             c1.write("Buy Link :")
             c2.link_button("Link", url)
             c3.image(shopping_results[i].get('thumbnail'),width=150)
             "____________________________________________________________________"

    st.title(f"Best Option")

    c1,c2,c3=st.columns(3)
    if shopping_results:
        c2.write(shopping_results[lowest_price_index].get("source"))
    
        c1.write("Company :")
        c2.write(shopping_results[lowest_price_index].get("source"))
        c1.write("Title :")
        c2.write(shopping_results[lowest_price_index].get("title"))
        c1.write("Price :")
        c2.write(shopping_results[lowest_price_index].get("price"))
        url=shopping_results[lowest_price_index].get("product_link")
        c2.link_button("Buy best price",url)
        c3.image(shopping_results[lowest_price_index].get('thumbnail'),width=150)
    else:
        c2.write("")
st.title("Graph Comparision")
df=pd.DataFrame(med_price,med_company)
st.bar_chart(df)


fig,ax=plt.subplots()
ax.pie(med_price,labels=med_company,shadow=True)
#ax.axis("equal")
st.pyplot(fig)


