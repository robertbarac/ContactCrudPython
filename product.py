from tkinter import ttk
from tkinter import *
import sqlite3 #conecction module

class Product:

    db_name = 'database.db'
    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')
        
        #Creating a Frame container
        frame = LabelFrame(self.wind, text='Register A New Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name Input
        Label(frame, text='Name: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #Price Input
        Label(frame, text = 'Price').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #Button Add Product
        ttk.Button(frame, text='Save Product', command = lambda:self.add_product()).grid(row=3, columnspan=2, sticky= W + E)

        # Output messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height= 10, columns= 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor= CENTER)
        
        # Buttons 
        ttk.Button(text='DELETE', command=lambda:self.delete_product()).grid(row=5, column=0, sticky= W+ E)
        ttk.Button(text='EDIT', command=lambda: self.edit_product()).grid(row=5, column=1, sticky= W+ E)

        # Filling the row
        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # Filling data
        for row in db_rows:
            #print(row)
            self.tree.insert('', 0, text = row[1], values = row[2])
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0


    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added succesfully!'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
            # print(self.name.get())
            # print(self.price.get())
        else:
            self.message['text'] = 'Product and price are required'
            #print('Name and price is required')

        self.get_products()
    
    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0] # el 0 es para que muestre correctamente 
        except IndexError as e:
            self.message['text'] = 'Please, select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'record {} deleted succesfully'.format(name)
        self.get_products()
    
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select a record to edit'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Product')
        
        # Old Name
        Label(self.edit_wind, text='Old Name: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        # New Name
        Label(self.edit_wind, text='New Name: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #Old Price
        Label(self.edit_wind, text='Old Price').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value= old_price), state='readonly').grid(row=2, column=2)

        #New Price
        Label(self.edit_wind, text='New Price').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        # Update Button
        Button(self.edit_wind, text='Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W + E)
        self.edit_wind.mainloop()


    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated succesfully'.format(name)
        self.get_products()
