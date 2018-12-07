from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')

#hace la conexion entre las tablas de las clases y la base de datos

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

"""
#para almacenar en la base de datos se realiza
session.add(myFirstRestaurant)
#para añadir a la base de datos
session.commit()
#para guardar la base de datos
"""



a = ["restaurante A","restaurante B","restaurante C","restaurante D","restaurante E","restaurante F","restaurante G"]
b = ["carne", "pollo", "hawaiana"]

for restaurante in a:
    myFirstRestaurant = Restaurant(name = restaurante)
    session.add(myFirstRestaurant)
    for pizza in b:
        cheesepizza = MenuItem(name = pizza, description = "pizza de peperoni", course = "Entreada", price = "8,99$",restaurant = myFirstRestaurant )
        session.add(cheesepizza)


session.commit()


print("poblacion exitosa prro")


