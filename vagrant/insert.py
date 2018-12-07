from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')

#hace la conexion entre las tablas de las clases y la base de datos

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

tmpRestaurant = Restaurant(name = "don jediondo prro")
session.add(tmpRestaurant)
session.commit()


first = session.query(Restaurant).first()
 
print(first.name)


restaurants = session.query(Restaurant).all()

for restaurant in restaurants:
    print(restaurant.id,"=>",restaurant.name)



element = session.query(Restaurant).filter_by(name = "restaurante C")

for restaurant in element:
    print(restaurant.name)

#menus = session.query(MenuItem).all()
#for menu in menus:
#    print(menu.id,"=>",menu.name,menu.price)



#actualizar precio enla base de datos
menu = session.query(MenuItem).filter_by(id = 1).one()
print(menu.id,"=>",menu.name,menu.price)
menu.price = "15.99$"
session.add(menu)
session.commit()

toDelete = session.query(Restaurant).filter_by(name = "don jediondo prro").one()
session.delete(toDelete)
session.commit()

restaurants = session.query(Restaurant).all()

for restaurant in restaurants:
    print(restaurant.id,"=>",restaurant.name)


