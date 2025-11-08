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
    DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState } from 'react'

export default function UploadFileButton() {
    const dummyFile = new File(["foo"], "foo.txt", {
        type: "text/plain",
    });
    const [currentFile, setFile] = useState(dummyFile)
    const [open, setOpen] = useState(false);

    function handleFile(event: React.ChangeEvent<HTMLInputElement>) {
        // event.target.files will have type FileList[File]
        setFile(event.target.files[0]); // fix event.target.files' is possibly 'null' later
        setOpen(true);
    }
    return (
        <>
            <input onChange={handleFile} type="file" id="files" accept="video/*" name="" hidden />
            <label htmlFor="files" className="w-full">
                <div className="h-10 cursor-pointer flex items-center flex-row px-2 gap-2 py-1 bg-primary text-on-primary rounded ">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M5 20h14q.425 0 .713.288T20 21t-.288.713T19 22H5q-.425 0-.712-.288T4 21t.288-.712T5 20m5-2q-.425 0-.712-.288T9 17v-6H7.05q-.625 0-.9-.562t.1-1.063l4.95-6.35q.15-.2.363-.3t.437-.1t.438.1t.362.3l4.95 6.35q.375.5.1 1.063t-.9.562H15v6q0 .425-.288.713T14 18z" />
                    </svg>
                    <button onClick={() => {console.log(open)}}>am i open</button>
                    <p className="max-w-md text-md font-medium leading-8 truncate"> Upload a video for analysis
                    </p>
                </div>
            </label>
            <Dialog open={open} onOpenChange={setOpen}>
                <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                        <DialogTitle>Video Processing</DialogTitle>
                        <DialogDescription>
                            Click on the ball and the hoop with your mouse. 
                        </DialogDescription>
                    </DialogHeader>
                    <div className="size-64 bg-neutral-300">
                    </div>
                    <DialogFooter className="flex flex-row">
                        {/* <DialogClose asChild>
                            <Button variant="outline">Reset</Button>
                        </DialogClose> */}
                        <Button variant="outline">Reset</Button>
                        <Button className="" type="submit">Upload Video</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </>
    )
}