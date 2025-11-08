import Image from "next/image";

export default function Home() {
  return (
    <div className="h-full rounded flex items-center justify-center">
      <main className="rounded flex w-full h-full flex-col items-center justify-center">
        <p className="text-xl max-w-md text-center font-medium">
          You don't have any videos in the database. Upload a video to get started.
        </p>
      </main>
    </div>
  );
}
