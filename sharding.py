import os
from database import *
 

class Sharding:
    # Split the entire file into 3 shards
    def split(filename, num_container): 
        try:
            if not os.path.exists("./input/" + filename):
                print(f"Error: File '{filename}' not found in './input/' directory.")
                return None

            with open("./input/" + filename, 'rb') as f:
                content = f.read()

            total_size = len(content)
            base_chunk_size = total_size // num_container

            if base_chunk_size == 0:
                print("Error: The file size is too small compared to the number of servers.")
                return None

            shard_list = []
            offset = 0
            for i in range(num_container):
                if i == num_container - 1:
                    chunk = content[offset:]  
                else:
                    chunk = content[offset:offset + base_chunk_size]
                    offset += base_chunk_size

                shard_list.append(chunk)
            
            print(f"File '{filename}' divided into {num_container} fragments.")
            return shard_list

        except Exception as e:
            print(f"Error during file splitting: {e}")
            return None


    # Recompose the retrieved and decrypted fragments
    def recompose_from_container(document_id, decrypted_data_list, output_filename):
        try:
            if not decrypted_data_list:
                print(">> Error: Empty fragment list!")
                return

            output_dir = "./output"
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, 'wb') as output_file:
                for shard in decrypted_data_list:
                    output_file.write(shard)  

            print(f">> File '{output_filename}' recomposed successfully in {output_path}.")
            return output_path

        except Exception as e:
            print(f">> Error during recomposition: {e}")
