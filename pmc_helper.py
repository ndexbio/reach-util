__author__ = 'dexter'

import requests

def get_pmc_full_text_xml(pmc_id):
      # Note: this service does not support CORS, but should work from Python
      pmc_id = remove_prefix(pmc_id, "PMC")
      params = {
          'verb': 'GetRecord',
          'identifier' :'oai:pubmedcentral.nih.gov:' + pmc_id,
          'metadataPrefix': 'pmc'
        }
      s = requests.session()
      response = s.get('http://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi', params = params)
      return response.text

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text