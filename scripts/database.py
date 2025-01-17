import mysql.connector
from datetime import datetime
import requests
import bcrypt

# Defining parameters for database connection
host = 'localhost'  
database = 'progetto_security'
user = 'root'
password = ''

connessione = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

class Database:
    # Login function used for authenticate user
    def login(username, password):
        if connessione.is_connected():
            try:
                cursor = connessione.cursor()
                query = "SELECT id, password FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                risultato = cursor.fetchone()

                # check if the retrieved data is equal to the input data
                if risultato:
                    user_id, hashed_password = risultato
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        return user_id  
                    else:
                        return False
                else:
                    return False
            except Exception as e:
                print(f">> Database login error: {e}")
                return False
            finally:
                cursor.close()
        else:
            print(">> Error: database connection failed")
            return False

    """
    def hash_existing_passwords():
        if connessione.is_connected():
            try:
                cursor = connessione.cursor()
                cursor.execute("SELECT id, password FROM users")
                utenti = cursor.fetchall()
                for user_id, plain_password in utenti:
                    if not plain_password.startswith('$2b$'):
                        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
                        update_query = "UPDATE users SET password = %s WHERE id = %s"
                        cursor.execute(update_query, (hashed_password.decode('utf-8'), user_id))
                
                connessione.commit()
                print(">> Password updated")
            except Exception as e:
                print(f">> Error during password update: {e}")
            finally:
                cursor.close()

    
    def register(username, password):
        if connessione.is_connected():
            try:
                cursor = connessione.cursor()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, hashed_password.decode('utf-8')))
                connessione.commit()
                print(">> Registration completed")
            except Exception as e:
                print(f">> Database registration error: {e}")
            finally:
                cursor.close()
        else:
            print(">> Error: database connection failed")
    """
    # Function user to check document associeted with a certain user
    def getDocuments(userid):
        if connessione.is_connected():
            try:
                cursor = connessione.cursor()
                query = "SELECT * FROM documents WHERE UserID = %s"
                cursor.execute(query, (userid,))
                risultati = cursor.fetchall()
                return risultati
            except Exception as e:
                print(f">> Database query error: {e}")
                return []
            finally:
                cursor.close()
        else:
            print(">> Error: database connection failed")
            return []

    # Function to upload fragments to docker containers
    def uploadShardToContainers(data_shards_list, document_id):
        server_urls = [
            "http://localhost:5001/upload",
            "http://localhost:5002/upload",
            "http://localhost:5003/upload"
        ]

        try:
            num_container = len(server_urls)
            # cycle to create shard name for each fragment
            for index, data_shard in enumerate(data_shards_list):
                server_url = server_urls[index % num_container]
                shard_name = f"shard_{document_id}_{index}"
                files = {
                    'file': (shard_name, data_shard)  
                }
                data = {
                    'shard_name': shard_name
                }
                response = requests.post(server_url, files=files, data=data)
                if response.status_code == 200:
                    print(f"Shard {shard_name} uploaded successfully to {server_url}")
                else:
                    print(f"Error uploading shard {shard_name} to {server_url}: {response.text}")
        except Exception as e:
            print(f"Error during shard upload: {e}")

    # Retrieve the documentID of a given document
    def getDocumentID(userid, filename):
        if connessione.is_connected():
            try:
                cursor = connessione.cursor()
                query = """
                    SELECT DocumentID
                    FROM documents
                    WHERE UserID = %s AND Filename = %s
                """
                cursor.execute(query, (userid, filename))
                risultato = cursor.fetchone()
                if risultato:
                    return risultato[0]
                else:
                    print(f">> Error: Document '{filename}' not found for user '{userid}'.")
                    return None
            except Exception as e:
                print(f">> Database query error: {e}")
                return None
            finally:
                cursor.close()
        else:
            print(">> Error: database connection failed")
            return None
        
    # Returns the maximum ID among all stored documents
    # Used to assign an ID to a document
    def get_max_id():
        try:
            if connessione.is_connected():
                cursor = connessione.cursor()
                query = "SELECT MAX(DocumentID) AS MaxDocumentID FROM documents;"
                cursor.execute(query)
                result = cursor.fetchone()
                if result[0] is not None:
                    print(f"Max DocumentID is: {result[0]}")
                    return result[0] + 1
                else:
                    print("This is the first file in the table: DocumentID 1\n")
                    return 1
        
        except Exception as e:
            print(f"Error in query: {e}")
            
    # Insert document in the database. If it exists it is overwritten otherwise it is added 
    def insert_documents_from_folder(folder_path, filename, user_id):
        try:
            if connessione.is_connected():
                cursor = connessione.cursor()
                check_query = """
                SELECT DocumentID
                FROM documents 
                WHERE UserID = %s AND filename = %s
                """
                cursor.execute(check_query, (user_id, filename))
                existing_document = cursor.fetchone()

                if existing_document:
                    document_id = existing_document[0]
                    print(f"File '{filename}' already exists. Overwrite DocumentID: {document_id}.")
                    
                    update_query = """
                    UPDATE documents 
                    SET date = %s
                    WHERE DocumentID = %s
                    """
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    cursor.execute(update_query, (current_date, document_id))
                else:
                    print(f"File '{filename}' not found. Creating a new record")
                    
                    insert_query = """
                    INSERT INTO documents (DocumentID, UserID, filename, date)
                    VALUES (%s, %s, %s, %s)
                    """
                    document_id = Database.get_max_id()
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    cursor.execute(insert_query, (document_id, user_id, filename, current_date))

                connessione.commit()
                print(f"File '{filename}' correctly uploaded")

        except Exception as e:
            print(f"Error during upload in database: {e}")
        finally:
            cursor.close()

    # Delete the shards from the containers
    def deleteShardsFromServer(document_id):
        server_urls = [
            "http://localhost:5001/delete",
            "http://localhost:5002/delete",
            "http://localhost:5003/delete"
        ]

        shard_names = [f"shard_{document_id}_{i}" for i in range(3)]  
        for server_url, shard_name in zip(server_urls, shard_names):
            response = requests.post(server_url, data={"shard_prefix": shard_name})
            if response.status_code == 200:
                print(f"Deleted successfully: {shard_name} from {server_url}")
            else:
                print(f"Error deleting {shard_name} from {server_url}: {response.text}")
        