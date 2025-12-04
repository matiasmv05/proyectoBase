from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import database as dbase  
from product import Product
from bson import ObjectId

db = dbase.dbConnection()

app = Flask(__name__)
app.secret_key = 'sportstore_secret_key_2024'

# Categorías disponibles para los productos
CATEGORIES = ['Fútbol', 'Básquetbol', 'Tenis', 'Natación', 'Ciclismo', 'Fitness', 'Running', 'Otros']

@app.route('/')

def home():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products=productsReceived)

@app.route('/products/new', methods=['GET'])
def new_product():
    """Mostrar formulario para crear nuevo producto"""
    return render_template('new_product.html', categories=CATEGORIES)

@app.route('/products', methods=['POST'])
def addProduct():
    """Crear nuevo producto (POST)"""
    products = db['products']
    
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    description = request.form.get('description')
    category = request.form.get('category')
    brand = request.form.get('brand')
    
    if name and price and quantity and category:
        try:
            product_data = {
                'name': name,
                'price': float(price),
                'quantity': int(quantity),
                'description': description,
                'category': category,
                'brand': brand,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            result = products.insert_one(product_data)
            
            flash(f'Producto "{name}" creado exitosamente', 'success')
            return redirect(url_for('home'))
            
        except ValueError:
            flash('Error: Precio y cantidad deben ser valores numéricos válidos', 'danger')
            return redirect(url_for('new_product'))
    else:
        flash('Error: Todos los campos obligatorios deben ser completados', 'danger')
        return redirect(url_for('new_product'))

@app.route('/products/<string:product_id>')
def product_detail(product_id):
    """Ver detalles de un producto específico"""
    products = db['products']
    
    try:
        product = products.find_one({'_id': ObjectId(product_id)})
        if product:
            return render_template('product_detail.html', product=product)
        else:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('home'))
    except:
        flash('ID de producto inválido', 'danger')
        return redirect(url_for('home'))

@app.route('/products/<string:product_id>/edit', methods=['GET'])
def edit_product(product_id):
    """Mostrar formulario para editar producto"""
    products = db['products']
    
    try:
        product = products.find_one({'_id': ObjectId(product_id)})
        if product:
            return render_template('edit_product.html', product=product, categories=CATEGORIES)
        else:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('home'))
    except:
        flash('ID de producto inválido', 'danger')
        return redirect(url_for('home'))

@app.route('/products/<string:product_id>/edit', methods=['POST'])
def update_product(product_id):
    """Actualizar producto existente"""
    products = db['products']
    
    try:
        product = products.find_one({'_id': ObjectId(product_id)})
        if not product:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('home'))
        
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        category = request.form.get('category')
        brand = request.form.get('brand')
        image_url = request.form.get('image_url')
        
        if name and price and quantity and category:
            try:
                update_data = {
                    'name': name,
                    'price': float(price),
                    'quantity': int(quantity),
                    'description': description,
                    'category': category,
                    'brand': brand,
                    'image_url': image_url,
                    'updated_at': datetime.now()
                }
                
                # Mantener la fecha de creación original
                update_data['created_at'] = product.get('created_at', datetime.now())
                
                products.update_one(
                    {'_id': ObjectId(product_id)},
                    {'$set': update_data}
                )
                
                flash(f'Producto "{name}" actualizado exitosamente', 'success')
                return redirect(url_for('home'))
                
            except ValueError:
                flash('Error: Precio y cantidad deben ser valores numéricos válidos', 'danger')
                return redirect(url_for('edit_product', product_id=product_id))
        else:
            flash('Error: Todos los campos obligatorios deben ser completados', 'danger')
            return redirect(url_for('edit_product', product_id=product_id))
            
    except:
        flash('ID de producto inválido', 'danger')
        return redirect(url_for('home'))

@app.route('/products/<string:product_id>/delete', methods=['GET'])
def show_delete(product_id):
    """Mostrar confirmación para eliminar producto"""
    products = db['products']
    
    try:
        product = products.find_one({'_id': ObjectId(product_id)})
        if product:
            return render_template('delete_product.html', product=product)
        else:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('home'))
    except:
        flash('ID de producto inválido', 'danger')
        return redirect(url_for('home'))

@app.route('/products/<string:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """Eliminar producto (POST)"""
    products = db['products']
    
    try:
        product = products.find_one({'_id': ObjectId(product_id)})
        if product:
            product_name = product['name']
            products.delete_one({'_id': ObjectId(product_id)})
            flash(f'Producto "{product_name}" eliminado exitosamente', 'success')
        else:
            flash('Producto no encontrado', 'danger')
    except:
        flash('Error al eliminar el producto', 'danger')
    
    return redirect(url_for('home'))

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000)
