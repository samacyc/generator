import random 
import numpy as np 
import matplotlib.pyplot as plt
import math
import json

import os
import xlsxwriter 


revenues = np.arange(24)
writed = []

P1 = []
P2 = []
workbook = xlsxwriter.Workbook('stores.xlsx') 


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

def writer (table1 , table2 ,link , link1 , link2 , folder_name , day = 1) : 
    data= []
    
    if not os.path.exists('./{}'.format(folder_name)): 
            os.makedirs('./{}'.format(folder_name))

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
        "Checkout" : table1[i]['Checkout'] 

    }
        )
    global P1 
    global P2
    day_P1 = 0
    day_P2 = 0
    for i in range(len(data)) : 
        day_P1 = day_P1 + data[i]['orders'][0]['orders']
        day_P2 =  day_P2 + data[i]['orders'][1]['orders']
    P1.append(day_P1)
    P2.append(day_P2)

    with open('./{}/{}.json'.format(folder_name, day), 'w') as outfile:
        json.dump({"object" : data}, outfile)
    return data

def indices () : 
    CR = random.uniform(4, 7) 
    checkout = CR * random.uniform(1.5, 2.5) 
    purchase = checkout * random.uniform(1.25, 2) 

    return (CR , checkout , purchase)

def main (revenue  , ordervalue1  , ordervalue2,per2  ,link  , link1  , link2 , folder_name  , d_ays   ) :
    indice = indices()
    rush_hour = 1 
    rush_range = 6 
    percentag_e = random.uniform(40,50)
    die_hour = 20 
    die_range = 5
    tocart = indice[2] 
    checkout = indice[1]
    purchased = indice[0]

    writed = taken(rush_hour , rush_range , revenue ,die_hour, die_range) 
    sale = sales(rush_hour , rush_range , revenue ,die_hour, die_range , writed , percentag_e) 
    chart = orders(ordervalue1,ordervalue2,per2,sale)
    total = total_orders(chart)
    vari = final(total , tocart , checkout , purchased)
    data = writer(vari,chart , link , link1 ,link2 , folder_name , d_ays)
    X = np.arange(24)
    f, ax = plt.subplots(1)
    ax.plot(X,revenues)
    ax.set_ylim(ymin=0)
    plt.savefig('sales.png')
    #plt.show(f)
    
with open('storeconfig.json' ,'rb') as f : 
    data = json.load(f)
    for store in data['stores'] : 
        for i in range(len(store['days'])) : 
            main( store['revenues'][i] ,
             store['ordervalue'][0] , 
             store['ordervalue'][1] ,
              store['percentage'] ,
              store['links'][0] ,store['links'][1] , store['links'][2] , store['store_name'] ,  store['days'][i])
            print(P1 , P2)
            P1 = []
            P2 = []
        worksheet = workbook.add_worksheet(store['store_name'] ) 
        attrb = ( 
            ['ankit', [0, 9, 15, 20, 24, 28, 32, 46]], 
            ['rahul',   [15124, 24015, 18425, 16454, 15416, 21459, 19874, 14789]], 
       
        ) 
        row = 0
        col = 0
        for i in range(len(attrb)) : 
            worksheet.write(row, col, attrb[i][0]) 
            for j in range(len(attrb[i][1])) : 
                worksheet.write(row, col + 1 + j, attrb[i][1][j]) 
            row += 1




workbook.close() 

