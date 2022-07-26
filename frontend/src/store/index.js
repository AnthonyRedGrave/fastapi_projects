import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    access_token: JSON.parse(localStorage.getItem('token')),
    username: JSON.parse(localStorage.getItem('username')),
    email: JSON.parse(localStorage.getItem('email'))

  },
  mutations: {
    updateAuthCredentials(state, { access, username, email }) {
        state.access_token = access
        state.username = username
        state.email = email
    },
  },
  getters:{
    loggedIn(state) {
        return state.access_token != null
    }
  },
  actions: {
    userLogin(context, usercredential) {
            return new Promise((resolve, reject) => {
              let data={
                email: usercredential.email,
                password: usercredential.password
              }
                axios({
                        method: 'post',
                        url: 'http://127.0.0.1:8000/api/login/',
                        data: data,
                        credentials: 'include',
                    }).then((responce) => {
                        localStorage.setItem('token', JSON.stringify(responce.data.access_token))
                        localStorage.setItem('username', JSON.stringify(responce.data.username))
                        localStorage.setItem('email', JSON.stringify(usercredential.email))
                        context.commit('updateAuthCredentials', { access: responce.data.access_token, username: responce.data.username, email: usercredential.email })
                        
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })

        },
  },
  modules: {
  }
})
