import random 
import numpy as np 
import matplotlib.pyplot as plt
import math
import json
from PIL import Image 
from tkinter import *
from tkinter import ttk


root = Tk()
root.geometry('1080x1080')
root.title('generator')

revenues = np.arange(24)
writed = []



def sales (hour , rang_e , revenue ,die_hour , die , indice , per) : 
    rush_period_revenue = revenue*(per/100)
    period = np.arange(rang_e)
    k = len(period)
    for i in range(len(period)) : 
        if (i != len(period) -1) : 
            period[i] = random.uniform(((rush_period_revenue*(1-0.1))/k) ,((rush_period_revenue*(1+0.1))/k))
            rush_period_revenue= rush_period_revenue - period[i] 
            k = k -1
        else :
            period[i] = rush_period_revenue
    revenues[hour-1 : hour+rang_e-1 ] = period
    death_period_revenue = revenue*0.05
    death_period = np.arange(die)
    k = len(death_period)
    for i in range(len(death_period)) : 
        if (i != len(death_period) -1) : 
            death_period[i] = random.uniform(((death_period_revenue*(1-0.5))/k) ,((death_period_revenue*(1+0.5))/k))
            death_period_revenue= death_period_revenue - death_period[i] 
            k = k -1
        else :
            death_period[i] = death_period_revenue
    revenues[die_hour -1: die + die_hour -1] = death_period
    rest_period_revenue = revenue*(1 -0.05 -per/100 )
    rest_period = np.arange(24-rang_e-die)
    k = len(rest_period)
    for i in range(len(rest_period)) : 
        if (i != len(rest_period) -1) : 
            rest_period[i] = random.uniform(((rest_period_revenue*(1-0.3))/k) ,((rest_period_revenue*(1+0.3))/k))
            rest_period_revenue= rest_period_revenue - rest_period[i] 
            k = k -1
        else :
            rest_period[i] = rest_period_revenue

    l = 0
    for i in range(24) : 
        if (i in indice) : 
            continue
        else : 
            revenues[i] = rest_period[l]
            l = l +1
    return revenues
def taken (hour , rang_e , revenue , die_hour , die) : 

        for i in range(hour -1 , rang_e + hour-1 ) : 
            writed.append(i)
        for i in range(die_hour -1 , die + die_hour -1 ) : 
            writed.append(i)
        return writed

def orders (order_value1 , order_value2 , percentage , sale) :  
    order_chart = [] 
    percentage = percentage/100
    for numbers in sale : 
        product2 = round(numbers*percentage/order_value2)
        product1 = round(numbers*(1-percentage)/order_value1)
        order_chart.append({
            "product1" : product1, 
            "product2" : product2
        })
    return order_chart

def total_orders(chart) : 
    S = np.arange(24)
    for i in range(len(chart)) :
        S[i] = 0
        S[i] = chart[i]['product1'] +S[i]
        S[i] = chart[i]['product2'] +S[i]
    return S
def final(table , add_to_cart_per , check_out_per , purchase_per ) :
    visitors = []
    addtocart =[] 
    checkout =[] 
    for order in table : 
        visitor = round(order/(purchase_per/100))
        ckout = visitor*(check_out_per/100) - order
        cart = visitor*(add_to_cart_per/100) - ckout - order
        visitor = visitor - order - cart - ckout
        visitors.append(math.ceil(visitor))
        addtocart.append(math.ceil(cart))
        checkout.append(math.ceil(ckout))
    
    data = []
    for i in range(len(visitors)) : 
        data.append({
            'visitors' : visitors[i],
            'toCart' : addtocart[i] , 
            'Checkout' : checkout[i]
        })
    
    return data

def writer (table1 , table2 ,link , link1 , link2 , day) : 
    data= []
    for i in range(len(table1)) : 
        data.append(
             {
        "link" : link,
        "orders" : [
            {"link" :link1,
            "orders" : table2[i]['product1']
            },
            {"link" :link2 ,
                 "orders":table2[i]['product2']}],
        "visitors" : table1[i]['visitors'] ,
        "toCart" :table1[i]['toCart'] ,
        "Checkout" : table1[i]['Checkout'] ,
        'day' : '*******************{}'.format(day)

    }
        )
   
    return data


def main (rush_hour , rush_range , revenue , percentag_e ,die_hour, die_range , ordervalue1 , ordervalue2,per2,tocart,checkout,purchased ,link , link1 , link2 ) :
    data = []
    k = 7
    revenue_per_day = []
    sales_week = []
    each_day =  []

    for i in range(7) : 
        if (i != 7) : 
            revenue_per_day.append(random.uniform(((revenue*(1-0.5))/k) ,((revenue*(1+0.5))/k)))
            revenue= revenue - revenue_per_day[i] 
            k = k -1
        else :
            revenue_per_day.append(revenue)
    for i in range(7) : 
        writed = taken(rush_hour , rush_range , revenue_per_day[i] ,die_hour, die_range) 
        sale = sales(rush_hour , rush_range , revenue_per_day[i] ,die_hour, die_range , writed , percentag_e) 
        chart = orders(ordervalue1,ordervalue2,per2,sale)
        total = total_orders(chart)
        vari = final(total , tocart , checkout , purchased)
        data = writer(vari,chart , link , link1 ,link2 , i)
        for j in range (len(sale)) : 
            sales_week.append(sale[j])
            each_day.append(data[j])
        print('*******************************')
    X = np.arange(7)
    print(len(sales_week))
    print(len(each_day))
    print(len(revenue_per_day))
    with open('./config_week.json', 'w') as outfile:
        json.dump({"object" : each_day}, outfile)
    f, ax = plt.subplots(1)
    ax.plot(X,revenue_per_day)
    ax.set_ylim(ymin=0)
    plt.savefig('sales.png')
    plt.show(f)
    
def get_var() :
        main(int(entry1.get()) , int(entry2.get()),float(entry3.get()),float(entry4.get()),int(entry5.get()),int(entry6.get()),float(entry7.get()),float(entry8.get()),float(entry9.get()),float(entry10.get()),float(entry11.get()),float(entry12.get()) ,entry13.get(),entry14.get(),entry15.get()) 
        
T = ttk.Label(root, text="Explode")
T.pack()
entry1 = ttk.Entry(root, width=40) 
entry1.pack()
T = ttk.Label(root, text="Explode Range")
T.pack()
entry2 = ttk.Entry(root, width=40) 
entry2.pack()
T = ttk.Label(root, text="Revenue")
T.pack()
entry3 = ttk.Entry(root, width=40) 
entry3.pack()
T = ttk.Label(root, text="Explode Percentage")
T.pack()
entry4 = ttk.Entry(root, width=40) 
entry4.pack()
T = ttk.Label(root, text="Shrink")
T.pack()
entry5 = ttk.Entry(root, width=40) 
entry5.pack()
T = ttk.Label(root, text="Shrink Range")
T.pack()
entry6 = ttk.Entry(root, width=40) 
entry6.pack()
T = ttk.Label(root, text="Price1")
T.pack()
entry7 = ttk.Entry(root, width=40) 
entry7.pack()
T = ttk.Label(root, text="Price2")
T.pack()
entry8 = ttk.Entry(root, width=40) 
entry8.pack()
T = ttk.Label(root, text="Product2 Percentage")
T.pack()
entry9 = ttk.Entry(root, width=40) 
entry9.pack()
T = ttk.Label(root, text="Add To Cat")
T.pack()
entry10 = ttk.Entry(root, width=40) 
entry10.pack()
T = ttk.Label(root, text="Checkout")
T.pack()
entry11 = ttk.Entry(root, width=40) 
entry11.pack()
T = ttk.Label(root, text="Purchase")
T.pack()
entry12 = ttk.Entry(root, width=40) 
entry12.pack()
T = ttk.Label(root, text="Link")
T.pack()
entry13 = ttk.Entry(root, width=40) 
entry13.pack()
T = ttk.Label(root, text="Product1 Link")
T.pack()
entry14 = ttk.Entry(root, width=40) 
entry14.pack()
T = ttk.Label(root, text="Product7 Link")
T.pack()
entry15 = ttk.Entry(root, width=40) 
entry15.pack()

btn = ttk.Button(root , text ='generate' , command = get_var).pack()



root.mainloop()

   
