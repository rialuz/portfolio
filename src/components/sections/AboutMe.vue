<script setup lang="ts">
const changeColorOnHover = () => {
  document.getElementsByTagName('span')
}
</script>

<template>
  <div id="about" class="about-section">
    <div class="img-container">
      <img src="../data/images/img.jpg" alt="image of luz" />
    </div>

    <div class="about-container">
      <h1 class="title">Hey! <span>I'm Luz Lopez Marcano</span></h1>
      <div class="about-details">
        <p>
          I am a passionate software engineer based in Maryland with 1.5 years of hands-on work
          experience developing new features as well as improving on existing features. I enjoy the
          challenge of finding effective solutions to problems I face. I've learned a lot in my past
          experiences and am confident in my ability to be a reliable asset to any team I am in.
        </p>
        <div class="tech-list">
          <h3>I've worked with:</h3>
          <ul>
            <li>HTML, CSS, JS</li>
            <li>Typescript</li>
            <li>Vue.js</li>
            <li>React.js</li>
            <li>Playwright</li>
            <li>Jest</li>
            <li>Java</li>
            <li>Git/Gitlab</li>
            <li>CI/CD</li>
            <li>New Relic</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
img {
  width: 250px;
}
.img-container {
  width: 250px;
  height: 250px;
  border-radius: 50%;
  border: 4px solid #3d52a0;
  overflow: hidden;
  margin: 0 auto;
}

.about-section {
  margin: 0 auto;
  width: 60vw;

  span:hover {
    color: #3d52a0;
    animation-name: color-changer;
    animation-duration: 4s;
    animation-iteration-count: infinite;
  }
}

.tech-list {
  margin-left: 25px;

  ul {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    margin-left: 30px;
  }
}

@keyframes color-changer {
  0% {
    color: #3d52a0;
  }
  25% {
    color: #45a3e2;
  }
  50% {
    color: #8d32b0;
  }
  100% {
    color: #3d52a0;
  }
}



@media screen and (width <= 875px) {
  .about-container {
    justify-content: flex-end;
    flex-direction: column-reverse;
    /* margin: 0 auto; */
    /* row-gap: 40px; */
    /* align-items: center; */
  }
  .about-details {
    margin: 10px;
    width: fit-content;
  }
}
</style>
