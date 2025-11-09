import VideoBody from "./general"
// import { useState, useRef } from 'react'

export default async function VideoPage({
  params,
}: {
  params: Promise<{ videoId: string }>
}) {
  const { videoId } = await params
  let response = await fetch(`http://localhost:8000/api/get/${videoId}`, {
    method: "GET",
  })
  const videoMetadata = await response.json()
  return (
    <div className="p-4">
      <VideoBody videoMetadata={videoMetadata} />
      <div className="mt-[350px]">
        <div className="">
          <h1 className="underline">Optimal Angle</h1>
          <p>{(Math.floor(videoMetadata.optimal_angle * 180 / 3.14))} degrees</p>
        </div>
      </div>
    </div>
  )
}