<template>
    <div class="max-w-full sm:max-w-4/5 lg:max-w-3/5 xl:max-w-1/2 mx-auto">
        <div class="flex justify-center mt-4 md:mt-6">
            <img class="w-1/3 sm:w-1/3 md:w-1/3 lg:w-1/4 xl:w-1/4 rounded-full border-2 border-mir-highlight" src="/static/images/moon.png" />
        </div>

        <p class="mt-4 sm:mt-6 text-2xl md:text-3xl font-bold text-mir-highlight">Mir, mirakzen</p>
        <p class="mt-2 sm:mt-4 md:text-lg leading-6">
            Инженер-программист, в свободное время страдающий всякой фигнёй)
        </p>

        <div v-if="socials.length" class="w-full flex flex-col mt-3 sm:mt-4 space-y-4">
            <a
                v-for="social in socials" :key="social.id"
                :href="social.link"
                target="_blank" rel="noreferrer"
                class="group"
            >
                <div class="p-2 sm:p-2 w-full flex flex-row place-items-center bg-mir-secondary sm:group-hover:text-mir-highlight rounded-md sm:group-hover:scale-105 transition ease-in-out duration-200">
                    <font-awesome-icon :icon="social.icon" class="size-12 mr-2 sm:mr-4 sm:group-hover:text-mir-highlight" />
                    <div class="flex flex-col justify-between w-full space-y-2 xl:space-y-1">
                        <span class="text-lg font-bold leading-6 text-left sm:group-hover:text-mir-highlight">{{ social.name }}</span>
                        <!-- <div class="text-justify lg:text-right lg:flex lg:flex-row lg:justify-end">
                            <span class="text-lg font-bold leading-6 lg:w-3/5 text-mir-faded sm:group-hover:text-mir-highlight">{{ social.description }}</span>
                        </div> -->
                        <span class="text-lg font-bold leading-6 text-justify lg:text-right text-mir-faded sm:group-hover:text-mir-highlight">{{ social.description }}</span>
                    </div>
                </div>
            </a>
        </div>
    </div>

    <!-- <div v-if="socials.length" class="mt-3 sm:mt-4 w-full flex flex-row justify-center space-x-4">
        <a
            v-for="social in socials" :key="social.id"
            :href="social.link"
            target="_blank" rel="noreferrer"
            class="group"
        >
            <div class="overflow-hidden p-1 rounded-full border-2 flex place-items-center sm:group-hover:border-mir-highlight sm:group-hover:scale-125">
                <font-awesome-icon :icon="social.icon" class="size-8 md:size-10 sm:group-hover:text-mir-highlight" />
            </div>

        </a>
    </div> -->
</template>

<script setup>
    import { onBeforeMount, ref } from 'vue';
    import api_get from '@/utils/api_get';

    const socials = ref([]);

    onBeforeMount(async () => {
        socials.value = (await api_get('/socials')).value || [];
    });
</script>
