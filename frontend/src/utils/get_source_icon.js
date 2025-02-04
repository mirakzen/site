export default function get_source_icon(link) {
    if (link.toLowerCase().includes("twitch.tv")) {
        return "fa-brands fa-twitch";
    } else if (
        link.toLowerCase().includes("youtube.com")
        ||
        link.toLowerCase().includes("youtu.be")
    ) {
        return "fa-brands fa-youtube";
    } else if (link.toLowerCase().includes("vk.com")) {
        return "fa-brands fa-vk";
    } else if (link.toLowerCase().includes("t.me")) {
        return "fa-brands fa-telegram";
    } else {
        return "fa-solid fa-arrow-up-right-from-square";
    }
};
