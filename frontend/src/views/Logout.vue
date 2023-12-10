<template>
    <div>
      <h2>Logout</h2>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LogoutView',
    methods: {
      async logout() {
        try {
          const response = await this.$axios.post('http://localhost:5002/logout');
          console.log(response.data);
        } catch (error) {
          console.error('Error en el cierre de sesión', error.response.data.message);
        }
      }
    }
  };
  </script>
  