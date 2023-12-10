<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <label>Username:</label>
            <input v-model="username" required>
            <label>Password:</label>
            <input type="password" v-model="password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</template>
  
<script>
export default {
    name: 'LoginView',
    data() {
        return {
            username: '',
            password: ''
        };
    },
    methods: {
        async login() {
            try {
                const response = await this.$axios.post('http://localhost:5002/login', {
                    username: this.username,
                    password: this.password
                });
                console.log(response.data);
            } catch (error) {
                console.error('Error en el inicio de sesión', error.response.data.message);
            }
        }
    }
};
</script>
  