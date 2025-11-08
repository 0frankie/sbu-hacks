import Link from "next/link"
import Image from "next/image"
import ThemeToggleButton from "./themetoggler"

function UploadFileButton() {
    // async function submitVideo(formData: FormData) {
    //     'use server'
    //     console.log(formData)
    // }
    async function submitVideo(event: React.ChangeEvent<HTMLInputElement>) {
        'use server'
        // POST the video to the api
    }
    return (
        <>
            <input onChange={submitVideo} type="file" id="files" accept="video/*" name="" hidden />
            <label htmlFor="files" className="w-full">
                <div className="h-10 cursor-pointer flex items-center flex-row px-2 gap-2 py-1 bg-primary text-on-primary rounded ">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M5 20h14q.425 0 .713.288T20 21t-.288.713T19 22H5q-.425 0-.712-.288T4 21t.288-.712T5 20m5-2q-.425 0-.712-.288T9 17v-6H7.05q-.625 0-.9-.562t.1-1.063l4.95-6.35q.15-.2.363-.3t.437-.1t.438.1t.362.3l4.95 6.35q.375.5.1 1.063t-.9.562H15v6q0 .425-.288.713T14 18z" />
                    </svg>
                    <p className="max-w-md text-md font-medium leading-8 truncate"> Upload a video for analysis
                    </p>
                </div>
            </label>
        </>
    )
}

export default function Header() {
    return (
        <nav className="pl-48 py-2 w-full pr-2 bg-background-50 flex flex-row items-center gap-2">
            <UploadFileButton />
            <ThemeToggleButton />
        </nav>
    )
}