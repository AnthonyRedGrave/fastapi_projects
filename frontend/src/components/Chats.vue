<template>
  <div class="chats_view">
      CHATS
      <div class="chats_list">
          <div class="chats_notifications">
            {{notify_message}}
          </div>
        <div v-for="chat in chats" :key="chat.id" class="chat_block" @click="toChat(chat.id)">
            <h2>{{chat.id}}</h2>
            <div v-for="user in chat.users" :key="user.id" class="chat_user">
                {{user.email}}
                {{user.name}}
            </div>
        </div>
      </div>
  </div>
</template>

<script>
// import axios from 'axios'
export default {
    name: 'Chats',
    data() {
        return {
            text_message: "",
            web_socket: null,
            chats: [],
            notify_message: null
        }
    },
    created() {
        let _self = this
        this.web_socket = new WebSocket(
        'ws://localhost:8000/ws?token=' + this.$store.state.access_token
        )
        this.web_socket.onopen = function(event){
            console.log(event)
        }
        setTimeout(function(){
            _self.sendMessage()
        }, 1000);
        this.web_socket.onmessage = function(event){
            let event_data = JSON.parse(event.data)
            if (event_data.status == 401){
                _self.$router.push({name: 'Login'})
            }
            else if(event_data.type == "chats"){
                console.log(event_data)
                _self.chats = event_data.data
            }
            else if(event_data.type == "notify_new_message"){
                console.log(event_data)
                _self.notify_message = event_data.data
            }
        }
    },
    methods: {
        sendMessage(){
            let data = {
                "email": this.$store.state.email
            }
            this.web_socket.send(JSON.stringify(data))
        },
        toChat(chat_id){
            this.$router.push({ path: 'chat', query: {'id': chat_id }})
        }
    },
}
</script>

<style>
.chat_block{
    padding: 15px;
    border: 1px solid black;
}
.chat_block:hover{
    background: rgb(214, 214, 214);
}
.chats_notifications{
    background: blue;
    
}
</style>