'use client'
import { RefObject, useEffect, useRef, useState } from "react"
export default function VideoDisplay({videoFile, set_ball_x, set_ball_y, set_hoop_x, set_hoop_y}:{videoFile:File, set_ball_x: Function, set_ball_y: Function, set_hoop_x:Function, set_hoop_y:Function}){
    const canva = useRef<HTMLCanvasElement>(null);
    let vid = useRef(null);
    let [vidTime, setVidTime] = useState("");
    const [count, setCount] = useState(0);
    
    function changeFrame(event:any){
        console.log("vidTime");
        setVidTime(`${event.target.currentTime}`);
    }
    
    function getPosition(e:MouseEvent){
        if(canva.current){
            console.log(canva.current.offsetLeft);
            const context = canva.current.getContext("2d");
            const canvasX = e.clientX - canva.current.getBoundingClientRect().left;
            const canvasY = e.clientY - canva.current.getBoundingClientRect().top;
            //only allow ability to fill color when all 4 var go from null to something
            //check b-ball left
            //check ball right
            //check hoop left
            //check hoop right
            //check time 
            if(count < 2){
                switch(count){
                case 0:
                    set_ball_x(canvasX);
                    set_ball_y(canvasY);
                    console.log("ball_y" + canvasY);
                    console.log("ball_x" + canvasX);
                    break;
                case 1:
                    set_hoop_x(canvasX);
                    set_hoop_y(canvasY);
                    console.log("hoop_y" + canvasY);
                    console.log("hoop_x" + canvasX);
                    break;
                }
                
                context.fillStyle = "red";
                context.fillRect(canvasX, canvasY, 5, 5)
                setCount( count + 1);
            }
             
        }
    }
    
    useEffect(()=>{
        if (canva.current) {
                if(vid){
                    const context = canva.current.getContext("2d");
                    context.fillStyle = "gray";
                    context.fillRect(0,0,320,210);
                    context.drawImage(vid.current, 0, 0, canva.current.width, canva.current.height);

               
                
            
            }
            

        }
        

    },[vidTime])

    return(
            <div className="absolute">
            <video width = "320" height = "220" controls src="/medias/test_ibblGVd.mp4" ref= {vid} onTimeUpdate={(e)=>{changeFrame(e as any)}} ></video>
            <canvas width= {300} height = {220} ref = {canva} onClick={(event)=>{getPosition(event)}}></canvas>
            </div>
    )
    
    
}