# $1: host, $2: httpMethod, $3: reqPath, $4: Accept_contentType, $5: header_contentType, $6: access_token, 
# $7: payload, $8: header_tppRedirectUri, $9: header_psuIpAddress, $10: logFile, $11: eIDASSignCer

# echo payload:"$7"
# echo httpMethod:"$2"
# echo reqPath:"$3"

# debe ser formato 'Wed, 14 Feb 2018 11:15:00 GMT', cuidado que está mal en el portal ING
reqDate=`LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT"`

payloadDigest=`echo -n "$7" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest
httpMethodLower=`echo -n "$2" | tr '[:upper:]' '[:lower:]'`
reqId=`uuidgen --time`

printf -v signingString "(request-target): $httpMethodLower $3\ndate: $reqDate\ndigest: $digest\nx-ing-reqid: $reqId"
signature=`printf "$signingString" | openssl dgst -sha256 -sign $certsPath/$certSignNameKey -passin "pass:changeit" | openssl base64 -A`

echo signingString:"$signingString"

# -i para ver el header https://api.sandbox.ing.com/v1/payments/sepa-credit-transfers

if [ "$6" == '' ]
then
# keyId=\"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa\"
# SN=XXX,CA=YYYYYYYYYYYYYYYY
# Ejemplo de redsys: keyId="SN=9FA1,CA=CN=D-TRUST%20CA%202-1%202015,O=D-Trust%20GmbH,C=DE"
# ING: keyId=\"SN=499602D2\,CA=CN=AppCertificateMeansAPI\,OU=ING\,O=ING\,L=Amsterdam\,ST=Amsterdam\,C=NL\"
apiResponse=$(curl -X "$2" $1$3 \
-H "Accept: ${4}" \
-H "Content-Type: ${5}" \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
-H "X-ING-ReqID: ${reqId}" \
-H "TPP-Signature-Certificate: ${11}: :" \
-H "Authorization: Signature keyId=\"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest x-ing-reqid\",signature=\"$signature\"" \
-d "${7}" \
--trace-ascii logs/${10} \
--cert $certsPath/$certTLSNameCer \
--key $certsPath/$certTLSNameKey
) 
else
# keyId=\"5ca1ab1e-c0ca-c01a-cafe-154deadbea75\" esto lo debería devolver la salida del oAuth, pero en sandbox no lo hace y debe usarse este
apiResponse=$(curl -X "$2" $1$3 \
-H "Accept: ${4}" \
-H "Content-Type: ${5}" \
-H "Authorization: Bearer ${6}" \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
-H "X-ING-ReqID: ${reqId}" \
-H "Signature: keyId=\"5ca1ab1e-c0ca-c01a-cafe-154deadbea75\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest x-ing-reqid\",signature=\"${signature}\"" \
-H "TPP-Redirect-URI: ${8}" \
-H "PSU-IP-Address: ${9}" \
-d "${7}" \
--trace-ascii logs/${10} \
--cert $certsPath/$certTLSNameCer \
--key $certsPath/$certTLSNameKey
) 
fi
