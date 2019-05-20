import json, os, sys #, argparse

# parseador de argumentos de entrada
# parser = argparse.ArgumentParser()
# parser.add_argument("path", help="path donde está el txt con las request")
# args = parser.parse_args()
# print(args.path)

# dataFile = os.getcwd() + '/sandbox_data.txt' # working dir
dataFile = os.path.dirname(os.path.abspath(__file__)) + '/sandbox_data.txt'

input = sys.stdin.readline()

sandboxRequests = {}

with open(dataFile) as fh:
    for line in fh:
        key, value = line.strip().split(':', 1)
        sandboxRequests[key] = json.loads(value.strip())

# sandboxRequests = json.dumps(sandboxRequests, indent=2, sort_keys=True)
# sandboxRequests = json.loads(sandboxRequests)

# print(type(sandboxRequests['PIS-0524']['header']))
# print(sandboxRequests['PIS-0524']['header'])

method = json.dumps(sandboxRequests[input]['Method']).replace("\"", "")
path = json.dumps(sandboxRequests[input]['Path']).replace("\"", "")
body = json.dumps(sandboxRequests[input]['body'])

# "header": {"Accept": "application/json", "Content-Type": "application/json", "PSU-IP-Address": "81.24.160.0", "TPP-Redirect-URI": "https://example.com/redirect"}
header_accept = json.dumps(sandboxRequests[input]['header']['Accept']).replace("\"", "")
header_contentType = json.dumps(sandboxRequests[input]['header']['Content-Type']).replace("\"", "")
header_psuIpAddress = json.dumps(sandboxRequests[input]['header']['PSU-IP-Address']).replace("\"", "")
header_tppRedirectUri = json.dumps(sandboxRequests[input]['header']['TPP-Redirect-URI']).replace("\"", "")

print(method + "#" + path + "#" + body + "#" + header_accept + "#" + header_contentType + "#" + header_psuIpAddress + "#" + header_tppRedirectUri)
