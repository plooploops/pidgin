import json

import flask
import requests


app = flask.Flask(__name__)


#JSON GET endpoint
#@app.route('/json', methods=['GET'])
#def get-json-metadata():
#    data = ...
#    return data


# Endpoint to get core metadata from an object_id.
@app.route('/json/<path:object_id>') # 'path' allows the use of '/' in the id
def get_json_metadata(object_id):
    metadata = get_metadata_dict(object_id)
    return translate_dict_to_json(metadata)


# Translate a dictionary to a JSON string.
def translate_dict_to_json(d):
    json_str = json.dumps(d)
    return json_str


# Create a dictionary containing the metadata for a given object_id.
def get_metadata_dict(object_id):
    response = query_metadata(object_id) # query to peregrine

    # translate the response to a dictionary
    data = response.get_json()['data']
    #file_type = next(iter(data.keys())) # name of first key = file type
    #metadata = data[file_type][0] # get metadata
    metadata = flatten_dict(data)
    #for key, value in metadata.items():
    #    print(key, value)
    return metadata


# Flatten a dictionary, assuming there are no duplicates in the keys.
def flatten_dict(d):
    flat_d = {}
    for k, v in d.items():
        if isinstance(v, list):
            if (v): # check if there is data to read
                # object_id is unique so the list should only contain one item
                flat_d.update(flatten_dict(v[0]))
        else:
            flat_d.update({k:v})
    return flat_d


# Write a query and transmit it to send_query().
def query_metadata(object_id):
    object_id = "f4a34430-9f3d-4f0b-b0eb-c50b0df87062"
    file_type = 'submitted_aligned_reads' # TODO: get file type from object_id
    #query_txt = '{ ' + file_type + """ {
    query_txt = '{ ' + file_type + ' (object_id: "' + object_id + """") {
        core_metadata_collections {
          title description creator contributor coverage
          language publisher rights source subject
        }
        file_name data_format file_size object_id updated_datetime
      }
    }"""
    #print(query_txt)
    data = send_query(query_txt)
    return data


# Send a query to peregrine and return the jsonified response.
def send_query(query_txt):
    query = {'query': query_txt}

    api_url = app.config.get('API_URL')
    if not api_url:
        return flask.jsonify({'error': 'pidgin is not configured with API_URL'}), 500

    #print(flask.request.headers)
    auth = flask.request.headers.get('Authorization')

    output = requests.post(api_url, headers={'Authorization': auth}, json=query).text
    #print(output)

    data = json.loads(output)
    return flask.jsonify(data)
