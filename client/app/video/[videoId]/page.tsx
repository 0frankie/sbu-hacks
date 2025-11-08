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
    <VideoBody videoMetadata={videoMetadata}/>
  )
}