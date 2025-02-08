<template>
    <header class="fixed w-full bg-mir-main border-b border-mir-highlight z-30">
        <nav class="mx-auto flex items-center justify-between max-w-screen-xl p-4 sm:px-6 lg:px-8" aria-label="Global">
            <div class="flex md:flex-1">
                <router-link to="/" class="flex place-items-center my-auto">
                    <span class="text-lg md:text-xl font-bold leading-6 md:hover:text-mir-highlight">MIR</span>
                </router-link>
            </div>

            <div class="flex lg:hidden">
                <Menu v-slot="{ close }">
                    <MenuButton class="-m-2.5 p-2.5 rounded-md inline-flex items-center justify-center">
                        <font-awesome-icon icon="fa-solid fa-bars" class="h-8 w-8 sm:h-10 sm:w-10" aria-hidden="true" />
                    </MenuButton>
                    <MenuItems class="absolute inset-0 top-16 sm:top-18 bg-mir-main p-4 pt-0 sm:px-6 lg:px-8 flex items-center justify-between border-b border-mir-highlight h-fit">
                        <router-link
                            v-for="link in header_links"
                            :key="link.url"
                            :to="link.url"
                            @click="close"
                            class="text-lg md:text-xl"
                        >
                            {{ link.name }}
                        </router-link>
                    </MenuItems>
                </Menu>
            </div>

            <div class="hidden lg:flex lg:gap-x-8 xl:gap-x-12 text-lg md:text-xl font-semibold leading-6">
                <div v-for="link in header_links" :key="link.name">
                    <router-link :key="link.url" :to="link.url" class="sm:hover:text-mir-highlight">{{ link.name }}</router-link>
                </div>
            </div>
        </nav>
    </header>

    <main class="mt-16 sm:mt-18 lg:mt-15 border-t border-mir-highlight overflow-hidden mx-auto w-full max-w-screen-xl px-4 sm:px-6 lg:px-8 grow shrink-0 flex place-items-center">
        <div class="flex flex-col w-full text-center mb-2">
            <RouterView />
        </div>
    </main>

    <footer class="mx-auto flex flex-col md:flex-row items-center justify-center max-w-screen-xl pt-8 pb-4 px-4 sm:px-6 lg:px-8 w-full">
        <!-- <div class="mx-auto flex flex-col sm:flex-row items-center justify-around max-w-screen-xl p-4 sm:p-6 lg:px-8"> -->
        <div class="text-lg md:text-xl font-semibold leading-6">
            Made by <router-link to="/login">me)</router-link> and still WIP, 2022-2025
        </div>
    </footer>

    <button id="scrollTopButton" @click="scrollToTop" class="fixed bottom-0 right-0 z-20 m-4 invisible">
        <div class="rounded-md border-2 border-mir-text h-12 w-12 flex flex-col text-center sm:hover:text-mir-highlight sm:hover:border-mir-highlight">
            <font-awesome-icon icon="fa-solid fa-angles-up" class="h-10 my-auto" />
        </div>
    </button>
</template>


<script setup>
    import { RouterLink, RouterView } from 'vue-router';
    import { onMounted, onUnmounted, ref } from 'vue';
    import {
        Menu,
        MenuButton,
        MenuItems
    } from '@headlessui/vue';

    const header_links = [
        {
            name: "ПРОЕКТЫ",
            url: "/projects"
        },
        {
            name: "ИГРЫ",
            url: "/games"
        },
        // {
        //     name: "СЭТАП",
        //     url: "/setup"
        // }
    ];

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    onMounted(() => {
        window.addEventListener("scroll", handleScroll);
    });

    onUnmounted(() => {
        window.removeEventListener("scroll", handleScroll);
    });

    function handleScroll() {
        const scrollBtn = document.getElementById("scrollTopButton");

        if (window.scrollY > 40) {
            scrollBtn.classList.remove("invisible");
        } else {
            scrollBtn.classList.add("invisible");
        }
    };
</script>
