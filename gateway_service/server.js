const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 5002;

const userServiceUrl = "http://users_service:5000";

// Función para configurar el token en las solicitudes Axios
const setAxiosHeaders = () => {
  if (globalToken) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${globalToken}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }
};

// Variable global para almacenar el token
let globalToken = null;
let globalDataUsuario = null;

const dns = require('dns');

dns.lookup('users_service', (err, address, family) => {
  console.log('address: %j family: IPv%s', address, family);
});

app.use(bodyParser.json());

app.post('/register', async (req, res) => {
  console.log("Recibida solicitud en /register");
  try {
    const response = await axios.post(`${userServiceUrl}/register`, req.body);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error al registrar usuario", error.message);
    res.status(500).json({ message: 'Error al registrar usuario' });
  }
});

app.post('/login', async (req, res) => {
  console.log("Recibida solicitud en /login");
  try {
    const response = await axios.post(`${userServiceUrl}/login`, req.body);
    globalToken = response.data.token; // Almacena el token globalmente
    globalDataUsuario = response.data.user; // Almacena el usuario globalmente
    setAxiosHeaders(); // Configura el token en las solicitudes Axios
    console.log('token almacenado', globalToken);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error en el inicio de sesión", error.message);
    res.status(401).json({ message: 'Error en el inicio de sesión' });
  }
});

app.get('/users', async (req, res) => {
  console.log("Recibida solicitud en /users");
  try {
    // Verifica si el usuario está autenticado
    if (!globalToken) {
      return res.status(401).json({ message: 'No autorizado. Inicie sesión para acceder.' });
    }

    // Configura el token en las solicitudes Axios
    setAxiosHeaders();

    const response = await axios.get(`${userServiceUrl}/users`);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error en buscar usuarios", error.message);
    res.status(401).json({ message: 'Error en buscar usuarios' });
  }
});

app.get('/hello', (req, res) => {
  console.log("Recibida solicitud en /hello");
  res.status(200).json({ message: 'Hola' });
});

// Ruta de logout
app.post('/logout', (req, res) => {
  console.log("Recibida solicitud en /logout");
  globalToken = null; // Invalida el token almacenado
  setAxiosHeaders(); // Configura el token en las solicitudes Axios (lo eliminará)
  res.status(200).json({ message: 'Logout exitoso' });
});

app.listen(port, () => {
  console.log(`Servidor de Node.js escuchando en el puerto ${port}`);
});
