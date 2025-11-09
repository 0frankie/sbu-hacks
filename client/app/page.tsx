import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import DeleteVideoButton from "@/components/ui/deletevideobutton";

export default async function Home() {
  const fetchVideos = async () => {
    let response = await fetch('http://localhost:8000/api/all', {
      method: "GET",
    })
    return await response.json()
  }
  const allVideos = await fetchVideos()
  // const [allVideos, setAllVideos] = useState(await fetchVideos());

  // const refreshVideos = async () => {
  //   setAllVideos(await fetchVideos());
  // }

  // if the user has some videos
  if (allVideos) {
    return (
      <div className="grid grid-rows-2 grid-cols-2 gap-4 p-4">
        {allVideos.map((video) => (
          <div key={`${video.id}`} className="flex flex-col bg-background-50 rounded">
            <div className="flex justify-end">
              <DeleteVideoButton id={video.id} refreshFn={refreshVideos} />
            </div>
            <Link href={`/video/${video.id}`}>
              <img className="rounded" src={`http://localhost:8000/media/${video.thumbnail}`} alt="" />
              <div className="px-2 py-2">
                <p>{video.video}</p>
              </div>
            </Link>
          </div>
        ))
        }
      </div >
    );
  }
  return (
    <div className="h-full rounded flex items-center justify-center">
      <main className="rounded flex w-full h-full flex-col items-center justify-center">
        <p className={`text-xl max-w-md text-center font-medium ${allVideos ? "hidden" : ""}`}>
          You don't have any videos in the database. Upload a video to get started.
        </p>
      </main>
    </div>
  );


}
