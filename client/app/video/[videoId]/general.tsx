'use client'
import { Pi } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import { start } from 'repl'
import "./general.css";

export default function VideoBody({
  videoMetadata,
}: {
  videoMetadata: any
}) {
  const perfectPathCoords = videoMetadata.ball_bboxes.map((bbox: number[]) => {
    return [bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2];
  })
  const videoElementRef = useRef<HTMLVideoElement>(null);
  let canva = useRef<HTMLCanvasElement>(null);
  console.log(videoMetadata);
  useEffect(() => {
    console.log(videoMetadata);
    const startFrame = videoMetadata.start_frame;
    const endFrame = videoMetadata.end_frame;

    if (canva) {
      canva.current.height = videoElementRef.current?.height;
      canva.current.width = videoElementRef.current?.width;
      const ballStartPosX = perfectPathCoords[startFrame][0];
      const ballStartPosY = perfectPathCoords[startFrame][1];
      const hoopStartPosX = videoMetadata.hoop_bbox[0];
      const hoopStartPosY = videoMetadata.hoop_bbox[1];

      const ratioX = videoElementRef.current?.width / (perfectPathCoords[startFrame][0] - perfectPathCoords[Math.min(endFrame, perfectPathCoords.length - 1)][0]);
      const ratioY = videoElementRef.current.height / (perfectPathCoords[startFrame][1] - perfectPathCoords[Math.min(endFrame, perfectPathCoords.length - 1)][1]);
      const context = canva.current?.getContext('2d');

      //context?.drawImage(videoElementRef.current, 0, 0, canva.current?.width, canva.current.height);
      context.strokeStyle = "red";
      context.lineWidth = 5;
      context?.beginPath();
      context?.moveTo((perfectPathCoords[startFrame][0]) * (videoElementRef.current.width / 1920), (perfectPathCoords[startFrame][1]) * (videoElementRef.current.height / 1080));
      for (let i = startFrame + 1; i <= Math.min(endFrame, perfectPathCoords.length - 1); i++) {
        const x = (perfectPathCoords[i][0]) * (videoElementRef.current.width / 1920);
        const y = (perfectPathCoords[i][1]) * (videoElementRef.current.height / 1080);


        context?.lineTo(x, y);
        context?.getLineDash
      }
      context?.stroke();

      context.strokeStyle = "green";
      context.lineWidth = 5;
      context?.beginPath();
      context?.moveTo((ballStartPosX) * (videoElementRef.current.width / 1920), (ballStartPosY) * (videoElementRef.current.height / 1080));
      let x = ballStartPosX;
      let y = ballStartPosY;
      let t = 0;
      while (y > 0 && x > 0 && x < 1920 && y < 1080) {
        const x1 = perfectPathCoords[startFrame][0] + videoMetadata.optimal_velocity * -Math.cos(videoMetadata.optimal_angle) * t
        const y1 = perfectPathCoords[startFrame][1] + videoMetadata.optimal_velocity * -Math.sin(videoMetadata.optimal_angle) * t + 0.5 * 9.81 * videoMetadata.px_per_meter * t * t
        x = x1 * (videoElementRef.current.width / 1920);
        y = y1 * (videoElementRef.current.height / 1080);
        context?.lineTo(x, y);
        context?.getLineDash;
        t += 0.01;
      }
      context?.stroke();
    }
  }, [])
  return (
    <>
      <div>
        <video ref={videoElementRef} style={{ position: "absolute" }} height={300.5} width={600} controls src={`http://localhost:8000/media/${videoMetadata.video}`}></video>
        <canvas ref={canva} style={{ overflow: 'hidden', position: 'absolute', pointerEvents: "none", left: videoElementRef.current?.getBoundingClientRect().left, top: videoElementRef.current?.getBoundingClientRect().top }}></canvas>
      </div>
      {/* <div className="h-[300.5px] relative">
        <video ref={videoElementRef} className="absolute" height={300.5} width={600} controls src={`http://localhost:8000/media/${videoMetadata.video}`}></video>
        <canvas style={{ left: videoElementRef.current?.getBoundingClientRect().left, top: videoElementRef.current?.getBoundingClientRect().top }} ref={canva} className={`hidden w-[600px] h-[300.5px] absolute`} ></canvas>
      </div> */}
    </>

  )
}
