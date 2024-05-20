<script setup lang="ts">

</script>

<template>
    <div id="about" class="about-section">
        
        <h1 class="title">Hi! I'm Luz Lopez Marcano</h1>
        <div class="about-container">
           <div class="about-details">
            <p>
            I am a passionate software engineer based in Maryland with 1.5 years
            of hands-on work experience developing new features as well as improving
            on existing features. I enjoy the challenge of finding effective solutions to
            problems I face. I've learned a lot in my past experiences and am confident
            in my ability to be a reliable asset to any team I am in. 
            </p>

            </div>  
            <div class="img-container">
            <img src="../data/img.jpg" alt="image of luz" />
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
    border: 4px solid white;
    overflow: hidden;
}

.about-section {
    margin: 0 auto;
    width: 80vw;
}

.about-details {
    width: 420px;
    padding-top: 25px;

}

.about-container {
    display: flex;
    gap: 50px;
}

@media screen and (width <= 875px) {
    .about-container {
        justify-content: flex-end;
        flex-direction: column-reverse;
        row-gap: 40px;
        align-items: center;
}
.about-details {
    margin: 10px;
    width: fit-content;
}

}

</style>