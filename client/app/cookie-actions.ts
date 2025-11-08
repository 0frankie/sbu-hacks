"use server"

import { cookies } from "next/headers";
export default async function toggleTheme() {
    const cookieStore = await cookies()
    const oldTheme = cookieStore.get('theme');
    if (oldTheme === undefined) {
        cookieStore.set('theme', 'dark')
    } else {
        const newTheme = oldTheme?.value === 'light' ? 'dark' : 'light';
        cookieStore.set('theme', newTheme)
    }
}

// export async function setThemeInitially() {
//     const cookieStore = await cookies()
//     cookieStore.set('theme', 'light')
// }