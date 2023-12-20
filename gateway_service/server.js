const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');


const app = express();
app.use(cors());
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
    console.error("Error al realizar la solicitud:", error);
    res.status(error.response ? error.response.status : 500).json(error.response ? error.response.data : error.message);
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
    console.error("Error en el inicio de sesión:", error);
    res.status(error.response ? error.response.status : 500).json(error.response ? error.response.data : error.message);
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
    res.status(error.response ? error.response.status : 500).json(error.response ? error.response.data : error.message);
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

app.post('/api/:segments*', async (req, res) => {
  const segments = req.params.segments || '';
  const remainingPath = req.params[0] || '';
  const fullPath = `/api/${segments}${remainingPath}`;
  //token header
  setAxiosHeaders(); // Configura el token en las solicitudes Axios (lo eliminará)

  // Combina los parámetros de la ruta con los datos del cuerpo
  const requestData = {
    pathParams: segments.split('/'),
    bodyParams: req.body
  };

  //dos linea para enviar a los otros servicios
  //const response = await axios.post(fullPath, requestData);
  //res.status(response.status).json(response.data);

  // Aquí puedes imprimir o manejar la ruta dinámica completa y los datos del cuerpo
  console.log(`Recibida solicitud en ${fullPath}`);
  console.log('Datos del cuerpo:', requestData);
  res.status(200).json({ message: 'Data send', fullPath, requestData });

  //globalToken = null; // Invalida el token almacenado
  //setAxiosHeaders(); // Configura el token en las solicitudes Axios (lo eliminará)
  //res.status(200).json({ message: 'Logout exitoso' });
});


//perfiles consumo
app.get('/profiles', async (req, res) => {
  console.log("Recibida solicitud en /profiles");
  try {
    // Verifica si el usuario está autenticado
    if (!globalToken) {
      return res.status(401).json({ message: 'No autorizado. Inicie sesión para acceder.' });
    }

    // Configura el token en las solicitudes Axios
    setAxiosHeaders();

    const response = await axios.get(`${userServiceUrl}/profiles`);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error al obtener perfiles", error.message);
    res.status(401).json({ message: 'Error al obtener perfiles' });
  }
});

//registrar un perfil
app.post('/profiles', async (req, res) => {
  console.log("Recibida solicitud en /profiles (POST)");
  try {
    // Verifica si el usuario está autenticado
    if (!globalToken) {
      return res.status(401).json({ message: 'No autorizado. Inicie sesión para acceder.' });
    }

    // Configura el token en las solicitudes Axios
    setAxiosHeaders();

    const response = await axios.post(`${userServiceUrl}/profiles`, req.body);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error al registrar perfil", error.message);
    res.status(500).json({ message: 'Error al registrar perfil' });
  }
});

app.put('/profiles/:profile_id', async (req, res) => {
  console.log("Recibida solicitud en /profiles/:profile_id");
  try {
    // Verifica si el usuario está autenticado
    if (!globalToken) {
      return res.status(401).json({ message: 'No autorizado. Inicie sesión para acceder.' });
    }

    // Configura el token en las solicitudes Axios
    setAxiosHeaders();

    const profileId = req.params.profile_id;
    const response = await axios.put(`${userServiceUrl}/profiles/${profileId}`, req.body);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error al actualizar perfil", error.message);
    res.status(401).json({ message: 'Error al actualizar perfil' });
  }
});

/* app.put('/profiles/:profile_id/:action', async (req, res) => {
  console.log("Recibida solicitud en /profiles/:profile_id/:action");
  try {
    // Verifica si el usuario está autenticado
    if (!globalToken) {
      return res.status(401).json({ message: 'No autorizado. Inicie sesión para acceder.' });
    }

    // Configura el token en las solicitudes Axios
    setAxiosHeaders();

    const profileId = req.params.profile_id;
    const action = req.params.action; // 'enable' or 'disable'
    const enable = action === 'enable';

    const response = await axios.put(`${userServiceUrl}/profiles/${profileId}/${action}`);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error al habilitar/deshabilitar perfil", error.message);
    res.status(401).json({ message: 'Error al habilitar/deshabilitar perfil' });
  }
}); */

app.get('/profiles/:profile_id/users', async (req, res) => {
  console.log("Recibida solicitud en /profiles/:profile_id/users");
  try {
    // Verifica si el usuario está autenticado
    if (!globalToken) {
      return res.status(401).json({ message: 'No autorizado. Inicie sesión para acceder.' });
    }

    // Configura el token en las solicitudes Axios
    setAxiosHeaders();

    const profileId = req.params.profile_id;
    const response = await axios.get(`${userServiceUrl}/profiles/${profileId}/users`);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error al obtener usuarios por perfil", error.message);
    res.status(401).json({ message: 'Error al obtener usuarios por perfil' });
  }
});
