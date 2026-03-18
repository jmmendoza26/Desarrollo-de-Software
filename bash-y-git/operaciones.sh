echo "Parametro 1 -> $1"
echo "Parametro 2 -> $2"

if [ -z "$1" ] || [ -z "$2" ]; then
echo "Faltan parametros"
echo "Uso: $0 <num1> <num2>"
exit 0
fi

if [[ $2 -eq 0 ]]; then
echo "Parámetro 2 es 0"
echo "error: Division por 0"
exit
fi

op=$(($1+$2))
echo "suma: $op"

op=$(($1-$2))
echo "resta: $op"

op=$(($1*$2))
echo "multiplicacion: $op"

op=$(echo "scale=2; $1 / $2" | bc)
echo "division: $op"

op=$(($1%$2))
echo "modulo: $op"
