<template>
  <div id="app">
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <div class="navbar-collapse collapse w-100 order-1 order-md-0 dual-collapse2">
      </div>
      <div class="mx-auto order-0">
        <a class="navbar-brand mx-auto" href="#">NNIO Admin Dashboard </a>
      </div>
      <div class="navbar-collapse collapse w-100 order-3 dual-collapse2">
      </div>
    </nav>
    <div id="nav">
      <router-link to="/">Home</router-link>
      |
      <router-link to="/login">LOGIN</router-link>
      |
      <router-link to="/admin">ADMIN</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
  #app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
