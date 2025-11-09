'use client'
import { useState, useRef, useEffect } from 'react'
import { start } from 'repl'


export default function VideoBody({
    videoMetadata,
}: {
    videoMetadata: any
}) {
  const perfectPathCoords = videoMetadata.ball_bboxes
  const videoElementRef = useRef<HTMLVideoElement>(null);
  let canva = useRef<HTMLCanvasElement>(null);
  console.log(videoMetadata);
  useEffect(()=>{
    console.log(videoMetadata);
    const startFrame = videoMetadata.start_frame;
    const endFrame = videoMetadata.end_frame;
    
    if(canva){
      canva.current.height = videoElementRef.current?.height ;
      canva.current.width = videoElementRef.current?.width;
      const ballStartPosX = perfectPathCoords[startFrame][0];
      const ballStartPosY = perfectPathCoords[startFrame][1];
      const hoopStartPosX = videoMetadata.hoop_bbox[0];
      const hoopStartPosY = videoMetadata.hoop_bbox[1];
      console.log(perfectPathCoords)
      const ratioX = videoElementRef.current?.width /(perfectPathCoords[startFrame][0]-perfectPathCoords[endFrame][0]);
      const ratioY = videoElementRef.current.height/(perfectPathCoords[startFrame][1]-perfectPathCoords[endFrame][1]);
      const context = canva.current?.getContext('2d');
      console.log("X" + ratioX);
      console.log("Y" + ratioY);
      
      //context?.drawImage(videoElementRef.current, 0, 0, canva.current?.width, canva.current.height);
      context.fillStyle = "red";
      for(let i = startFrame; i <= endFrame; i++){
        const x = (perfectPathCoords[i][0] ) * (videoElementRef.current.width / 1920)  ;
        const y = (perfectPathCoords[i][1] )* (videoElementRef.current.height/1080);
        console.log("x" + x + "y" + y);
       
        context?.fillRect(x, y, 5, 5);
      }
     
    }
  },[])
  return (
    <div >
      <video ref={videoElementRef} style={{position:"absolute"}} height = {377.5} width={600}  controls src={`http://localhost:8000/media/${videoMetadata.video}`}></video>
      <canvas ref = {canva} style ={{position:'absolute', pointerEvents:"none", left:videoElementRef.current?.getBoundingClientRect().left, top: videoElementRef.current?.getBoundingClientRect().top}}></canvas>
    </div>
  )
}