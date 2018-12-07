from http.server import BaseHTTPRequestHandler,HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
#hace la conexion entre las tablas de las clases y la base de datos
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()



def getRestaurants():

        restaurants = session.query(Restaurant).all()
        output = ""
        for restaurant in restaurants:
            output += "<div>"+restaurant.name+"   "+str(restaurant.id)+"</div>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/edit'><input name='id' type='hidden' value="+ str(restaurant.id)+" ><input name='name' type='hidden' value="+ str(restaurant.name)+" ><input value='Edit' type='submit'></form>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/delete'><input name='id' type='hidden' value="+ str(restaurant.id)+" ><input name='name' type='hidden' value="+ str(restaurant.name)+" ><input value='Delete' type='submit'></form>"            

        return output

class webserverHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):

        
        print("se ejecuta",self.path)

        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body>Hello!"
            output += "<a href = \"/restaurants/new\"> new restaurant</a>"
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input value='Submit' type='submit'></form>"
            

            output += getRestaurants()

            output += "</body></html>"
            #el . encode es 
            self.wfile.write(output.encode())
            #print(output)
            return 
        
        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body>Hola!<a href = \"/hello\"> Back to hello</a>"
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input value='Submit' type='submit'></form>"
            output += "</body></html>"

            #el . encode es 
            self.wfile.write(output.encode())
            #print(output)
            return 
        
        
        elif self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body><h1>Restaurantes</h1>"
            output += "<a href = \"/restaurants/new\"> New Restaurand</a>"
            output += getRestaurants()
            output += "</body></html>"

            #el . encode es 
            self.wfile.write(output.encode())
            print(output)
            return 
        
        elif self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body><h1>Nuevo Restaurante</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What would you like me to say?</h2><input name='message' type='text' ><input value='Submit' type='submit'></form>"
            output += "</body></html>"

            #el . encode es 
            self.wfile.write(output.encode())
            #print(output)
            return 

        elif self.path.endswith("/restaurants/edit"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body><h1>No hay elementos por editar</h1>"
            output += "</body></html>"

            self.wfile.write(output.encode())
            #print(output)
            return
        
        

        
        else:
            self.send_error(404,"File not found",self.path)

    def do_POST(self):
        try:

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            
            
            
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            

            if ctype == 'multipart/form-data':

                if self.path.endswith("/restaurants/new"):
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    newRestaurant = Restaurant(name = messagecontent[0].decode())
                    session.add(newRestaurant)
                    session.commit()
                    
                    output=""
                    output += "<html><body><h1>Nuevo Restaurante</h1>"
                    output += "<h1>Se ha creado "+ messagecontent[0].decode()+"</h1>"
                    output += "<a href = \"/hello\"> Back to hello</a>"
                    output += "</body></html>"            
                    self.wfile.write(output.encode())
                
                elif self.path.endswith("/restaurants/edit"):
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')[0].decode()
                    id = fields.get('id')[0].decode()

                    editRestaurant = session.query(Restaurant).filter_by(id = int(id)).one()
                    editRestaurant.name = name
                    session.add(editRestaurant)
                    session.commit()
                    
                    output = ""
                    output += "<html><body><h1>Editar Restaurante</h1>"
                    output += "<h1>nombre es  "+ editRestaurant.name+"</h1>"
                    output += "<h1>id del restaurante es "+ id+"</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/edit'><input name='id' type='hidden' value="+ str(id)+" ><input name='name' type='text' value="" ><input value='Edit' type='submit'></form>"
                    output += "<a href = \"/hello\"> Back to hello</a>"
                    output += "</body></html>"            
                    print("melo2")
                    self.wfile.write(output.encode())
                
                
                elif self.path.endswith("/restaurants/delete"):
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    id = fields.get('id')[0].decode()

                    editRestaurant = session.query(Restaurant).filter_by(id = int(id)).one()
                    session.delete(editRestaurant)
                    session.commit()
                    
                    self.send_header('Location', '/restaurants')
                    


                else:
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Okay, how about this: </h2>"
                    output += "<h1>"+ messagecontent[0].decode()+"</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input value='Submit' type='submit'></form>"
                    output += "<a href = \"/hola\"> Back to hola</a>"
                    output += getRestaurants()
                    output += "</body></html>"
                    self.wfile.write(output.encode())
                
                self.end_headers()
        except:
            pass    


def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print("web server is running in port:",port)
        server.serve_forever()

    #se ejecuta cuando la persona de ctr+c
    except KeyboardInterrupt: 
        print("servidor interrumpido, detniendo procesos .....")
        server.socket.close()
if __name__ == '__main__':
    main()


