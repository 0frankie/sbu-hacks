'use client'
// import { useState, useRef } from 'react'

function drawPoint(coordinateRect) {
  if (coordinateRect) {
    console.log(coordinateRect)
  }
}

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
  const perfectPathCoords = videoMetadata.ball_bboxes
  // const videoElementRef = useRef(null);
  return (
    <div>
      <video className='w-full md:w-4/5' controls src={`http://localhost:8000/media/${videoMetadata.video}`}></video>
      <p>dynamic segment with {videoId}</p>
      {perfectPathCoords.map((coordinateRect: Array<number>) => (
        drawPoint(coordinateRect)
      ))}
    </div>
  )
}