# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship, declarative_base

# from app.core.db import Base
# from pprint import pprint


# class Customer(Base):
#     name = Column(String(64))
#     orders = relationship('Order', back_populates='customer')


# class Product(Base):
#     name = Column(String(64))
#     price = Column(Integer)
#     order_items = relationship('OrderItem', back_populates='product')


# class Order(Base):
#     customer_id = Column(Integer, ForeignKey('customer.id'))
#     customer = relationship('Customer', back_populates='orders')
#     order_items = relationship('OrderItem', back_populates='order')


# class OrderItem(Base):
#     order_id = Column(Integer, ForeignKey('order.id'))
#     product_id = Column(Integer, ForeignKey('product.id'))
#     quantity = Column(Integer)
#     order = relationship('Order', back_populates='order_items')
#     product = relationship('Product', back_populates='order_items')



# customer1 = Customer(name='Igor')
# customer2 = Customer(name='Petya')

# product1 = Product(name='Potato', price=50)
# product2 = Product(name='Meat', price=100)

# order1 = Order(customer_id=1)
# order2 = Order(customer_id=1)

# order_item1 = OrderItem(order_id=1, product_id=1, quantity=250)
# order_item2 = OrderItem(order_id=0, product_id=0, quantity=350)

# pprint(order_item1)


#import requests

#response = requests.get('http://numbersapi.com/43f')

#if response.status_code == 200:
#    print(response.text)
#else:
#    print(response.status_code)

# from app.core.db import Base
# from app.models.cable import Cable, Isolation
# for i in Base.metadata.tables: 
#     print(i)
