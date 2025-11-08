import Image from "next/image";

export default async function Home() {
  let response = await fetch('http://localhost:8000/api/all', {
    method: "GET",
  })
  let allVideos = await response.json()
  let allThumbnails = [];
  for (const video of allVideos) {
    let thumbnail = await fetch(`http://localhost:8000/api/thumbnail/${video.id}`, {
      method: "GET",
    })
    allThumbnails.push(thumbnail);
  }
  return (
    <div className="h-full rounded flex items-center justify-center">
      <main className="rounded flex w-full h-full flex-col items-center justify-center">
        {/* <p className="text-xl max-w-md text-center font-medium">
          You don't have any videos in the database. Upload a video to get started.
        </p> */}
        <ul>
{allThumbnails.map((thumbnail) => (
            <p>{JSON.stringify(thumbnail)}</p>
          ))}
          {/* {allVideos.map((video) => (
            <p>{`${video.id}`}</p>
          ))} */}
        </ul>
      </main>
    </div>
  );
}
