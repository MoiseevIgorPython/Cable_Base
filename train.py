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

#n = list(input('jewel: '))
#m = list(input('stone: '))

#count = 0

#for i in set(n):
#    for j in m:
#        if i == j:
#            count+=1

#print(count)


#n = list(input())

#summa = [int(i) for i in n]

#print(sum(summa))



# N = int(input())
# K = [int(input()) for _ in range(N)]

# left = 0
# right = len(K)

# searching = True

# while searching:
#     mid = (left + right) // 2
#     if K[mid] == 1:
#         if K[mid+1] == 0:
#             print(f'! {mid + 2}')
#             searching = False
#         left = mid
#     elif K[mid] == 0:
#         if K[mid-1] == 1:
#             print(f'! {mid}')
#             searching = False
#         right = mid


# n, m = map(int, input().split())

# for _ in range(n):
#     koord = map(int, input().split())[:m]

# print(n, m)


N = int(input())  # колво платформ

H = list(map(int, input().split()))


result = ''

for i in range(len(H)):
    for j in range(len(H)):
        if H[j] > H[i] and j > i and ((i % 2) == (j % 2)):
            result += f'{j-i} '
            break
        elif j == len(H) - 1:
            result += '-1 '

print(result)