'use client'
import { RefObject, useEffect, useRef, useState } from "react"
export default function VideoDisplay(){
    const canva = useRef<HTMLCanvasElement>(null);
    let vid = useRef(null);
    let [vidTime, setVidTime] = useState("");
    
    function changeFrame(event:any){
        console.log("vidTime");
        setVidTime(`${event.target.currentTime}`);
    }
    
    function getPosition(e:any){
        if(canva.current){
            const context = canva.current.getContext("2d");
            console.log("x: " + (e.clientX - canva.current.offsetLeft));
            console.log("y: " + (e.clientY - canva.current.getBoundingClientRect().top));
            context.fillStyle = "red";
            context.fillRect(e.clientX - canva.current.offsetLeft, e.clientY - canva.current.getBoundingClientRect().top, 19, 19)
        }
    }
    
    useEffect(()=>{
        if (canva.current) {
                if(vid){
                    const context = canva.current.getContext("2d");
                    canva.current.height = 1020;
                    canva.current.width = 1920;
                    context.fillStyle = "red";
                    context.fillRect(0,0,200,200);
                    context.drawImage(vid.current, 0, 0);

               
                
            
            }
            

        }
        

    },[vidTime])

    return(
        <>
            
            <video width = "1280" height = "720" controls src="/medias/test_ibblGVd.mp4" ref= {vid} onTimeUpdate={(e)=>{changeFrame(e as any)}} ></video>
            if(vid && vid.current){
                <canvas width= {720} height = {1080} ref = {canva} onClick={(event)=>{getPosition(event)}}>
             </canvas>
            }
            
            
        </>
        
    )
    
    
}