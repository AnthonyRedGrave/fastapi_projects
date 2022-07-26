<template>
  <div class="chat_view">
      <div class="chat_messages_block">
          <div v-for="message in messages" :key="message.id" class="message_block">
              {{message}}
          </div>
      </div>
      <input type="text" v-model="text_message">
      <button @click="sendMessage">Отправить</button>
  </div>
</template>

<script>
export default {
    name: 'Chat',
    data() {
        return {
            text_message: "",
            web_socket: null,
            messages: []
        }
    },
    created() {
        let _self = this
        this.web_socket = new WebSocket(
        'ws://localhost:8000/ws/'+ this.$route.query.id
        )
        this.web_socket.onopen = function(event){
            console.log(event)
        }
        this.web_socket.onmessage = function(event){
            // console.log(JSON.parse(event.data))
            let event_data = JSON.parse(event.data)
            // console.log(event_data.type)
            if (event_data.type == 'messages'){
                _self.messages = event_data.data
            }
            else if(event_data.type == 'notify'){
                _self.messages.push(event_data.data)
            }
        }
    },
    methods: {
        sendMessage(){
            let data = {
                "text": this.text_message,
                "email": this.$store.state.email
            }
            this.web_socket.send(JSON.stringify(data))
        }
    },
}
</script>

<style>
.chat_messages_block{
    border: 1px solid black;
    height: 500px;
    margin: 10px;
    padding: 15px;
}
</style>