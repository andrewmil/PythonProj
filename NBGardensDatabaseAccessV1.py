# -*- coding: utf-8 -*-

import pymysql
from datetime import *
from pymongo import MongoClient
import pandas
from tkinter import *
from PIL import *


conn = MongoClient()
db = conn.Database1
db1 = pymysql.connect('localhost', 'root', 'password', 'NBGardensV2')


class ProductDetails:
    def getProductName(i):
    #####Gets product name from given ID#####
        products = db.Product.find({"_id": i})
        for doc in products:
            productName = doc["name"]
        return productName   

    def getProductIDList():
        #####Returns a list of the product ID's#####
        cursor = db1.cursor()
        sql = 'SELECT ProductID FROM Product'      
        cursor.execute(sql)
        productIDList = cursor.fetchall() 
        
        productIDListN = []
        j = 0
        for i in productIDList:
            productIDListN.append(productIDList[j][0])
            j += 1
        return productIDListN


class SalespersonDetails:
    def searchSalespeople(search):
        #####Searches salespeople from name#####
        salespeopleIDList = SalespersonDetails.getSalespersonIDList()
        matches = []
        for salesID in salespeopleIDList:
            nameDb = SalespersonDetails.getSalespersonName(salesID)
            if search in nameDb:
                matches.append(salesID)
        return matches

    def getSalespersonIDList():
        cursor = db1.cursor()
        sql = 'SELECT SalespersonID FROM Salesperson'      
        cursor.execute(sql)
        salespersonIDList = cursor.fetchall() 
        
        salespersonIDListN = []
        j = 0
        for i in salespersonIDList:
            salespersonIDListN.append(salespersonIDList[j][0])
            j += 1
        return salespersonIDListN
        
    def getSalespersonName(i):
        cursor = db1.cursor()
        sql = 'SELECT name FROM Salesperson \
        WHERE SalespersonID = ' + str(i)
        cursor.execute(sql)
        name = cursor.fetchall()
        nameStr = name[0][0]
        return nameStr


class CustomerDetails:
    def getCustomerName(i):
        #####Gets customer name from CustomerID in SQL#####
        cursor = db1.cursor()
        sql = 'SELECT fname, lname FROM Customer \
        WHERE CustomerID = ' + str(i)
        cursor.execute(sql)
        name = cursor.fetchall()
        nameStr = name[0][0] + ' ' + name[0][1]
        return nameStr
        
    def getCustomerIDList():
        cursor = db1.cursor()
        sql = 'SELECT CustomerID FROM Customer'      
        cursor.execute(sql)
        customerIDList = cursor.fetchall() 
        
        customerIDListN = []
        j = 0
        for i in customerIDList:
            customerIDListN.append(customerIDList[j][0])
            j += 1
        return customerIDListN

    def searchCustomers(search):
        
        if type(search) is str:
            customerIDList = CustomerDetails.getCustomerIDList()
            matches = []
            for custID in customerIDList:
                nameDb = CustomerDetails.getCustomerName(custID)
                if search in nameDb:
                    matches.append(custID)
        elif type(search) is int:
            matches.append(search)
            print(matches)
        return matches

    def getCustomerEmail(i):
        cursor = db1.cursor()
        sql = 'SELECT email FROM Customer_email \
        WHERE Customer_CustomerID = ' + str(i)
        cursor.execute(sql)
        emaili = cursor.fetchall()
        email = emaili[0][0]
        return email
        
    def getCustomerPhone(i):
        cursor = db1.cursor()
        sql = 'SELECT PhoneNumber FROM Customer_Phone \
        WHERE Customer_CustomerID = ' + str(i)
        cursor.execute(sql)
        phonei = cursor.fetchall()
        phone = phonei[0][0]
        return phone
        
        
class OrderDetails:
    def getOrderCreationDate(i):
        #####Gets the creation date of an order from given ID#####
        cursor = db1.cursor()
        sql = 'SELECT Order_Creation_Date FROM Customer_Order \
        WHERE OrderID = ' + str(i)
        cursor.execute(sql)
        date = cursor.fetchall()
        dateStr = date[0][0]
        return dateStr

    def getOrderSalesperson(i):
        cursor = db1.cursor()
        sql = 'SELECT Salesperson_SalespersonID FROM Customer_Order \
        WHERE OrderID = ' + str(i)
        cursor.execute(sql)
        salesID = cursor.fetchall()
        salesIDInt = salesID[0][0]
        print(salesIDInt)


class Reviews:
    def getAverageProductScore(i, dateFrom, dateBefore, current):
        #####Gets average review score for inputted product from a given date#####
        #####If no date is given ask user for date#####
        if current == 0:
            if dateFrom == 0:
                dateFromi = input("At which date do you want the average orders?:")
                dateFrom = datetime.strptime(dateFromi, '%Y-%m-%d').date()
            if dateBefore == 0:
                dateBeforei = input("At which date do you want the average orders?:")
                dateBefore = datetime.strptime(dateBeforei, '%Y-%m-%d').date()
        
        if current == 1:
            dateFrom   = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            dateBefore = datetime.now().date()
            
        customerOrders = db.Customer_Order.find()
        totalRating  = 0
        numOfReviews = 0
        for document in customerOrders:
            orderID = document["_id"]
            orderDate = OrderDetails.getOrderCreationDate(orderID)
            if (dateBefore > orderDate > dateFrom):
                productsOrdered = document["products"]
                for productOrdered in productsOrdered:
                    productID = productOrdered["Product_id"]
                    if productID == i:
                        rating = productOrdered["Customer_Rating"]
                        totalRating  += rating
                        numOfReviews += 1
        if numOfReviews > 0:
            avRating = totalRating / numOfReviews
        else: avRating = 0
        return avRating
    
    def getProductReviews(i, dateFrom, dateBefore):
        #####Prints all reviews for a given product from a given date#####
        ##### if no date is given ask user for date#####
        if dateFrom == 0:
            dateFromi = input("From which date do you want the reviews?:")
            dateFrom = datetime.strptime(dateFromi, '%Y-%m-%d').date()
        if dateBefore == 0:
            dateBeforei = input("At which date do you want the average orders?:")
            dateBefore = datetime.strptime(dateBeforei, '%Y-%m-%d').date()
            
        reviewList = []
        customerOrders = db.Customer_Order.find()
        for document in customerOrders:
            orderID = document["_id"]
            orderDate = getOrderCreationDate(orderID)
            if (dateBefore > orderDate > dateFrom):
                productsOrdered = document["products"]
                for productOrdered in productsOrdered:
                    productID = productOrdered["Product_id"]
                    if productID == i:
                        review = productOrdered["Customer_Review"]
                        reviewList.append(review)
        return reviewList


class ProductReports:
    def getProductReviewsReport(i):
        #####Genertates a report for a given product including average#####
        #####review score and reviews from a given date               #####
        avScore = Reviews.getAverageProductScore(i)
        reviewsList = Reviews.getProductReviews(i)
        proName = ProductDetails.getProductName(i)
        reviewsString = ""
        for j in reviewsList:
            reviewsString += j + "\n"  
        productReportFile = open(proName + "_Reviews.txt", 'w')
        productReportFile.write(proName + "\n" + "Average reviews score is " \
            + str(avScore) +"\n" + "REVIEWS" + "\n" + reviewsString)

    def plotAverageScore(i, dateFrom):
        #####Plots the average score of a product between until a given date#####
        DataSet = []
        dateFromD   = datetime.strptime(dateFrom, '%Y-%m-%d').date()
        dateBefore = dateFromD        
        for j in range(0,20):
            dateBefore += timedelta(days = 30)
            DataSet.append([Reviews.getAverageProductScore(i, dateFromD, dateBefore, 0), dateBefore])
        df = pandas.DataFrame(data = DataSet, columns = ['Average_Rating', 'Date'])
        pltt = df.plot()
        
        fig = pltt.get_figure()
        fig.savefig("plot{0}".format(i))
        
        return df

ProductReports.plotAverageScore(2, '2015-01-01')

class SalesReport:
    def getSalespersonReport(dateFrom, dateTo):
        #####Returns the top salesperson and totalsold#####
        cursor = db1.cursor()
        sql = 'SELECT name, SUM(quantity * price) AS TotalSold FROM Customer_Line_Order \
            JOIN Customer_Order ON Customer_Order.OrderID = Customer_Line_Order.Customer_Order_OrderID \
            RIGHT JOIN Salesperson ON Customer_Order.Salesperson_SalespersonID = Salesperson.SalespersonID \
            AND Customer_Order.Order_Creation_Date > "' + dateFrom + '" \
            AND Customer_Order.Order_Creation_Date < "' + dateTo + '" \
            GROUP BY Salesperson.name ORDER BY TotalSold DESC;'
        cursor.execute(sql)
        salesReport = cursor.fetchall()
        print(salesReport)
        return salesReport
    
    def getCustomerSpend(i, dateAfter, dateBefore):
        #####Returns customer name and spend between two dates#####
        cursor = db1.cursor()
        sql = 'SELECT SUM(price*quantity) AS TotalSpent FROM Customer_Order, Customer_Line_Order \
            WHERE Customer_Payment_Customer_CustomerID = ' + str(i) \
            + ' AND Customer_Order.Order_Creation_Date > "' + dateAfter + '" \
            AND Customer_Order.Order_Creation_Date < "' + dateBefore + '" \
            AND Customer_Order.OrderID = customer_line_order.Customer_Order_OrderID'
        cursor.execute(sql)
        totalSpend = cursor.fetchall()
        totalSpendInt = totalSpend[0][0]
        if totalSpendInt == None:
            totalSpendInt = 0
        custName = CustomerDetails.getCustomerName(i)
        return [custName, totalSpendInt]
        
    def getTopCustomer(dateAfter, dateBefore):
        #####Returns the customer with highest total sales cost along with the cost#####
        #####Between two given dates                                               #####
        
        customerIDListN = CustomerDetails.getCustomerIDList()
        customerSpending = []
        for customerID in customerIDListN:
            customerSpending.append([SalesReport.getCustomerSpend(customerID, dateAfter, dateBefore)[0], \
                SalesReport.getCustomerSpend(customerID, dateAfter, dateBefore)[1]])
        
        sortedCustomerSpending = sorted(customerSpending, key=lambda customer: customer[1], reverse=True)
        return sortedCustomerSpending[0]
        

class GUIFunctions:
    def initialiseGUI():
        #####initialises frame with product selection#####
        top = Tk()
        
        textFrame = Frame(top, width=40, height= 10)
        textFrame.pack()
        selAreaText = Text(textFrame, width = 55, height = 5)
        selAreaText.pack()
        selAreaText.insert(INSERT, "Select the area you want information from:")
        
        butFrame = Frame(top)
        butFrame.pack(side=BOTTOM)
        
        B1 = Button(butFrame, text = 'Products', command = lambda: GUIFunctions.ProductsGUI.productMenu(top, selAreaText, butFrame, textFrame))
        B2 = Button(butFrame, text = 'Customers', command = lambda: GUIFunctions.CustomerGUI.selectCustomer(top, selAreaText, butFrame, textFrame))
        B3 = Button(butFrame, text = 'Salespeople', command = lambda: GUIFunctions.SalespersonGUI.salesPersonMenu(top, selAreaText, butFrame, textFrame))
        BH = Button(top, text = 'Home', command = lambda: GUIFunctions.goHome(top))
        B1.pack(side=LEFT)
        B2.pack(side=LEFT)
        B3.pack(side=LEFT)
        BH.pack(side=LEFT)
        top.mainloop()
    
    def goHome(top):
        top.destroy()
        GUIFunctions.initialiseGUI()
        
    class ProductsGUI:
        def productMenu(top, sAT, butFrame, textFrame):
            #####Displays products as button options#####
            sAT.destroy()
            butFrame.destroy()
            
            butFrame = Frame(top)
            butFrame.pack()
            selProductText = Text(textFrame, width=50, height=5)
            selProductText.pack(expand=True)
            selProductText.insert(INSERT, "Select a product:")
            
            prodIDList = ProductDetails.getProductIDList()        
            
            buttons = {}
            for prodID in prodIDList:
                name = ProductDetails.getProductName(prodID)
                var = 'B{0}'.format(prodID)
                buttons[var] = Button(butFrame, text=name, width=10, \
                    command = lambda a=prodID: GUIFunctions.ProductsGUI.productInfo(top, selProductText, butFrame, textFrame, a))
                buttons[var].config(width=15, height=1)
                buttons[var].pack(side = LEFT)             
                    
        def productInfo(top, selProductText, butFrame, textFrame, a):
            #####displays product info#####
            selProductText.destroy()
            butFrame.destroy()
            textFrame.destroy()
            
            proName = ProductDetails.getProductName(a)      
            avScore = Reviews.getAverageProductScore(a,0,0,1)
            
            textFrame = Frame(top, width = 10, height = 10)
            textFrame.pack()
            proInfoT = Text(textFrame, width = 30, height = 3)
            proInfoT.pack(expand = True)
            proInfoT.insert(INSERT, proName + "\n" + "Average Score: " + str(avScore))
            
            ProductReports.plotAverageScore(a, '2015-01-01')
            
            img = ImageTk.PhotoImage(Image.open("plot{0}.png".format(a)))
            panel = Label(top, image=img)
            panel.img = img
            panel.pack(side = "bottom", fill = "both", expand = "yes")

    class SalespersonGUI:
        def salesPersonMenu(top, sAT, butFrame, textFrame):
            #####Salesperson options menu#####
            sAT.destroy()
            butFrame.destroy()
            
            selSalespersonText = Text(textFrame)
            selSalespersonText.pack()
            selSalespersonText.insert(INSERT, "Make a Selection:")
                
            butFrame = Frame(top)
            butFrame.pack()        
                
            B1 = Button(butFrame, text = 'Salespeople total sales', \
            command = lambda: GUIFunctions.SalespersonGUI.salespeopleReportOptions(top, selSalespersonText, butFrame, textFrame))
            B2 = Button(butFrame, text = 'Search for salesperson',  \
            command = lambda: GUIFunctions.SalespersonGUI.selectSalesperson(top, selSalespersonText, butFrame, textFrame))
            B1.pack(side=LEFT)
            B2.pack(side=LEFT)
                
        def salespeopleReportOptions(top, sST, butFrame, textFrame):
            
            sST.destroy()
            butFrame.destroy()
            textFrame.destroy()
            top.geometry("500x200")
            
            dateToFrame = Frame(top)            
            dateToFrame.pack(side=BOTTOM)
            dateToEntry = Entry(dateToFrame)
            dateToEntry.pack(side=RIGHT)
            dateToEntry.focus_set()
            
            dateToText = Text(dateToFrame, height=1,width=10)
            dateToText.pack(side=LEFT)
            dateToText.insert(INSERT, "Date until: ")
            
            dateFromFrame = Frame(top)            
            dateFromFrame.pack(side=BOTTOM)
            dateFromEntry = Entry(dateFromFrame)
            dateFromEntry.pack(side=RIGHT)
            
            dateFromText = Text(dateFromFrame, height=1, width=10)
            dateFromText.pack(side=LEFT)
            dateFromText.insert(INSERT, "Date From: ")
                        
            B = Button(top, text="Okay", width=10, \
                command = lambda: GUIFunctions.SalespersonGUI.salespeopleRankings(top, dateFromFrame, dateToFrame, dateFromEntry, dateToEntry, B))
            B.pack(side=BOTTOM)
   
        def salespeopleRankings(top, dateFromFrame, dateToFrame, dateFromEntry, dateToEntry, B):
            #####Displays salesperson rankings byt total sold in £#####
        
            dateFrom = dateFromEntry.get() 
            dateTo = dateToEntry.get()
            B.destroy()
            dateToFrame.destroy()
            dateFromFrame.destroy()

            textFrame = Frame(top)
            textFrame.pack()
            salesReport = SalesReport.getSalespersonReport(dateFrom, dateTo)
            salesReportString = "NAME           TOTAL SOLD\n"
            for sp in salesReport:
                length = len(sp[0])
                gap = ""
                for i in range(0, 15 - length):
                    gap += " "
                salesReportString += sp[0] + gap + "£" + str(sp[1]) +"\n"

            salespersonReportText = Text(textFrame)
            salespersonReportText.pack()
            salespersonReportText.insert(INSERT, salesReportString)

        def selectSalesperson(top, sST, butFrame, textFrame):
            #####Allows user to search for salesperson by text#####
            sST.destroy()
            butFrame.destroy()
        
            selSalespersonText = Text(textFrame)
            selSalespersonText.pack()
            selSalespersonText.insert(INSERT, "Search for a salesperson: ")

            salesSarchEntry = Entry(top)
            salesSarchEntry.pack()
            salesSarchEntry.focus_set()
            
            B = Button(top, text="Okay", width=10, \
                command = lambda: GUIFunctions.SalespersonGUI.returnedSalesperson(top, selSalespersonText, salesSarchEntry, B, textFrame))
            B.pack()

        def returnedSalesperson(top, sST, sSE, B, textFrame):
            ##### returns the salespersons matching previous search#####
            search = sSE.get()
            sST.destroy()
            B.destroy()
            sSE.destroy()
        
            foundList = SalespersonDetails.searchSalespeople(search)
        
            selSalespersonText = Text(textFrame)
            selSalespersonText.pack(side=BOTTOM)
            selSalespersonText.insert(INSERT, "Salespeople found: ")
            
            butFrame = Frame(top)
            butFrame.pack(side=TOP)        
        
            buttons = {}
            for salesID in foundList:
                name = SalespersonDetails.getSalespersonName(salesID)
                var = 'B{0}'.format(salesID)
                buttons[var] = Button(butFrame, text=name, width=10, \
                    command = lambda a=salesID: GUIFunctions.SalespersonGUI.showSalespersonDetails(top, selSalespersonText, butFrame, a, textFrame))
                buttons[var].pack(side=LEFT)
        
        def showSalespersonDetails(top, sST, butFrame, a, textFrame):
            #####Shows salesperson details#####
            sST.destroy()
            butFrame.destroy()
    
            name = SalespersonDetails.getSalespersonName(a)        
        
            salespersonDetails = Text(textFrame)
            salespersonDetails.pack()
            salespersonDetails.insert(INSERT, "SalesPerson name: " + name + "\n" + \
                "Salesperson ID: " + str(a) +"\n")
                
    class CustomerGUI:
        def selectCustomer(top, sAT, butFrame, textFrame):
        #####Allows user to search for customer by name#####
            sAT.destroy()
            butFrame.destroy()       
        
            selCustomerText = Text(textFrame)
            selCustomerText.pack()
            selCustomerText.insert(INSERT, "Search for a customer:")

            custSearchEntry = Entry(top)
            custSearchEntry.pack()
            custSearchEntry.focus_set()
        
            B = Button(top, text="get", width=10, \
                command = lambda: GUIFunctions.CustomerGUI.returnedCustomers(top, selCustomerText, custSearchEntry, B, textFrame))
            B.pack()
        
        def returnedCustomers(top, sCT, custSearchEntry, B, textFrame):
        #####Returns buttons for customers #####
            search = custSearchEntry.get()
            sCT.destroy()
            B.destroy()
            custSearchEntry.destroy()
        
            foundList = CustomerDetails.searchCustomers(search)
            butFrame = Frame(top)
            butFrame.pack()
            buttons = {}
        
            for custID in foundList:
                name = CustomerDetails.getCustomerName(custID)
                var = 'B{0}'.format(custID)
                buttons[var] = Button(butFrame, text=name, width=10, \
                    command = lambda a=custID: GUIFunctions.CustomerGUI.showCustomerDetails(top, butFrame, a, textFrame))
                buttons[var].pack(side=LEFT)
            
        def showCustomerDetails(top, butFrame, a, textFrame):
            #####Presents chosen customers details#####
            butFrame.destroy()
        
            name = CustomerDetails.getCustomerName(a)
            email = CustomerDetails.getCustomerEmail(a)
            phone = CustomerDetails.getCustomerPhone(a)
            totalSpend = SalesReport.getCustomerSpend(a, '2000-01-01', '2016-12-20')[1]
        
            customerDetails = Text(textFrame)
            customerDetails.pack()
            customerDetails.insert(INSERT, "Customer name: " + name + "\n" + \
                "Customer ID: " + str(a) +"\n" + \
                "email: " + email +"\n" + \
                "Phone: " + str(phone) +"\n" \
                "Total Spend: £" + str(totalSpend))
        

GUIFunctions.initialiseGUI()
            
            
            
            

