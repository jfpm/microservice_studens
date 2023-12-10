<template>
    <div>
        <h2>Users</h2>
        <button @click="getUsers">Get Users</button>
        <ul v-if="users.length">
            <li v-for="user in users" :key="user.username">{{ user.username }}</li>
        </ul>
    </div>
</template>
  
<script>
export default {
    name: 'UsersView',
    data() {
        return {
            users: []
        };
    },
    methods: {
        async getUsers() {
            try {
                const response = await this.$axios.get('http://localhost:5002/users');
                this.users = response.data.users;
            } catch (error) {
                console.error('Error al obtener usuarios', error.response.data.message);
            }
        }
    }
};
</script>
  