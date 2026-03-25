# Documentacion de validaciones - API de Productos

## Descripcion general

La API de productos cuenta con un conjunto de validaciones implementadas sobre los endpoints de consulta, creacion, modificacion y eliminacion. Estas validaciones tienen como proposito garantizar la integridad de los datos y proporcionar respuestas claras al usuario cuando una operacion no puede completarse.

Se utiliza `HTTPException` de FastAPI para retornar codigos de estado HTTP apropiados: **400** cuando los datos enviados son invalidos y **404** cuando el recurso solicitado no existe.

---

## Validaciones en consulta (GET)

### 1. El codigo de busqueda debe ser mayor a cero

Cuando el usuario realiza una busqueda de producto por codigo, el sistema verifica que el valor proporcionado sea mayor a cero. Si el codigo es menor o igual a cero, se retorna un error **400 Bad Request** con el mensaje *"El codigo debe ser mayor a cero"*.

**Endpoint:** `GET /productos/{cod}`

```python
@app.get('/productos/{cod}')
def findProduct(cod:int):
    if cod <= 0:
        raise HTTPException(status_code=400, detail="El código debe ser mayor a cero")
```

### 2. Mensaje de error si el producto no existe

Si el usuario busca un producto por codigo o por nombre y este no se encuentra en la lista, el sistema retorna un error **404 Not Found** con un mensaje indicando que el producto no fue encontrado. Esto aplica tanto para la busqueda por codigo (`GET /productos/{cod}`) como para la busqueda por nombre (`GET /productos/?nom=`).

Busqueda por codigo:

```python
@app.get('/productos/{cod}')
def findProduct(cod:int):
    if cod <= 0:
        raise HTTPException(status_code=400, detail="El código debe ser mayor a cero")
    for p in productos:
        if p["codigo"] == cod:
            return p
    raise HTTPException(status_code=404, detail=f"Producto con código {cod} no encontrado")
```

Busqueda por nombre:

```python
@app.get('/productos/')
def findProduct2(nom:str=""):
    for p in productos:
        if p["nombre"] == nom:
            return p
    raise HTTPException(status_code=404, detail=f"Producto '{nom}' no encontrado")
```

---

## Validaciones en creacion (POST)

### 3. Asignacion automatica del codigo consecutivo

Al momento de crear un nuevo producto, el sistema asigna el codigo de manera automatica. Para ello, se obtiene el codigo maximo existente en la lista de productos y se le suma uno. En caso de que la lista se encuentre vacia, el primer codigo asignado sera **1**. El usuario no necesita ni debe enviar el codigo del producto.

**Endpoints:** `POST /productos` y `POST /productos2`

```python
nuevo_codigo = max(p["codigo"] for p in productos) + 1 if productos else 1
nuevo_producto = {
    "codigo": nuevo_codigo,
    "nombre": nombre,
    "valor": valor,
    "existencias": existencias
}
productos.append(nuevo_producto)
return nuevo_producto
```

### 4. El valor y las existencias deben ser mayores a cero

Antes de registrar un nuevo producto, el sistema valida que tanto el valor como las existencias sean estrictamente mayores a cero. Si alguno de estos campos no cumple con la condicion, se retorna un error **400 Bad Request** con el mensaje correspondiente.

```python
@app.post('/productos')
def createProduct(nombre:str, valor:float, existencias:int):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor a cero")
    if existencias <= 0:
        raise HTTPException(status_code=400, detail="Las existencias deben ser mayores a cero")
```

---

## Validaciones en modificacion (PUT)

### 5. Error si el producto no existe

Cuando se intenta modificar un producto cuyo codigo no se encuentra registrado, el sistema retorna un error **404 Not Found** con el mensaje *"Producto con codigo {cod} no encontrado"*.

**Endpoint:** `PUT /producto`

```python
    for prod in productos:
        if prod["codigo"] == cod:
            antes = dict(prod)
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exis
            return {"antes": antes, "después": dict(prod)}
    raise HTTPException(status_code=404, detail=f"Producto con código {cod} no encontrado")
```

### 6. El valor y las existencias deben ser mayores a cero

De manera similar a la creacion, al modificar un producto se valida que el nuevo valor y las nuevas existencias sean mayores a cero. Si no se cumple esta condicion, el sistema rechaza la operacion con un error **400 Bad Request**.

```python
@app.put('/producto')
def updateProduct(
    cod:int,
    nom:str=Body(),
    val:float=Body(),
    exis:int=Body()
    ):
    if val <= 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor a cero")
    if exis <= 0:
        raise HTTPException(status_code=400, detail="Las existencias deben ser mayores a cero")
```

### 7. Mostrar el producto antes y despues de la modificacion

Cuando la modificacion se realiza correctamente, el sistema retorna un objeto con dos campos: `antes` y `despues`. El campo `antes` contiene los datos del producto previos a la modificacion, y el campo `despues` contiene los datos actualizados. Esto permite al usuario verificar los cambios realizados.

```python
            antes = dict(prod)
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exis
            return {"antes": antes, "después": dict(prod)}
```

**Ejemplo de respuesta:**

```json
{
  "antes": {"codigo": 1, "nombre": "Esfero", "valor": 3500, "existencias": 10},
  "después": {"codigo": 1, "nombre": "Boligrafo", "valor": 4000, "existencias": 15}
}
```

---

## Validaciones en eliminacion (DELETE)

### 8. Error si el producto no existe y confirmacion de eliminacion

Si el usuario intenta eliminar un producto cuyo codigo no existe, el sistema retorna un error **404 Not Found**. Cuando el producto si existe y se elimina correctamente, el sistema retorna un objeto con un mensaje de confirmacion junto con los datos del producto eliminado.

**Endpoint:** `DELETE /productos/{cod}`

```python
@app.delete('/productos/{cod}')
def deleteProduct(cod:int):
    for prod in productos:
        if prod["codigo"] == cod:
            productos.remove(prod)
            return {"mensaje": "Producto eliminado", "producto": prod}
    raise HTTPException(status_code=404, detail=f"Producto con código {cod} no encontrado")
```

**Ejemplo de respuesta exitosa:**

```json
{
  "mensaje": "Producto eliminado",
  "producto": {"codigo": 2, "nombre": "Cuaderno", "valor": 5000, "existencias": 25}
}
```
