from flask import Flask, request, jsonify

app = Flask(__name__)

# Ejemplo para un recurso "items"
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        
        items_list = [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}]
        return jsonify(items_list)
    elif request.method == 'POST':
      
        new_item_data = request.json

        return jsonify({"message": "Item creado exitosamente", "item": new_item_data}), 201 # 201 Created


@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_specific_item(item_id):
    if request.method == 'GET':

        return jsonify({"id": item_id, "name": "Detalles del Item"})
    elif request.method == 'PUT':

        updated_data = request.json
        # ...
        return jsonify({"message": f"Item {item_id} actualizado", "item": updated_data})
    elif request.method == 'DELETE':

        # ...
        return jsonify({"message": f"Item {item_id} eliminado"})

if __name__ == '__main__':
    app.run(debug=True)