# https://developer.ing.com/openbanking/get-started

# pasar a pem: openssl x509 -inform pem -in certificate.cer -outform der -out certificate.pem
# paths y nombres de los certificados
rm logs/*.log

certsPath="/home/luis-carrascosa/psd2-certificates/IngDirect/sandboxcerts/psd2"

certSignNameKey="example_eidas_client_signing.key"
certSignNameCer="example_eidas_client_signing.cer"
certSignNameCerPem="example_eidas_client_signing.pem"

certTLSNameKey="example_eidas_client_tls.key"
certTLSNameCer="example_eidas_client_tls.cer"

host="https://api.sandbox.ing.com"

# PSD2
# Es necesario el contenido del cer del eIDAS
eIDASSignCer=`cat $certsPath/$certSignNameCerPem | tr -d '\n'`

# $1: host, $2: httpMethod, $3: reqPath, $4: Accept_contentType, $5: header_contentType, $6: access_token, 
# $7: payload, $8: header_tppRedirectUri, $9: header_psuIpAddress, $10: logFile, $11: eIDASSignCer
source callAPI.sh "$host" "POST" "/oauth2/token" "application/json" "application/x-www-form-urlencoded" "" "grant_type=client_credentials" "" "" "oauth.log" "${eIDASSignCer}"
oAuthResponse="$apiResponse"

echo oAuthResponse: "$oAuthResponse"