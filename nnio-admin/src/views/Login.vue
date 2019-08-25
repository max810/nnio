<template>
  <div class="container">
    <div class="row" id="first-row">
      <div class="col-sm"></div>
      <div class="col-sm"></div>
      <div class="col-sm"></div>
    </div>
    <div class="row">
      <div class="col-sm"></div>
      <div class="col-sm">
        <form v-on:submit.prevent="submit" id="login-form" method="post">
          <h2 class="text-center">Log in</h2>
          <div class="form-group">
            <input
              v-model="email"
              type="email"
              name="username"
              class="form-control"
              placeholder="Email"
              required="required"
            />
          </div>
          <div class="form-group">
            <input
              v-model="password"
              type="password"
              name="password"
              class="form-control"
              placeholder="Password"
              required="required"
            />
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-primary btn-block">Log in</button>
          </div>
        </form>
        <span id="login-error" v-bind:style="loginErrorStyle">Wrong email or password. Try again.</span>
      </div>
      <div class="col-sm"></div>
    </div>
    <span id="err-msg">{{ msg }}</span>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import axios from "axios";
import { backendUrls } from "@/constants";

@Component({})
export default class Login extends Vue {
  @Prop(String) msg: String | undefined;
  email: string = "";
  password: string = "";
  loginSuccessfull: boolean = true;

  get loginErrorStyle() {
    return {
      visibility: this.loginSuccessfull ? "hidden" : "visible"
    };
  }

  submit(event: Event) {
    this.loginSuccessfull = true;

    let bodyFormData = new FormData();
    bodyFormData.append("username", this.email);
    bodyFormData.append("password", this.password);

    axios
      .post(backendUrls.login, bodyFormData)
      .then(async response => {
        console.log(`LOGIN STATUS: ${response.status}, ${response.statusText}`);
        const data = response.data;
        const jwt: string =
          typeof data == "string"
            ? JSON.parse(data)["access_token"]
            : data["access_token"];

        localStorage.setItem("jwt", jwt);
        await this.$router.push({ name: "admin" });
      })
      .catch(err => {
        console.log(`LOGIN ERROR: ${err}`);
        console.log({ err });
        this.loginSuccessfull = false;
      });
  }
}
</script>

<style scoped>
#first-row {
  height: 100px;
}

#login-error {
  font-size: 16px;
  color: red;
}

#err-msg {
  color: red;
  font-weight: bold;
  font-size: 18px;
}
</style>