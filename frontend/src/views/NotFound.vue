<template>
    <p class="text-8xl font-semibold text-mir-highlight">404</p>
    <h1 class="mt-2 text-xl font-bold tracking-tight">Страница не найдена</h1>
    <div class="mt-4 flex items-center justify-center">
        <router-link to="/" class="px-4 py-3 md:text-lg bg-mir-secondary sm:hover:text-mir-highlight rounded-md ">
            На главную
        </router-link>
    </div>
</template>


<script setup>
    import { RouterLink } from 'vue-router';
</script>
