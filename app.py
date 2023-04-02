from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, create_refresh_token
from flask_bcrypt import Bcrypt
import datetime
import jwt
import psycopg2


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60  # seconds
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 3600  # seconds
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def ree():
    return "ree"

    

@app.route('/api/login', methods=['POST'])
def login():
    try:
        conn = psycopg2.connect(database="lasertag", user="postgres", password="psetter", host="localhost", port="5432")
    except Exception as err:
        return f"Error is: {str(err)}, the app failed to connect to the database"
    
    username = request.json.get('username')
    password = request.json.get('password')

    print(username)
    print(password)

    cur = conn.cursor()
    cur.execute('SELECT password FROM users WHERE email = %s', (username,))
    result = cur.fetchone()
    
    if result:
        print("reeeeeeee")
        stored_password = result[0]
        if stored_password == password:
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            print(request.headers)
            conn.close()
            cur.close()
            return jsonify({'status': 'success', 'access_token': access_token, 'refresh_token': refresh_token})
    else:
        conn.close()
        cur.close()
        return jsonify({'status': 'error', 'message': 'Invalid username or password!'})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        conn = psycopg2.connect(database="lasertag", user="postgres", password="psetter", host="localhost", port="5432")
    except Exception as err:
        return f"Error is: {str(err)}, the app failed to connect to the database"
    
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    cur = conn.cursor()
    
    try:
        cur.execute('INSERT INTO users (name, email, password)'
            'VALUES (%s, %s, %s)',
            (username, email, password)
    )
    except:
        print("Your username or email is not unique.")
    conn.commit()
    conn.close()
    cur.close()
    return jsonify({'status': 'success', 'message': 'Account creation successful!'})
    

    

    

     
@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)
    return jsonify({'status': 'success', 'access_token': access_token})

@app.route('/protected', methods=["GET"])
@jwt_required()
def hemmelig():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200

def ServerDbInit():
    # Using the psycopg2 module to connect to postgresql database. The connect inputs are very self-explanatory.
    try:
        conn = psycopg2.connect(database="lasertag", user="postgres", password="psetter", host="localhost", port="5432")
    except:
        return print("Failed to connect to the database")
    
    # cursor() makes it possible to execute SQL code directly with python syntax.
    cur = conn.cursor()

    try:
        # Deletes the users table if it already exists. CASCADES is used here because we're making a many to many relationship between users and games.
        cur.execute('DROP TABLE IF EXISTS users CASCADE;')
        # Making the users table
        cur.execute('CREATE TABLE users(id serial PRIMARY KEY,'
        'name varchar (60) NOT NULL UNIQUE,'
        'email varchar (50) NOT NULL UNIQUE,'
        'password varchar (60) NOT NULL);'
        )
        # Inserting a dummy account into users table
        cur.execute('INSERT INTO users (name, email, password)'
        'VALUES (%s, %s, %s)',
        ('petter', 'petter_1995@hotmail.com', 'password')
        )

        # Deletes the games table if it already exists
        cur.execute('DROP TABLE IF EXISTS games CASCADE;')
        # Creating the games table
        cur.execute('CREATE TABLE games (id serial PRIMARY KEY,'
        'finished boolean NOT NULL,'
        'date_added timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL);'
        )
        # Inserting a dummy game into games table
        cur.execute('INSERT INTO games (finished) VALUES (%s)', ('FALSE',))

        # Deletes the users_games table if it already exists
        cur.execute('DROP TABLE IF EXISTS users_games CASCADE;')

        # Making a users_games table to create a relationship between users and games table.
        # Composite key formed from the primary keys from users and games table.
        # "FOREIGN KEY" command is used to create the many to many relationship between the users and games table.
        cur.execute('CREATE TABLE users_games (user_id int NOT NULL,'
        'game_id int NOT NULL,'
        'points int NOT NULL,'
        'hp int NOT NULL,'
        'PRIMARY KEY (user_id, game_id),'
        'FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE,'
        'FOREIGN KEY (game_id) REFERENCES games(id) ON UPDATE CASCADE);'
        )

        # Get the last inserted user_id and game_id to insert into the relationship table.
        # Also making the points and hp variables
        cur.execute('SELECT id FROM users ORDER BY id DESC LIMIT 1;')
        user_id = cur.fetchone()[0]
        cur.execute('SELECT id FROM games ORDER BY id DESC LIMIT 1;')
        game_id = cur.fetchone()[0]
        points = 0
        hp = 100

        # Putting the user_id, game_id, points and hp attributes into the users_games table
        cur.execute('INSERT INTO users_games (user_id, game_id, points, hp)'
          'VALUES (%s, %s, %s, %s)',
          (user_id, game_id, points, hp)
        )

    except Exception as err:
        return f"Error is: {str(err)}"

    conn.commit()
    conn.close()
    cur.close()
    return print("Initiating the database with dummy inputs successfull")

# Initing the postgresql database method is called here
# uncomment next line, if you wanna initiate the Postgresql database from the Flask backend server

ServerDbInit()

if __name__ == '__main__':
    app.run(debug=True)