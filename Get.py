from flask import Flask, request, jsonify

app = Flask(__name__)

# "Base de datos" en memoria. Es una lista de diccionarios.
# Comenzamos con algunos datos de ejemplo más "llenos".
items_db = [
    {"id": 1, "name": "Laptop Modelo X", "description": "Potente laptop para trabajo y juegos, 16GB RAM, SSD 512GB."},
    {"id": 2, "name": "Mouse Inalámbrico Ergonómico", "description": "Mouse con diseño ergonómico para mayor comodidad, conexión Bluetooth."},
    {"id": 3, "name": "Teclado Mecánico RGB", "description": "Teclado con switches mecánicos, retroiluminación RGB personalizable."},
    {"id": 4, "name": "Monitor Curvo 27 pulgadas", "description": "Monitor Full HD curvo para una experiencia visual inmersiva."},
    {"id": 5, "name": "ADRIAN ES GAY", "description": "CHUPA MONDA POR DINERO"}
]
# Para generar IDs únicos para nuevos items.
# Se ajusta al último ID de la lista de ejemplo + 1.
next_item_id = 5

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API de Items. Accede a /items para ver los items."})

# Rutas para el recurso "items"
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    global next_item_id # Necesitamos indicar que vamos a modificar la variable global

    if request.method == 'GET':
        # Devolver todos los items de nuestra "base de datos"
        return jsonify(items_db)
    
    elif request.method == 'POST':
        # Crear un nuevo item
        new_item_data = request.json # Los datos vienen en el cuerpo de la solicitud como JSON
        
        # Validación simple: el 'name' es requerido
        if not new_item_data or 'name' not in new_item_data or not new_item_data['name'].strip():
            return jsonify({"error": "Faltan datos o el campo 'name' es requerido y no puede estar vacío"}), 400 # Bad Request

        new_item = {
            "id": next_item_id, # Asignamos el ID automáticamente
            "name": new_item_data.get("name"),
            "description": new_item_data.get("description", "") # Descripción es opcional, por defecto cadena vacía
        }
        items_db.append(new_item) # Agregamos el nuevo item a nuestra lista
        next_item_id += 1 # Incrementamos el contador para el próximo ID
        return jsonify({"message": "Item creado exitosamente", "item": new_item}), 201 # 201 Created

@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_specific_item(item_id):
    # Buscar el item en nuestra "base de datos" por su ID
    item_found = None
    for item in items_db:
        if item["id"] == item_id:
            item_found = item
            break

    # Si el item no se encuentra, devolver un error 404
    if not item_found:
        return jsonify({"error": f"Item con ID {item_id} no encontrado"}), 404 # Not Found

    if request.method == 'GET':
        # Devolver los detalles del item encontrado
        return jsonify(item_found)
    
    elif request.method == 'PUT':
        # Actualizar un item existente
        updated_data = request.json # Los datos para actualizar vienen en el cuerpo JSON
        if not updated_data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400 # Bad Request

        # Actualizar los campos permitidos. Si 'name' viene vacío, se podría añadir validación.
        if 'name' in updated_data and updated_data['name'].strip(): # Asegura que el nombre no sea solo espacios
            item_found["name"] = updated_data["name"]
        if 'description' in updated_data: # La descripción puede ser una cadena vacía
            item_found["description"] = updated_data["description"]
        
        return jsonify({"message": f"Item {item_id} actualizado exitosamente", "item": item_found})
    
    elif request.method == 'DELETE':
        # Eliminar un item existente
        items_db.remove(item_found) # Eliminamos el item de la lista
        return jsonify({"message": f"Item {item_id} eliminado exitosamente"})

if __name__ == '__main__':
    # El servidor se ejecutará en http://127.0.0.1:5000/ por defecto
    # debug=True es útil para desarrollo:
    # - Recarga el servidor automáticamente con los cambios en el código.
    # - Muestra errores detallados en el navegador.
    # ¡No uses debug=True en un entorno de producción!
    app.run(debug=True)