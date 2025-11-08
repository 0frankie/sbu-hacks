'use client'
import { RefObject, useEffect, useRef, useState } from "react"
export default function VideoDisplay({video, set_ball_x, set_ball_y, set_hoop_x, set_hoop_y}:{vid:File, set_ball_x: Function, set_ball_y: Function, set_hoop_x:Function, set_hoop_y:Function}){
    const canva = useRef<HTMLCanvasElement>(null);
    let vid = useRef(null);
    let [vidTime, setVidTime] = useState("");
    const [count, setCount] = useState(0);
    
    function changeFrame(event:any){
        console.log("vidTime");
        setVidTime(`${event.target.currentTime}`);
    }
    
    function getPosition(e:any){
        if(canva.current){
            const context = canva.current.getContext("2d");
            const canvasX = e.clientX - canva.current.offsetLeft;
            const canvasY = e.clientY - canva.current.getBoundingClientRect().top;
            //only allow ability to fill color when all 4 var go from null to something
            //check b-ball left
            //check ball right
            //check hoop left
            //check hoop right
            //check time 
            switch(count){
                case 0:
                    set_ball_x(canvasX);
                    console.log("ball x: " + canvasX);
                    break;
                case 1:
                    set_ball_y(canvasY);
                    console.log("ball_y" + canvasY);
                    break;
                case 2:
                    set_hoop_x(canvasX);
                    break;
                case 3:
                    set_hoop_y(canvasY);
                    break;
            }

            context.fillStyle = "red";
            context.fillRect(e.clientX - canva.current.offsetLeft, e.clientY - canva.current.getBoundingClientRect().top, 25, 25)
            setCount( count + 1);
        }
    }
    
    useEffect(()=>{
        if (canva.current) {
                if(vid){
                    const context = canva.current.getContext("2d");
                    canva.current.height = 720;
                    canva.current.width = 1020;
                    context.fillStyle = "gray";
                    context.fillRect(0,0,320,210);
                    context.drawImage(vid.current, 0, 0, 300, 220);

               
                
            
            }
            

        }
        

    },[vidTime])

    return(
        <>
            
            <video width = "320" height = "220" controls src="/medias/test_ibblGVd.mp4" ref= {vid} onTimeUpdate={(e)=>{changeFrame(e as any)}} ></video>
            <canvas width= {720} height = {1020} ref = {canva} onClick={(event)=>{getPosition(event)}}></canvas>
            
            
            
        </>
        
    )
    
    
}