# importing redirect
from flask import Flask, redirect, url_for, render_template, request, session
import cv2
from matplotlib.figure import Figure
import numpy as np
import sys
import psycopg2
import time
import uuid

# Initialize the flask application
app = Flask(__name__)
app.secret_key = "super secret key"

HOST = "your_host"
DB = "your_database"
USER_DB = "your_username"
PASSWORD_USER = "your_password"
TABLE_NAME = "table_name"

def take_save_image():

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
        print(len(frame)) # this is a placeholder para representar que aqui deberia ir algun algoritmo de regresion

        k = cv2.waitKey(1)
        print(k)
        if k%256 == 32:
            # ESC pressed
            #print("Escape hit, closing...")
            #break
        #elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            time.sleep(3)
            break
         #   img_counter += 1

    cam.release()

    cv2.destroyAllWindows()

def write_registry_in_DB(dimensions: "json"):

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=HOST,
        database=DB,
        user=USER_DB,
        password=PASSWORD_USER
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Define the SQL query to insert data into the table
    sql = f"INSERT INTO {TABLE_NAME} (ID, PADRE, FIM, LDG[mm], LPG[mm]) VALUES (%s, %s, %s, %s, %s)"

    # Define the data to be inserted



    data = (dimensions['id'], dimensions['padre'], dimensions['fim'], dimensions['ldg'], dimensions['lpg'])

    try:
        # Execute the SQL query with the data
        cursor.execute(sql, data)

        # Commit the transaction to the database
        conn.commit()

        print("Data inserted successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data into PostgreSQL table:", error)
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
def retrieve_fim_padre(value: str, ):
    
    if value:
    
        try: 
            # Establish a connection to the PostgreSQL database
            conn = psycopg2.connect(
                host=HOST,
                database=DB,
                user=USER_DB,
                password=PASSWORD_USER
            )

            # Create a cursor object to interact with the database
            cursor = conn.cursor()

            postgreSQL_select_Query = "select * where id = {value}"

            cursor.execute(postgreSQL_select_Query)

            print("Selecting rows from publisher table using cursor.fetchall")

            record_padre = cursor.fetchall()

            fim = record_padre[0]['fim']
            cursor.close()
            conn.close()
        except Exception as e:
           # By this way we can know about the type of error occurring
            print("The error is: ",e)
            fim = '090909'
    else:
        print("The introduced ID was empty - the fim will be assigned as 090909 but is wrong -- CHECK!!")
        fim = '090909'
    
    return fim

def measure_width(mask):
    ancho = []
    for j in range(mask.shape[0]):
        qq = np.where(mask[j,:]==255)
        if len(qq[0])>0:
            dens = (np.max(qq[0])-np.min(qq[0]))
            ancho.append(np.max(qq[0])-np.min(qq[0]))
        else:
            ancho.append(0)
            
    return ancho

def measure_length(mask):
    length = []
    for j in range(mask.shape[1]):
        qq = np.where(mask[:,j]==255)
        if len(qq[0])>0:
            dens = (np.max(qq[0])-np.min(qq[0]))
            length.append(np.max(qq[0])-np.min(qq[0]))
        else:
            length.append(0)
            
    return length
  
"""
  
# It will load the form template which 
# is in login.html
@app.route('/')
def index():
    return render_template("login.html")
"""  


@app.route('/taking_photo')
def taking_fotos():
    take_save_image()
    
    return "File saved"


@app.route('/measuring_1')
def measuring_method1():

   
    #image = take_image_webcam_opencv()
    #ancho, largo = measure_image(image)
    #load_DB(ancho, largo)

    #camera = cv2.VideoCapture(0)
    #while True:
    #    return_value,image = camera.read()
    #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('image',image)
    #    if cv2.waitKey(1):# & 0xFF == ord('s'):
    #        cv2.imwrite('test2.jpg',image)
    #        break
    #camera.release()
    #cv2.destroyAllWindows()
    
    
    file_name =  "IMG_1485.JPG"
    image = cv2.imread(file_name)
    image = image[900:3500,500:2300,:]
    lower_red = np.array([120,185,190])
    upper_red = np.array([145,235,250])
    mask = cv2.inRange(image, lower_red, upper_red)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    imagen_dilatada = opening #cv2.dilate(mask, kernel, iterations=3)
    num_labels, labels = cv2.connectedComponents(imagen_dilatada)
    x = []
    y = []

    for k in range(num_labels):
        x.append(k)
        y.append(len(np.where(labels==k)[1]))
    y = np.array(y)

    num_pix_block = np.sort(y)[::-1][1]
    index_pieza = x[np.where(y==num_pix_block)[0][0]]
    labels[np.where(labels!=index_pieza)]=0
    labels[np.where(labels==index_pieza)]=255
    
    ancho = measure_width(labels)
    largo = measure_length(labels)
    
    ancho_max = np.max(np.array(ancho))
    largo_max = np.max(np.array(largo))
    
    #print(f"Ancho: {ancho_max}", file=sys.stderr)
    print(f"=========================", file=sys.stderr)
    #print(f"Largo: {largo_max}", file=sys.stderr)
    
    dimensions = {}
    dimensions['ldg'] = largo_max
    dimensions['lpg'] = ancho_max
    dimensions['id'] = 5
    dimensions['padre'] = 3
    dimensions['fim'] = 'abcdefg' 
    print(dimensions, file=sys.stderr)
    
    print(f"=========================", file=sys.stderr)
    
    
    #fig = Figure()
    #ax = fig.subplots()
    #ax.plot(ancho)
    #buf = BytesIO()
    #fig.savefig(buf, format="png")
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")
    

    #fig, ax = subplots.plt(figsize =(10, 7))
    #plt.plot(ancho, '.')
    #plt.show()


    #fig, ax = plt.subplots(figsize =(10, 7))
    #ax.hist(largo, bins = 20)
    #plt.show()
    
    
    

# create a red HSV colour boundary and 
# threshold HSV image
#


    return f"saving into DB - largo = {largo_max} | ancho = {ancho_max}" #, f"<img src='data:image/png;base64,{data}'/>"
  
  
  
# loggnig to the form with method POST or GET
@app.route("/login", methods=["POST", "GET"])
def login():
    
    # if the method is POST and Username is admin then
    # it will redirects to success url.
    
    if request.method == "POST" and request.form["username"] == "admin":
        return render_template("read_id.html")#redirect(url_for("measuring_method1"))
  
    # if the method is GET or username is not admin,
    # then it redirects to index method.
    return redirect(url_for('index'))
    
@app.route("/ask_number_of_pieces", methods=["GET", "POST"])
def ask_number_of_pieces():
    num = request.form["num_pieces"]
    #global num
    list_new_ids = []
    for k in range(int(num)):
        new_id = uuid.uuid4()
        print(new_id)
        list_new_ids.append(new_id)
    print(list_new_ids)
    print("SESSION: ", session)
    return "hasta aca ya llegamos"
        
    

    
@app.route("/readcode", methods=["GET", "POST"])
def readcode():
    #codigo = input("ESCANEE EL CODIGO DE BARRAS: ")
    #fim_padre = retrieve_fim_padre(codigo)
    #global codigo, fim_padre
    #if fim_padre != '090909':
    #    return redirect(url_for("ask_number_of_pieces"))
    #flash("TIRAR MENSAJE DE ERROR")
    print("EL ID es: ", request.form["ID"])
    session['ID'] = request.form["ID"]
    
    return render_template("num_of_pieces.html") #redirect(url_for("ask_number_of_pieces"))
    
    
#@app.route('/found/<email>/<listOfObjects>')
#def found(email, listOfObjects):
#  return render_template("found.html",
#      keys=email, obj=listOfObjects)
           
# It will load the form template which 
# is in login.html
@app.route('/')
def index():
    return render_template("login.html")
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
# 0) LOGIN
# 1) escanear ID de pieza a cortar --> ID PADRE, y traer FIM de DB
# 2) Preguntar cuantos rezagos se generaran
# 3) Registrar cuantos rezagos se generaran
# 4) Generar nuevos ID tantos como numero de nuevos rezagos
# 5) Imprimir stickers con codigos de barra para los nuevos IDs generados
# 6) Indicar al usuario que ID se va a tratar primero y solicitar ubicar al rezago bajo camara -- con longitud de grano paralelo a la sierra
# 7) Cuando el rezago esta en verde (una ventana de la pantalla), y se dispara el lector de codigo de barra: se toma la foto
# 8) Se mide la foto y se muestra un indicador de la medicion (otra ventana en pantalla) 
# 9) Si el indicador es existente (segun python) y si se ve exitoso para el operario, se autoriza (apreta una tecla) la escritura en DB -- Si no, se vuelve a item 6)
# 10) Se recopila la info a escribir: 1) ldg, 2) lpg, 3) id (proviene del punto 4), 4) ID Padre (provine de punto 2), 5) FIM (proviene de punto 2)
# 11) Se genera la tupla de datos y se escribe en la DB
# 12) Se pega el sticker en la pieza medida
# 13) Se quita la pieza de la mesa y se vuelve al punto 6. 
# 14) Cuando no hay mas rezagos para catalogar, se cierra el programa 

