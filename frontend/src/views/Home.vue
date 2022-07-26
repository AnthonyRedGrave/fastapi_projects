<template>
  <div class="home">
    <router-link to='/login'>Логин</router-link>
    <div class="create_chat_form">
      <label class="user_input_label">Введите пользователя</label>
      <input type="text" class="user_input_name" v-model="username_search" @input="searchUsers">
      <div class="users_search">
        <div class="users_list_block">
          <div v-for="user in search_users" :key="user.id" class="user_block">
            <span style="font-size: 18px;" @click="addToChat(user.email)">{{user.name}}</span>
            <span>{{user.email}}</span>
          </div>
        </div>
      </div>
      <button class="create_chat_button" @click="createChat()">Создать чат</button>
    </div>
    <chats/>
  </div>
</template>

<script>
import axios from 'axios'
import Chats from '../components/Chats.vue'
export default {
  name: 'Home',
  components: {
    Chats
  },
  data() {
    return {
      search_users: [],
      search_users_names:[],
      username_search: null,
      users_to_chat: []
    }
  },
  methods: {
    searchUsers(){
      if (this.username_search !== ''){
           axios
                .get(`http://127.0.0.1:8000/api/users`, {
                headers: {
                  Authorization: `Bearer ${this.$store.state.access_token}`,
                },
                params: {
                    username: this.username_search
                },
                })
                .then((response) => {
                  response.data.forEach(element => {
                    if (!this.search_users_names.includes(element.name)){
                      this.search_users.push(element)
                      this.search_users_names.push(element.name)                    
                    }
                  });
                  
                })
                .catch((err) => {
                    console.log(err);
                });
      }
      else{
        this.search_users = []
        this.search_users_names = []  
      }
    },
    addToChat(user_name){
      this.users_to_chat.push(user_name)
    },
    createChat(){
      let data = {
                  users: this.users_to_chat
      }
      axios({
              method: "post",
              url: `http://127.0.0.1:8000/api/chats_create`,
              data: data,
              headers: {
              Authorization: `Bearer ${this.$store.state.access_token}`,
              },
              })
              .then((response) => {
                  console.log(response.data)
                  this.$router.push({ path: 'Chat', id: response.data.id})
              })
              .catch((err) => {
              console.log(err)
              // Object.entries(err.response.data).forEach((element)=>{
              //   this.errorList.push(element)
              // })
              });
    }
  },
}
</script>

<style>
.create_chat_form{
  display: flex;
  justify-content: center;
  flex-direction: column;
  padding: 15px;
  margin: 15px 0;
}
.user_input_name{
  margin-bottom: 10px;
}
.create_chat_button{
  width: 300px;
  margin: 0 auto;
}
.users_search{
  border: 1px solid black;
  height: 100px;
  margin: 15px 0;
  border-radius: 5px;
  padding: 5px;
}
.users_list_block{
  display: flex;
  flex-direction: row;
  gap: 10px;
}
.user_block{
  display: flex;
  flex-direction: column;
  border: 1px solid black;
  padding: 5px;

}
</style>