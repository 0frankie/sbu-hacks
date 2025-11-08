'use client'
import {useState, useRef, useEffect} from "react";
export default function Test(){
    let r = useRef<HTMLCanvasElement>(null);
    let v = useRef<HTMLVideoElement>(null);
    let [cTime, setCTime] = useState("");
    function resetFrame(event:any){
        setCTime(`${event.target.currentTime}`);
        console.log("set");
    }
    useEffect(()=>{
        if(r){
            let context = r.current?.getContext("2d");
            r.current.height = '10800';
            r.current.width = '1980';
            if(v){
                console.log(v);
             context.drawImage(v.current, 0, 0, 100, 100);
            }
        }
    }, [cTime])
    return(
        <>
              <video ref = {v} src="/medias/test_ibblGVd.mp4" controls onTimeUpdate={(e)=>{resetFrame(e)}}></video>
              <canvas ref={r} ></canvas>
        </>
      
    )
}