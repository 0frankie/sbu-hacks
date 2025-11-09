'use client'
import { useState, useRef } from 'react'

function drawPoint(coordinateRect, videoRect) {
    if (coordinateRect) {
        console.log(coordinateRect)
        console.log(videoRect.x)
    }
}

export default function VideoBody({
    videoMetadata,
}: {
    videoMetadata: any
}) {
    const perfectPathCoords = videoMetadata.ball_bboxes
    const videoElementRef = useRef(null);
    return (
        <div>
            {perfectPathCoords.map((coordinateRect: Array<number>) => (
                drawPoint(coordinateRect, videoElementRef.current ? videoElementRef.current.getBoundingClientRect() : null)
            ))}
            <video ref={videoElementRef} className='w-full md:w-4/5' controls src={`http://localhost:8000/media/${videoMetadata.video}`}></video>
            <p>dynamic segment with</p>
        </div>
    )
}