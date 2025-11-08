import Image from "next/image";
import Link from "next/link";

export default async function Home() {
  let response = await fetch('http://localhost:8000/api/all', {
    method: "GET",
  })
  let allVideos = await response.json()
  // if the user has some videos
  if (allVideos) {
    return (
      <div className="grid grid-rows-2 grid-cols-2 gap-4 p-4">
        {allVideos.map((video) => (
          <Link key={`${video.id}`} className="flex flex-col rounded" href={`/video/${video.id}`}>
            <img src={`http://localhost:8000/media/${video.thumbnail}`} alt="" />
            <div className="bg-background-50">
              <p>{video.video}</p>
            </div>
          </Link>
        ))}
      </div>
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
