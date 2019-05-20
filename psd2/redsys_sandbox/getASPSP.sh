# GET {provider}/v2/sva/aspsps
# https://hub-i.redsys.es:16443/api-entrada-xs2a/services/v2/sva/aspsps
# https://apis-i.redsys.es:20443/psd2/xs2a/api-entrada-xs2a/services/BBVA/v1/payments/instant-sepa-credit-transfers

payload="{}"
# ****************************************************
# X-Request-ID
# Identificador único de la operación asignado por el TPP.
# UUID
# ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
# x_request_id=`printf "$oAuthResponse" | python -c "import sys, json; print (json.load(sys.stdin)['access_token'])"`
x_request_id=`python -c "import uuid; print (uuid.uuid4())"`
echo x_request_id: "$x_request_id"

# Digest
# Es contenido si viaja el campo Signature.
# Ver 6.1 Firma para más información.
# Ej: Digest: SHA-256=NzdmZjA4YjY5M2M2NDYyMmVjOWFmMGNmYTZiNTU3MjVmNDI4NTRlMzJkYzE3ZmNmMDE3ZGFmMjhhNTc5OTU3OQ==
payloadDigest=`echo -n "$payload" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest

# Signature
# Firma de la petición por el TPP.
# Ver 6.1 Firma para más información.
# ****************************************************
# 1. keyId: Es una cadena que el HUB puede usar para buscar el componente que necesita para validar la firma.
# Número de serie del certificado del TPP incluido en “TPP-Signature-Certificate”.
# Debe estar formateado como sigue:
# KeyId="SN=XXX,CA= YYYYYYYYYYYYYYYY"
# Donde “XXX” es el número de serie del certificado en codificación hexadecimal y "YYYYYYYYYYYYYYYY" es el "Distinguished Name” completo de la autoridad certificadora.
    # CN=Banco Bilbao Vizcaya Argentaria, S.A.
    # OU=Departamento de informatica
    # O=BBVA
    # L=Bilbao
    # S=Bilbao
    # C=ES
    # OID.2.5.4.97=PSDES-BDE-0182
# keyId=\"SN=01,CA=CN=Banco%20Bilbao%20Vizcaya%20Argentaria%2C%20S.A.,O=BBVA,C=ES,S=Bilbao,L=Bilbao,OU=Departamento%20de%20informatica\",

# 2. Algorithm-ID: Es usado para especificar el algoritmo utilizado para la generación de la firma.
# El algoritmo debe identificar al mismo algoritmo para la firma que el que se presenta en el certificado de la petición.
# Debe identificar SHA-256 o SHA-512.
# algorithm=\"SHA-256\"

# 3. Headers
# Es usado para especificar la lista de cabeceras HTTP incluidas cuando se genera la firma para el mensaje.
# Si se especifica, debe ser una lista entre comillas y en minúscula, separados por un espacio en blanco. Si no se especifica se debe entender que se ha especificado solo un valor. Dicho valor especificado es el atributo “Date” del encabezado de la petición.
# El orden de los atributos es importante y debe ser el mismo que el orden especificado en la lista de cabeceras HTTP especificadas en este campo.
# Los campos a firmar obligatorios son:
# • digest
# • x-request-id
# Condicionalmente, si viajan y son soportados, puede incluir:
# • psu-id
# • psu-corporate-id
# • tpp-redirect-uri
# headers=\"digest x-request-id tpp-redirect-uri\" --> inicio de pago
# headers=\"digest x-request-id\"

# 4. Signature
# El parámetro “signature” debe ir en Base64 SEGÚN RFC 4648.
# El TPP usa el algoritmo y los parámetros de la cabecera a firmar para formar la cacdena a firmar. La cadena a firmar es firmada con la keyId y el algoritmo correspondiente. 
# El contenido debe ir en Base64

# x-request-id digest
               
printf -v signingString "digest: $digest\nx-request-id: $x_request_id"
signature=`printf "$signingString" | openssl dgst -sha256 -sign bbva.pem -passin "pass:changeit" | openssl base64 -A`

echo signingString:"$signingString"
echo signature:"$signature"

# Invocación
curl -X get https://hub-i.redsys.es:16443/api-entrada-xs2a/services/v2/sva/aspsps \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "digest: ${digest}" \
-H "x-request-id: ${reqId}" \
-H "signature keyId=\"SN=01,CA=CN=Banco%20Bilbao%20Vizcaya%20Argentaria%2C%20S.A.,O=BBVA,C=ES,S=Bilbao,L=Bilbao,OU=Departamento%20de%20informatica\",algorithm=\"SHA-256\",headers=\"digest x-request-id\",signature=\"$signature\"" \
-d "${payload}" \
--cert bbva_ttp_2wssl.csr