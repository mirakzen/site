import axios from "axios";
import {ref} from 'vue';


export default async function api_post(route, data) {
    var response_data = ref(null);

    var url_string = `/api${route}`;
    if (
        window.location.host.includes("localhost:") ||
        window.location.href.includes("localhost:") ||
        window.location.origin.includes("localhost:")
    ) {
        url_string = `http://127.0.0.1:8540/api${route}`;
    }

    const headers = {
        "Content-Type": "application/json",
        "X-SITE-MESSAGES-TOKEN": import.meta.env.VITE_MESSAGE_TOKEN
    };

    try {
        const response = await axios.post(
            url_string, data, {headers: headers}
        ).then(
            function (response) {
                response_data.value = response.data.content;
            }
        ).catch(
            function (error) {
                response_data.value = error.response.data.content;
            }
        );
    } catch (e) {
        response_data.value = "Send error";
    }
    return response_data;
};
