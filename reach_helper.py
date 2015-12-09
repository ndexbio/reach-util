__author__ = 'dexter'
import requests
import json
from requests_toolbelt import MultipartEncoder


def process_nxml(nxml, outputType):
    # Note: this service does not support CORS, but Python should be ok
    response = requests.post('http://agathon.sista.arizona.edu:8080/odinweb/api/nxml',
                             {'nxml': nxml, 'output': outputType})
    response.raise_for_status()
    if response.status_code == 204:
        return ""
    result = process_reach_json(response.text)
    return result


def process_xml_from_file(filename, outputType):
    fields = {

        'fileUpload': (filename, open(filename, 'rb'), 'application/octet-stream'),
        'filename': filename
    }
    url = 'http://agathon.sista.arizona.edu:8080/odinweb/api/ingestNxml'
    multipart_data = MultipartEncoder(fields=fields)
    headers = {'Content-Type': multipart_data.content_type,
               'Accept': 'application/json',
               'Cache-Control': 'no-cache',
    }
    response = requests.post(url, data=multipart_data, headers=headers)
    response.raise_for_status()
    if response.status_code == 204:
        return ""
    result = process_reach_json(response.text)
    return result

def process_reach_json(json_str):
    json_str = json_str.replace('frame-id','frame_id')
    json_str = json_str.replace('argument-label','argument_label')
    json_str = json_str.replace('object-meta','object_meta')
    json_str = json_str.replace('doc-id','doc_id')
    json_dict = json.loads(json_str)
    return json_dict
