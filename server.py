from flask import Flask, request, Response
import os

app = Flask(__name__)

# Endpoint/upload, POST method: this function enables to upload fragment on a container
@app.route('/upload', methods=['POST'])
def upload_fragment():
    fragment = request.files['file']
    shard_name = request.form.get('shard_name', 'shard')
    save_path = os.path.join('/app/data', shard_name)

    try:
        fragment.save(save_path)
        return f"Shard {shard_name} saved successfully at {save_path}", 200
    except Exception as e:
        return f"Error saving shard: {e}", 500
    
# Endpoint/download, GET method: enable to download fragment from a container
@app.route('/download', methods=['GET'])
def download_fragment():
    shard_name = request.args.get('shard_name')
    file_path = os.path.join('/app/data', shard_name)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
            return Response(
                file_content,
                mimetype='application/octet-stream',
                headers={
                    'Content-Disposition': f'attachment; filename={shard_name}'
                }
            )
        except Exception as e:
            return f"Error reading shard: {e}", 500
    else:
        return f"Shard {shard_name} not found.", 404


# Endpoint/delete, POST method: enable to delete a shard with a certain prefix
@app.route('/delete', methods=['POST'])
def delete_shards():
    shard_prefix = request.form.get('shard_prefix')
    data_path = '/app/data'

    try:
        deleted_files = []
        for filename in os.listdir(data_path):
            if filename.startswith(shard_prefix):
                file_path = os.path.join(data_path, filename)
                os.remove(file_path)
                deleted_files.append(filename)

        if deleted_files:
            return f"Deleted files: {', '.join(deleted_files)}", 200
        else:
            return "No files matched the prefix.", 404
    except Exception as e:
        return f"Error deleting files: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
