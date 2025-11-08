'use client'
import { useState, useRef, RefObject, useEffect } from "react";
import VideoDisplay from "./VideoDisplay";
export default function VideoScreen(){
    let vid = useRef(null);
    let [vidTime, setVidTime] = useState("");
    function changeFrame(event:any){
      setVidTime(`${event.target.time}`);
    }
    useEffect(()=>{
        console.log("vidTime");
    },[vidTime])
    return(
        <>
                <VideoDisplay ></VideoDisplay>
        </>
        
        
    )
}