import Link from 'next/link'

import NaviBar from "./components/navbar";
import Offerings from "./components/ourofferings";



export default function Home() {
  return (
    <div className = "min-h-screen flex items-center justify-center bg-gray-50 bg-cover bg-no-repeat" style = {
      { backgroundImage: `url("./health.png")` , backgroundSize: 'contain'}}>

      <div className = "max-w-4xl mx-auto px-4">
        <div className = "text-center mb-8">
            <NaviBar />
        </div>
        <div className = "max-w-4xl mx-auto px-4">
          <div className = "flex flex-grow-1 mb-8">
            <Offerings />
          </div>
        </div>
        <p className = "text-center text-green-600 mb-8">
          Welcome to the Agro Watcher. Click below to monitor your farms.
        </p>
        <div className = "text-center mb-8">
          <Link href = "/map" className = "bg-green-500 hover:bg-yellow-400 text-white font-bold py-2 px-4 rounded">
              Go to Watcher
          </Link>
        </div>
      </div>
    </div>
  );
}