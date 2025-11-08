'use client'
import { useEffect, useRef } from "react"
export default function VideoDisplay(video:any){
    const canva = useRef<HTMLCanvasElement>(null);
    function getPosition(e:any){
        
        if(canva.current){
            const context = canva.current.getContext("2d");
            console.log("x: " + (e.clientX - canva.current.offsetLeft));
            console.log("y: " + (e.clientY - canva.current.getBoundingClientRect().top));
            context.fillStyle = "blue";
            context.fillRect(e.clientX - canva.current.offsetLeft, e.clientY - canva.current.getBoundingClientRect().top, 5, 5)
        }
    }
    useEffect(()=>{
        if (canva.current) {
            const context = canva.current.getContext("2d");
            context.fillStyle = "red";
            context?.fillRect(0,0, canva.current.width, canva.current.height)
            console.log(canva.current)
        }

    },[])

    return(
        <canvas height='400' width='400' ref = {canva} onClick={(event)=>{getPosition(event)}}>

        </canvas>
    )
    
    
}