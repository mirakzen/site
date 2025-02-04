<template>
    <div v-if="projects.length" class="mt-4 md:mt-6 w-full">
        <div class="md:text-lg leading-6 text-justify md:text-center">
            Почему бы не написать о том, чем я занимался и занимаюсь как разработчик...
            Однако не стоит воспринимать данную страницу как резюме)
        </div>

        <div
            v-for="project in projects" :key="project.id"
            class="overflow-hidden w-full mt-3 sm:mt-4 bg-mir-secondary rounded-md"
        >
            <Disclosure v-slot="{ open }">
                <DisclosureButton
                    class="w-full p-2 sm:p-4 flex place-items-center justify-between select-text"
                >
                    <div class="text-base sm:text-lg w-full">
                        <div class="text-mir-link text-justify" :class="project.summary ? 'mb-2' : ''">{{ project.name }}</div>
                        <div class="text-justify">{{ project.summary }}</div>
                    </div>
                    <font-awesome-icon
                        v-if="project.description || project.pictures && project.pictures.length || project.links && project.links.length"
                        icon="fa-solid fa-angle-down"
                        :class="open ? 'rotate-180 transform' : ''"
                        class="ml-2 sm:ml-4 shrink-0 h-6 w-5 sm:h-7 sm:w-6"
                    />
                </DisclosureButton>
                <DisclosurePanel
                    v-if="project.description || project.pictures && project.pictures.length || project.links && project.links.length"
                    class="pt-0 px-2 pb-2 sm:px-4 sm:pb-4"
                >
                    <div class="w-full pt-2 md:pt-4 border-t-2 border-mir-highlight flex flex-col">
                        <article
                            class="text-justify max-w-none md:text-lg space-y-1 md:space-y-2 text-mir-text prose prose-a:text-mir-link prose-ul:list-disc prose-ul:ml-5"
                            v-html="marked.parse(project.description)"
                        ></article>

                        <div v-if="project.pictures && project.pictures.length" class="mt-2 text-justify md:text-lg">
                            <span class="font-bold">Скрины/картинки: </span>
                            <button type="button"@click="openModal({pics: project.pictures, current_pic: 0});" class="text-mir-link">Нажать тут</button>
                        </div>

                        <div v-if="project.links && project.links.length" class="mt-2 text-justify md:text-lg flex flex-wrap">
                            <span class="font-bold">Ссылки: </span>

                            <a
                                v-for="link in project.links" :key="link.url"
                                class="ml-3 text-mir-link"
                                :href="link.url" target="_blank" rel="noreferrer"
                            >
                                <font-awesome-icon
                                    :icon="link.icon || get_source_icon(link.url)"
                                    class="h-4 w-auto align-middle"
                                /> {{ link.name }}
                            </a>
                        </div>
                    </div>
                </DisclosurePanel>
            </Disclosure>
        </div>
    </div>
    <div v-else class="w-full">
        <h1 class="text-3xl font-bold tracking-tight">Проектов нет, я бездельник)</h1>
        <div class="mt-4 flex items-center justify-center">
            <router-link to="/" class="px-4 py-3 text-lg md:text-xl bg-mir-main sm:hover:text-mir-highlight rounded-md border-2 border-mir-text sm:hover:border-mir-highlight">
                На главную
            </router-link>
        </div>
    </div>

    <TransitionRoot appear :show="isOpen" as="template">
        <Dialog as="div" @close="closeModal" class="relative z-50">
            <TransitionChild
                as="template"
                enter="duration-300 ease-out"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="duration-100 ease-in"
                leave-from="opacity-100"
                leave-to="opacity-0"
            >
                <div class="fixed inset-0 bg-black bg-opacity-75" />
            </TransitionChild>

            <div id="dialog-all" class="fixed inset-0" :style="dataModal.padding" >
                <div
                    class="mx-auto max-w-screen-2xl px-4 sm:px-6 lg:px-8 flex min-h-full items-center justify-center text-center"
                >
                    <TransitionChild
                        as="template"
                        enter="duration-300 ease-out"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="duration-100 ease-in"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                    >
                        <DialogPanel
                            class="overflow-hidden transform rounded-md bg-mir-secondary text-mir-text shadow-xl transition-all relative"
                        >
                            <img
                                :src="dataModal.pics[dataModal.current_pic]"
                                class="max-h-[80svh] object-contain"
                                alt="а нету картинки"
                            />
                            <div
                                v-if="dataModal.pics.length > 1"
                                @click="change_picture(-1)"
                                class="z-[60] absolute left-0 top-0 h-full w-1/2 group cursor-pointer flex flex-col justify-center"
                            >
                                <font-awesome-icon icon="fa-solid fa-angle-left" class="h-14 w-auto hidden sm:group-hover:inline ml-2 mr-auto"/>
                            </div>
                            <div
                                v-if="dataModal.pics.length > 1"
                                @click="change_picture(1)"
                                class="z-[60] absolute right-0 top-0 h-full w-1/2 group cursor-pointer flex flex-col justify-center"
                            >
                                <font-awesome-icon icon="fa-solid fa-angle-right" class="h-14 w-auto hidden sm:group-hover:inline mr-2 ml-auto" />
                            </div>

                            <button className="absolute h-0 w-0 overflow-hidden" /> <!-- for focus-trap -->
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>

<script setup>
    import { onBeforeMount, ref } from 'vue';
    import {
        Disclosure,
        DisclosureButton,
        DisclosurePanel,
        TransitionRoot,
        TransitionChild,
        Dialog,
        DialogPanel
    } from '@headlessui/vue';
    import { marked } from 'marked';
    import api_get from '@/utils/api_get';

    const isOpen = ref(false);
    const dataModal = ref(
        {
            picture: '',
            padding: '',
            current_pic: 0
        }
    );

    function closeModal() {
        isOpen.value = false;
        document.getElementById('dialog-all').style.paddingRight = "";
        dataModal.value.padding = "";
    };

    function openModal(info) {
        isOpen.value = true;
        dataModal.value = JSON.parse(JSON.stringify(info));

        var scroller = window.innerWidth - (document.documentElement.clientWidth || document.body.clientWidth);
        dataModal.value.padding = 'padding-right: ' + scroller + 'px !important;';
    };

    function change_picture(diff) {
        if (dataModal.value.pics.length > 1) {
            dataModal.value.current_pic = ((dataModal.value.pics.length + dataModal.value.current_pic + diff) % dataModal.value.pics.length);
        }
    };

    const projects = ref([]);

    onBeforeMount(async () => {
        projects.value = (await api_get('/projects')).value || [];
    });
</script>
