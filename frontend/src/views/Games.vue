<template>
    <div class="mt-4 md:mt-6 sm:text-lg leading-6 text-justify">
        Тут перечислены игры, которые я либо пробовал, либо хочу попробовать.
        Тут не будет перечисления всех имеющихся игр
        (для этого есть
        <a
            href="https://steamcommunity.com/id/mirakzen"
            target="_blank" rel="noreferrer"
            class="text-mir-link"
        >
            <font-awesome-icon icon="fa-brands fa-steam" class="h-5 w-auto align-middle mr-1" />Steam
        </a>, а бесплатную библиотеку Epic Store даже трогать не хочется),
        большинства опробованных демо-версий или
        большей части игр из списка желаемого Steam (уж больно он большой, и бОльшую его часть я скорее всего никогда и не трону).
        А про что-то я и вовсе мог забыть... Ну и пара заметок: не обязательно игр, которые я бы хотел пройти, у меня нет,
        а также даже заброшеные прохождения могут когда-нибудь вернуться)
    </div>

    <div v-if="has_games">
        <div class="mt-3 sm:mt-4">
            <div class="flex justify-center">
                <input
                    @input="update_search"
                    @keyup.enter="fake_submit()"
                    placeholder="Поиск..."
                    id="search_input"
                    class="focus:outline-none w-4/5 sm:w-1/3 p-2 pr-8 rounded-md text-mir-text bg-mir-secondary placeholder:text-mir-text placeholder:bg-mir-secondary placeholder-mir-text autofill:bg-mir-secondary"
                />
                <button @click="search_reset()">
                    <font-awesome-icon icon="fa-solid fa-xmark" class="h-6 w-auto align-middle -ml-9" />
                </button>
            </div>
        </div>

        <div v-for="status in statuses" :key="status">
            <div
                v-if="filtered_games.hasOwnProperty(status.code)"
                class="overflow-hidden w-full mt-3 sm:mt-4 bg-mir-secondary rounded-md"
                :key="is_search"
            >
                <Disclosure v-slot="{ open }" :default-open="status.code == 'in_progress' || is_search">
                    <DisclosureButton
                        class="w-full flex place-items-center justify-between p-2 sm:p-4"
                        :class="get_color_mapping(status.code)"
                    >
                        <span class="px-1 sm:text-lg font-bold text-left">{{ status.name }}</span>
                        <font-awesome-icon icon="fa-solid fa-angle-down" :class="open ? 'rotate-180 transform' : ''" class="ml-2 sm:ml-4 shrink-0 h-6 w-5 sm:h-7 sm:w-6" />
                    </DisclosureButton>
                    <DisclosurePanel class="pt-0 px-2 pb-2 sm:px-4 sm:pb-4">
                        <div class="w-full pt-2 md:pt-4 border-t-2 border-mir-highlight flex flex-col space-y-2">
                            <button
                                v-for="game in filtered_games[status.code]" :key="game.id"
                                type="button"
                                @click="openModal(game)"
                                class="flex justify-between place-items-center p-2 rounded-md bg-mir-main"
                            >
                                <span class="sm:text-lg text-left space-x-1">
                                    {{ game.name }}
                                </span>
                                <div class="pl-1 text-sm sm:text-base font-bold text-end space-x-1">
                                    <font-awesome-icon
                                        v-if="game.speenrun && game.speenrun.code"
                                        icon="fa-solid fa-trophy"
                                        class="shrink-0 h-4 w-4"
                                        :class="get_color_mapping(game.speenrun.code)"
                                    />
                                    <font-awesome-icon
                                        v-if="game.full_completion && game.full_completion.code"
                                        icon="fa-solid fa-star"
                                        class="shrink-0 h-4 w-4"
                                        :class="get_color_mapping(game.full_completion.code)"
                                    />
                                </div>
                            </button>
                        </div>
                    </DisclosurePanel>
                </Disclosure>
            </div>
        </div>
    </div>
    <div v-else class="w-full">
        <h1 class="mt-2 text-xl font-bold tracking-tight">Игорь тонет)</h1>
        <div class="mt-4 flex items-center justify-center">
            <router-link to="/" class="px-4 py-3 md:text-lg bg-mir-secondary sm:hover:text-mir-highlight rounded-md ">
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
                    class="mx-auto max-w-screen-xl flex min-h-full items-center justify-center px-6 lg:px-8 text-center"
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
                            class="transform overflow-hidden w-full sm:w-2/5 rounded-md bg-mir-secondary text-mir-text shadow-xl transition-all"
                        >
                            <div class="flex flex-col">
                                <button className="absolute h-0 w-0 overflow-hidden" /> <!-- for focus-trap -->
                                <a v-if="dataModal.picture" class="w-full h-auto mb-1 sm:mb-2" :href="dataModal.link" target="_blank" rel="noreferrer">
                                    <img v-if="dataModal.picture" :src="dataModal.picture" class="w-full h-auto" />
                                </a>
                                <div class="flex flex-col justify-center w-full p-2 text-sm sm:text-base">
                                    <a
                                        :href="dataModal.link" target="_blank" rel="noreferrer"
                                        class="sm:text-lg font-bold leading-4 sm:leading-5 mx-auto text-mir-link"
                                    >
                                        {{ dataModal.name }} <font-awesome-icon v-if="dataModal.link" icon="fa-solid fa-arrow-up-right-from-square" class="h-3 w-auto font-bold align-middle" />
                                    </a>
                                    <div class="pt-2">
                                        <p v-if="dataModal.comment"><span class="font-bold">Комментарий: </span>{{ dataModal.comment }}</p>
                                        <p><span class="font-bold">Жанр: </span>{{ dataModal.genre }}</p>
                                        <div class="flex flex-wrap justify-center">
                                            <span class="font-bold mr-1">Статусы: </span>
                                            <template v-for="(status, index) in dataModal.statuses">
                                                <template v-if="index > 0">,</template>
                                                {{ status.name }}
                                            </template>
                                        </div>

                                        <p v-if="dataModal.full_completion && dataModal.full_completion.name"><span class="font-bold">Полное прохождение: </span>{{ dataModal.full_completion.name }}</p>
                                        <p v-if="dataModal.speenrun && dataModal.speenrun.name"><span class="font-bold">Спидран: </span>{{ dataModal.speenrun.name }}</p>
                                        <div v-if="dataModal.links && dataModal.links.length" class="flex flex-wrap justify-center">
                                            <span class="font-bold mr-2">Записи:</span>
                                            <div
                                                v-for="record in dataModal.links" :key="record.name"
                                                :class="(dataModal.links.length > 1 && record.order != dataModal.links.length) ? 'mr-3' : ''"
                                            >
                                                <a v-if="record.url.includes('http')" :href="record.url" class="font-bold text-mir-link" target="_blank" rel="noreferrer">
                                                    <font-awesome-icon
                                                        :icon="record.icon || get_source_icon(record.url)"
                                                        class="h-4 w-auto align-middle"
                                                    /> {{ record.name }}
                                                </a>
                                                <p v-if="!record.url.includes('http')" class="text-wrap">
                                                    {{ record.name }}: {{ record.url }}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>

<script setup>
    import { onBeforeMount, ref } from 'vue';
    import { useRouter, useRoute } from 'vue-router';
    import {
        Disclosure,
        DisclosureButton,
        DisclosurePanel,
        TransitionRoot,
        TransitionChild,
        Dialog,
        DialogPanel
    } from '@headlessui/vue';
    import api_get from '@/utils/api_get';
    import get_source_icon from '@/utils/get_source_icon';

    const route = useRoute();
    const router = useRouter();
    const query_params = ref(
        {
            search: "",
            id: ""
        }
    );

    function update_query() {
        const q = {};
        if (query_params.value.search) {
            q.search = query_params.value.search;
        }
        if (query_params.value.id) {
            q.id = query_params.value.id;
        }
        router.replace({query: q, force: false});
    };

    const is_search = ref(false);
    const search_string = ref('');

    function update_search(event) {
        search_string.value = event.target.value;
        if (search_string.value) {
            query_params.value.search = search_string.value;
            for (const status of statuses.value) {
                if (games.value.hasOwnProperty(status.code)) {
                    filtered_games.value[status.code] = games.value[status.code].slice().filter((game) => game.name.toLowerCase().includes(search_string.value.toLowerCase()));
                    if (filtered_games.value[status.code].length == 0) {
                        delete filtered_games.value[status.code];
                    }
                }
            }
            is_search.value = true;
        } else {
            query_params.value.search = "";
            is_search.value = false;
            filtered_games.value = JSON.parse(JSON.stringify(games.value));
        }
        update_query();
    };

    function search_reset() {
        document.getElementById("search_input").value = "";
        search_string.value = "";
        filtered_games.value = JSON.parse(JSON.stringify(games.value));
        query_params.value.search = "";
        is_search.value = false;
        update_query();
    };

    function fake_submit() {
        document.getElementById("search_input").blur();
    };

    const isOpen = ref(false);
    const emptyModel = {
        id: 0,
        name: '',
        subname: '',
        link: '',
        picture: '',
        statuses: [],
        full_completion: {},
        speenrun: {},
        genre: '',
        links: [],
        comment: '',
        padding: ''
    };
    const dataModal = ref(emptyModel);

    function closeModal() {
        isOpen.value = false;
        document.getElementById('dialog-all').style.paddingRight = "";
        dataModal.value.padding = "";
        query_params.value.id = "";
        update_query();
    };

    function openModal(game_info) {
        isOpen.value = true;
        dataModal.value = JSON.parse(JSON.stringify(game_info));
        query_params.value.id = dataModal.value.id;
        update_query();

        var scroller = window.innerWidth - (document.documentElement.clientWidth || document.body.clientWidth);
        dataModal.value.padding = 'padding-right: ' + scroller + 'px !important;';
    };

    const statuses = ref([]);
    const games = ref({});
    const filtered_games = ref([]);
    const has_games = ref(true);

    onBeforeMount(async () => {
        statuses.value = (await api_get('/games/statuses')).value || [];
        games.value = (await api_get('/games')).value || {};

        filtered_games.value = JSON.parse(JSON.stringify(games.value));

        let found_statuses = 0;
        for (const status of statuses.value) {
            if (games.value.hasOwnProperty(status.code)) {
                found_statuses += 1;
            }
        }
        if (!found_statuses) {
            has_games.value = false;
        }

        const query_search = route.query.search;
        if (query_search) {
            const search = (Array.isArray(query_search) ? query_search : [query_search])[0];
            query_params.value.search = search;
            document.getElementById("search_input").value = search;
            update_search({target: {value: search}});
        }

        const query_id = route.query.id;
        if (query_id) {
            const game_id = (Array.isArray(query_id) ? query_id : [query_id])[0];
            const all_games = [];
            for (const status of statuses.value) {
                if (games.value.hasOwnProperty(status.code)) {
                    all_games.push(...games.value[status.code].slice());
                }
            }
            for (const game of all_games) {
                if (game.id == game_id) {
                    query_params.value.id = game_id;
                    openModal(game);
                    break;
                }
            }
        }
    });

    const color_mapping = new Map();
    color_mapping.set("in_progress", "");
    color_mapping.set("wanted", "text-mir-wanted");
    color_mapping.set("completed", "text-mir-done");
    color_mapping.set("mp_coop_uncat", "text-mir-uncat");
    color_mapping.set("on_hold", "text-mir-on-hold");
    color_mapping.set("dropped", "text-mir-dropped");

    function get_color_mapping(item) {
        if (color_mapping.has(item)) {
            return color_mapping.get(item);
        }
        return "";
    }
</script>
