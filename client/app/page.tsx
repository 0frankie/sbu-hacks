'use client'

import Link from "next/link";
import useSWR, { useSWRConfig } from 'swr'

const fetcher = (...args) => fetch(...args).then(res => res.json())

export default function Home() {
  const { mutate } = useSWRConfig()
  async function deleteVideo(videoId: string) {
    await fetch(`http://localhost:8000/api/delete/${videoId}`, {
      method: "GET",
    })
    mutate('http://localhost:8000/api/all')
  }

  const { data: allVideos, error, isLoading } = useSWR('http://localhost:8000/api/all', fetcher)

  if (error) return <div>Failed to load, is the server running? </div>

  // if the user has some videos
  if (isLoading) {
    return (
      <div className="h-full rounded flex items-center justify-center">
        <main className="rounded flex w-full h-full flex-col items-center justify-center">
          <p className={`text-xl max-w-md text-center font-medium`}>
            Loading...
          </p>
        </main>
      </div>
    )
  }

  // console.log(allVideos);
  if (allVideos.length === 0) {
    return (
      <div className="h-full rounded flex items-center justify-center">
        <main className="rounded flex w-full h-full flex-col items-center justify-center">
          <p className={`text-xl max-w-md text-center font-medium`}>
            You don't have any videos in the database. Upload a video to get started.
          </p>
        </main>
      </div>
    );
  }

  return (
    <div className="grid grid-rows-2 grid-cols-2 gap-4 p-4">
      {allVideos.map((video) => (
        <div key={`${video.id}`} className="flex flex-col bg-background-50 rounded">
          <div className="flex justify-end">
            <button onClick={() => {
              deleteVideo(video.id)
            }} className="button-transition flex flex-row justify-center items-center p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path fill="currentColor" d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z" /></svg>
            </button>
          </div>
          <Link href={`/video/${video.id}`}>
            <img className="rounded" src={`http://localhost:8000/media/${video.thumbnail}`} alt="" />
            <div className="px-2 py-2">
              <p>{video.video}</p>
            </div>
          </Link>
        </div>
      ))
      }
    </div >
  );
}
