source oauth_sandbox_2_0.sh
echo oAuthResponse: "$oAuthResponse"

# sleep 10 # espera x segundos

# access_token="PASTE_ACCESSTOKEN_HERE"
access_token=`printf "$oAuthResponse" | python -c "import sys, json; print (json.load(sys.stdin)['access_token'])"`

echo certsPath/certTLSNameCer: "$certsPath/$certTLSNameCer"
echo certsPath/certTLSNameKey: "$certsPath/$certTLSNameKey"
echo signature: "$signature"

# /home/luis-carrascosa/psd2-certificates/IngDirect/sandboxcerts/psd2
# /home/luis-carrascosa/sandboxcerts/example_eidas_client_signing.key
# DO NOT MODIFY BELOW THIS LINE

digest=$(printf "" | openssl dgst -binary -sha256 | openssl base64)
#Host and path
host="api.sandbox.ing.com"
httpMethod="get"
reqPath="/oauth2/authorization-server-url?scope=payments-accounts%3Abalance%3Aview&country_code=nl"

#actual request date
reqDate=`LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT"`

#ref UUID
# reqId=$(uuidgen)
reqId=`uuidgen --time`
echo reqId2: "$reqId"

#signing the request
signingString="(request-target): $httpMethod $reqPath
date: $reqDate
digest: $digest
x-ing-reqid: $reqId"
signature2=$(printf "$signingString" | openssl dgst -sha256 -sign $certsPath/$certSignNameKey -passin "pass:changeit" | openssl base64 -A)
echo signature2: "$signature2"

curl -iv -X GET "https://$host$reqPath" \
-H "Authorization: Bearer ${access_token}" \
-H 'Content-Type: application/json' \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
-H "X-ING-ReqID: ${reqId}" \
-H "Signature: keyId=\"5ca1ab1e-c0ca-c01a-cafe-154deadbea75\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest x-ing-reqid\",signature=\"$signature2\"" \
--cert $certsPath/$certTLSNameCer \
--key $certsPath/$certTLSNameKey
