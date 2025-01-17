from database import *
from login import *
from encryption import *
from sharding import *

num_container= 3
 
print("-- Sharding system --\n")
userid = Login.execute()


while 1: 
    print("\nMenu:")
    print("[0] Exit")
    print("[1] Generate new key")
    print("[2] Splitting file")
    print("[3] Recompose a file")
    choose = str(input("\nChoose option: "))

    if choose == '0':
        print("Exiting...")
        break

    elif choose == '1':
        regenerate = input("Confirm: (y/n): ").lower()
        if regenerate == 'y':
            user_key = Encryption.generate_and_save_key(userid, force_regeneration=True)
        else:
            user_key = Encryption.generate_and_save_key(userid)

    elif choose == '2':
        filename = str(input("\nWrite the file name: "))
        Database.insert_documents_from_folder("./../input", filename, userid)
        fragments = Sharding.split(filename, num_container)
        if fragments:
            document_id = Database.getDocumentID(userid, filename)
            if document_id:
                crypted_list = []
                for fragment in fragments:
                    part = Encryption.encrypt_file_with_user_key(fragment, userid)
                    crypted_list.append(part)

                Database.uploadShardToContainers(crypted_list, document_id)  
                print("\n>> File split and uploaded to containers successfully!")
            else:
                print(f"\n>> Error: DaocumentID not found for the file '{filename}'.")
        else:
            print("\n>> Error: Could not split the file.")

    elif choose == '3':
        print("\n>> Your saved documents")
        documents = Database.getDocuments(userid)
        for document in documents:
            print(document[2]) 

        documentNotFound = True
        while documentNotFound:
            filename = str(input("\nWhat file do you wanna read: "))  
            document_id = Database.getDocumentID(userid, filename)

            if document_id:  
                documentNotFound = False
                print(">> File found, recomposing...")
                decrypted_shards = []
                server_urls = [
                    "http://localhost:5001/download",
                    "http://localhost:5002/download",
                    "http://localhost:5003/download",
                ]

                for shard_index, server_url in enumerate(server_urls):
                    shard_name = f"shard_{document_id}_{shard_index}"
                    try:
                        response = requests.get(server_url, params={"shard_name": shard_name})
                        if response.status_code == 200:  
                            encrypted_data = response.content
                            decrypted_shard = Encryption.decrypt_file_with_user_key(encrypted_data, userid)
                            decrypted_shards.append(decrypted_shard)
                        else:
                            print(f"Error downloading shard {shard_name} from {server_url}: {response.text}")
                    except Exception as e:
                        print(f"Error processing shard {shard_name}: {e}")

                
                if decrypted_shards:
                    Sharding.recompose_from_container(document_id, decrypted_shards, "recomposed_" + filename)
                    print(">> File recomposed and decrypted successfully!")
                    delete = input("Do you want to delete shards? [y/n] ").lower()
                    if delete == 'y': 
                        Database.deleteShardsFromServer(document_id)
                    else : 
                        print("Shards still in containers")     
                else:
                    print(">> Error: No decrypted shards were found.")
