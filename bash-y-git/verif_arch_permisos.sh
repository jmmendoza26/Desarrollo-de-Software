# Ingresar como parámetro un nombre de archivo y decir si existe y si lo puedo leer
echo "Buscando $1 ..."

if [[ -f $1 ]]; then
echo "Archivo $1 existe..."
    if [[ -r $1 ]]; then
	echo "El archivo $1 se puede leer"
    else
	echo "El archivo $1 NO se puede leer."
	exit
    fi
else
echo "No existe el archivo $1"
fi
