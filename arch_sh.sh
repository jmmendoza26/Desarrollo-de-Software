#ls -la *.sh
#find -name "*.sh" -ls
#rwx
#421

#ls -l *.sh | awk '{print $1, $9}'

for file in *.sh; do
  if [ -f "$file" ]; then
    permisos=$(stat -c %A "$file")
    #permisos=$(stat -c %a "$file") muestra en numero
    echo "$file: $permisos"
    
    if ! [ -x "$file" ]; then
    	chmod 755 "$file"
    	permisos=$(stat -c %A "$file")
    	echo "Los permisos cambiaron -> $file: $permisos"
    fi
  fi 
done
