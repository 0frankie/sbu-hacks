'use client'

import { Button } from "./button"

export default async function DeleteVideoButton({ id, refreshFn }: { id: string, refreshFn: () => Promise<void>;}) {
    async function handleDelete(videoId: string) {
        // delete the video
        await fetch(`http://localhost:8000/api/delete/${videoId}`, {
            method: "GET",
        })
        // refresh
        refreshFn();
    }
    return (
        <button onClick={() => { handleDelete(id) }} className="button-transition flex flex-row justify-center items-center p-2 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="currentColor" d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z" /></svg>
        </button>
    )
    return (
        <Button variant="outline" onClick={() => { deleteVideo(id) }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="currentColor" d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z" /></svg>
        </Button>
    )
}