# Ejecución del script de oAuth
# ./pis_sandbox.sh PIS-0524
source oauth_sandbox_2_0.sh

access_token=`printf "$oAuthResponse" | python -c "import sys, json; print (json.load(sys.stdin)['access_token'])"`
# echo access_token: "$access_token" 

sandbox_request=`printf "$1" | python data_extractor.py`
echo sandbox_request: "$sandbox_request" 

# ${string//substring/replacement}
# $ VERSION='2.3.3'
# $ echo "${VERSION//.}"

# $ echo "Python is a Programming language" | tr -d 'Pyt'

# http body
payload="$(cut -d'#' -f3 <<<$sandbox_request)"
httpMethod="$(cut -d'#' -f1 <<<$sandbox_request)"
reqPath="$(cut -d'#' -f2 <<<$sandbox_request)"

header_contentType="$(cut -d'#' -f5 <<<$sandbox_request)"
header_psuIpAddress="$(cut -d'#' -f6 <<<$sandbox_request)"
header_tppRedirectUri="$(cut -d'#' -f7 <<<$sandbox_request)"
header_accept="$(cut -d'#' -f4 <<<$sandbox_request)"

# $1: host, $2: httpMethod, $3: reqPath, $4: Accept_contentType, $5: header_contentType, $6: access_token, 
# $7: payload, $8: header_tppRedirectUri, $9: header_psuIpAddress, $10: logFile, $11: eIDASSignCer
source callAPI.sh "$host" "$httpMethod" "$reqPath" "$header_accept" "$header_contentType" "$access_token" "$payload" "$header_tppRedirectUri" "$header_psuIpAddress" "pis.log"
pisResponse="$apiResponse"
echo pisResponse: "$pisResponse"

tppMessages=`printf "$pisResponse" | python -c "import sys, json; print (json.load(sys.stdin)['tppMessages'])"`

if [ "$tppMessages" == '' ]
then
paymentId=`printf "$pisResponse" | python -c "import sys, json; print (json.load(sys.stdin)['paymentId'])"`
transactionStatus=`printf "$pisResponse" | python -c "import sys, json; print (json.load(sys.stdin)['transactionStatus'])"`
scaRedirect=`printf "$pisResponse" | python -c "import sys, json; print (json.load(sys.stdin)['_links']['scaRedirect'])"`
self=`printf "$pisResponse" | python -c "import sys, json; print (json.load(sys.stdin)['_links']['self'])"`
status=`printf "$pisResponse" | python -c "import sys, json; print (json.load(sys.stdin)['_links']['status'])"`

echo transactionStatus: "$transactionStatus"
echo paymentId: "$paymentId"
echo scaRedirect: "$scaRedirect"
echo self: "$self"
echo status: "$status"

# Step 3: Validate payment instruction details (optional)
# Method	GET
# Path	https://api.ing.com/v1/payments/sepa-credit-transfers/79554cb2-901a-4447-a7ca-c84aa5567eec
# Headers	X-Request-ID, Authorization: Bearer [APPLICATION_ACCESS_TOKEN], Signature, Digest, Date, TPP-Redirect-URI, PSU-IP-Address

# $1: host, $2: httpMethod, $3: reqPath, $4: Accept_contentType, $5: header_contentType, $6: access_token, 
# $7: payload, $8: header_tppRedirectUri, $9: header_psuIpAddress, $10: logFile, $11: eIDASSignCer
source callAPI.sh "$host" "GET" "$reqPath/$paymentId" "$header_accept" "$header_contentType" "$access_token" "" \
"$header_tppRedirectUri" "$header_psuIpAddress" "validatePis.log"

validatePisResponse="$apiResponse"
echo validatePisResponse: "$validatePisResponse"

# Step 4: Validate payment status
# Method	GET
# Path	https://api.ing.com/v1/payments/sepa-credit-transfers/79554cb2-901a-4447-a7ca-c84aa5567eec/status
# Headers	X-Request-ID, Authorization: Bearer [APPLICATION_ACCESS_TOKEN], Signature, Digest, Date, TPP-Redirect-URI, PSU-IP-Address

# $1: host, $2: httpMethod, $3: reqPath, $4: Accept_contentType, $5: header_contentType, $6: access_token, 
# $7: payload, $8: header_tppRedirectUri, $9: header_psuIpAddress, $10: logFile, $11: eIDASSignCer
source callAPI.sh "$host" "GET" "$reqPath/$paymentId/status" "$header_accept" "$header_contentType" "$access_token" "" \
"$header_tppRedirectUri" "$header_psuIpAddress" "statusPis.log"

statusPisResponse="$apiResponse"
echo statusPisResponse: "$statusPisResponse"
else
echo tppMessages: "$tppMessages"
fi