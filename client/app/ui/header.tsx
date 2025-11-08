import Link from "next/link"
import Image from "next/image"
import ThemeToggleButton from "./themetoggler"
import UploadFileButton from "./upload-video-button"

export default function Header() {
    return (
        <nav className="pl-48 py-2 w-full pr-2 bg-background-50 flex flex-row items-center gap-2">
            <UploadFileButton />
            <ThemeToggleButton />
        </nav>
    )
}