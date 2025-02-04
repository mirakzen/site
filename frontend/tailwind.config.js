/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                'montserrat': ['"Montserrat"', "sans-serif"]
            },
            spacing: {
                '15': '3.75rem;',
                '18': '4.5rem;',
            },
            maxWidth: {
                'screen-4xl': '1920px;',
                '4/5': '80%',
                '3/5': '60%',
                '1/2': '50%',
                '1/3': '33.33333333%'
            },
            colors: {
                'mir-main': '#0a0a0a', /** red-950 #450a0a */ /** zink-950 #09090b */
                'mir-secondary': '#262626', /** red-300 #fca5a5 */ /** neutral-800 #262626 */ /** neutral-900 #171717 */
                'mir-text': '#ACB3BF',  /** gray-200 #e5e7eb */ /** gray-300 #d1d5db */ /** gray-400 #9ca3af */
                'mir-faded': '#6b7280',  /** gray-200 #e5e7eb */ /** gray-300 #d1d5db */ /** gray-400 #9ca3af */ /** gray-500 #6b7280 */ /** gray-600 #4b5563 */
                'mir-link': '#ffffff',
                'mir-highlight': '#FF3F35',
                'mir-wanted': '#eab308', /** yellow-500 #eab308 */
                'mir-done': '#059669', /** emerald-600 #059669 */
                'mir-on-hold': '#3b82f6', /** cyan-600 #0891b2 */ /** blue-500 #3b82f6 */
                'mir-dropped': '#f43f5e', /** rose-500 #f43f5e */
                'mir-uncat': '#86efac', /** green-300 #86efac */
            }
        },
        typography: {
            DEFAULT: {}
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
