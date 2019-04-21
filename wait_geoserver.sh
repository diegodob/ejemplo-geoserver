wait_for_url="$1/ows?service=wms&version=1.3.0&request=GetCapabilities"
statusCode=0
echo "Esperando por URL: $wait_for_url"
#while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' '$1/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities' )" != "200" ]]
#while [ "$(curl -s -o /dev/null -w ''%{http_code}'' '$1/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities' )" -eq "200" ]
until [ "$statusCode" -eq "200"  ]
do 
    sleep 5
    statusCode=$(eval 'curl -s -o /dev/null -w "%{http_code}" "$wait_for_url"') 
    echo "Probando URL:  $wait_for_url. Respuesta: $statusCode"
done 
#echo "Esperando 10 segundos a que inicie el geoserver..."
#sleep 10
#echo "Gracias por esperar. Continuando!"
    
