'use client'

import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { useState, useRef } from 'react'
import Video from "../Video/page"

export default function UploadFileButton() {
    const dummyFile = new File(["foo"], "foo.mp4", {
        type: "video/*",
    });
    const [currentFile, setFile] = useState(dummyFile);
    const [open, setOpen] = useState(false);
    const [ballPosition, setBallPosition] = useState({ x: 0, y: 0 });
    const [hoopPosition, setHoopPosition] = useState({ x: 0, y: 0 });
    const [selecting, setSelecting] = useState("");
    const videoElementRef = useRef(null);

    function handleFile(event: React.ChangeEvent<HTMLInputElement>) {
        // event.target.files will have type FileList[File]
        setFile(event.target.files[0]); // fix event.target.files' is possibly 'null' later
        setOpen(true);
    }
    async function submitFile() {
        const formData = new FormData();
        formData.append('video', currentFile);
        formData.append('ball_x', JSON.stringify(ballPosition.x));
        formData.append('ball_y', JSON.stringify(ballPosition.y));
        formData.append('hoop_x', JSON.stringify(hoopPosition.x));
        formData.append('hoop_y', JSON.stringify(hoopPosition.y));
        // formData.append('ball_x', JSON.stringify(1315));
        // formData.append('ball_y', JSON.stringify(633));
        // formData.append('hoop_x', JSON.stringify(396));
        // formData.append('hoop_y', JSON.stringify(207));
        formData.append('start_frame', JSON.stringify(45));
        let response = await fetch('http://localhost:8000/api/track', {
            method: "POST",
            body: formData
        })
    }

    function handleClick(event) {
        const posData = {
            x: Math.floor((event.clientX - videoElementRef.current.getBoundingClientRect().x) * 1920 / 462),
            y: Math.floor((event.clientY - videoElementRef.current.getBoundingClientRect().y) * 1080 / 260),
        }
        if (selecting === "ball") {
            setBallPosition(posData)
            setSelecting("")
        }
        else if (selecting === "hoop") {
            setHoopPosition(posData)
            setSelecting("")
        }
        else {
        }
    }

    return (
        <>
            <input onChange={handleFile} type="file" id="video" accept="video/*" name="" hidden />
            <label htmlFor="video" className="w-full">
                <div className="h-10 cursor-pointer flex items-center flex-row px-2 gap-2 py-1 bg-primary text-on-primary rounded ">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M5 20h14q.425 0 .713.288T20 21t-.288.713T19 22H5q-.425 0-.712-.288T4 21t.288-.712T5 20m5-2q-.425 0-.712-.288T9 17v-6H7.05q-.625 0-.9-.562t.1-1.063l4.95-6.35q.15-.2.363-.3t.437-.1t.438.1t.362.3l4.95 6.35q.375.5.1 1.063t-.9.562H15v6q0 .425-.288.713T14 18z" />
                    </svg>
                    {/* <button onClick={() => { console.log(open) }}>am i open</button> */}
                    <p className="max-w-md text-md font-medium leading-8 truncate"> Upload a video for analysis
                    </p>
                </div>
            </label>
            <Dialog open={open} onOpenChange={setOpen}>
                <div className="w-screen h-fit">
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Video Processing</DialogTitle>
                            <DialogDescription>
                                Click on the ball and the hoop with your mouse.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="w-full">
                            <div className="h-[260px] relative">
                                <video ref={videoElementRef} width={462} height={260} className="absolute" controls preload="none">
                                    <source src={URL.createObjectURL(currentFile)} type="video/mp4" />
                                    Your browser does not support the video tag.
                                </video>
                                <canvas className={`w-[462px] h-[260px] absolute bg-amber-300 opacity-10 ${(selecting === 'ball' || selecting === 'hoop') ? "" : "hidden"}`} onClick={handleClick}></canvas>
                            </div>
                            {/* <button onClick={() => {console.log(videoElementRef.current.videoWidth)}}>how big am i</button>
                            <button onClick={() => {console.log(videoElementRef.current.getBoundingClientRect())}}>where am i </button> */}
                            <div className="flex flex-row items-center justify-between">
                                <Button variant="outline" onClick={() => { setSelecting('ball') }}>Select ball position</Button>
                                <div className="flex flex-row gap-4">
                                    <p>X: {ballPosition.x}</p>
                                    <p>Y: {ballPosition.y}</p>
                                </div>
                            </div>
                            <div className="flex flex-row items-center justify-between">
                                <Button variant="outline" onClick={() => { setSelecting('hoop') }}>Select hoop position</Button>
                                <div className="flex flex-row gap-4">
                                    <p>X: {hoopPosition.x}</p>
                                    <p>Y: {hoopPosition.y}</p>
                                </div>
                            </div>
                        </div>
                        <DialogFooter className="flex flex-row justify-end">
                            <Button variant="outline">Reset</Button>
                            <Button type="submit" aria-label="Submit" onClick={submitFile}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                    <path fill="currentColor" d="M5 20h14q.425 0 .713.288T20 21t-.288.713T19 22H5q-.425 0-.712-.288T4 21t.288-.712T5 20m5-2q-.425 0-.712-.288T9 17v-6H7.05q-.625 0-.9-.562t.1-1.063l4.95-6.35q.15-.2.363-.3t.437-.1t.438.1t.362.3l4.95 6.35q.375.5.1 1.063t-.9.562H15v6q0 .425-.288.713T14 18z" />
                                </svg>
                                Upload Video
                            </Button>
                        </DialogFooter>
                    </DialogContent>

                </div>
            </Dialog>
        </>
    )
}