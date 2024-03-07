from flask import Flask, request, jsonify
import mysql.connector
import hashlib

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'btnsdrtwj5nxrypwcudz-mysql.services.clever-cloud.com',
    'user': 'uwec7nhlqoobwbmh',
    'password': 'L2sdCH6IMHjcw9bbS4AO',
    'database': 'btnsdrtwj5nxrypwcudz'
}


# Endpoint para registrar usuarios
@app.route('/register', methods=['POST'])
def register():
  data = request.json
  nombre_usuario = data['nombre_usuario']
  correo_electronico = data['correo_electronico']
  contrasena = data['contrasena']

  # Aquí deberías implementar un mejor mecanismo de cifrado de contraseñas
  hash_contrasena = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO Usuarios (NombreUsuario, CorreoElectronico, Contrasena) VALUES (%s, %s, %s)"
    cursor.execute(query,
                   (nombre_usuario, correo_electronico, hash_contrasena))
    conn.commit()
  except mysql.connector.Error as e:
    return jsonify({'error': str(e)}), 500
  finally:
    cursor.close()
    conn.close()

  return jsonify({'message': 'Usuario registrado con éxito'}), 201


if __name__ == '__main__':
  app.run(debug=True)
