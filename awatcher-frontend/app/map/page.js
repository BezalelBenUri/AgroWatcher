import dynamic from "next/dynamic";

const Map = dynamic(() => import("../components/map"), { ssr: false });

const mapper = () => {
  return (
    <div>
      <h1>Agro Watcher</h1>
      <Map />
    </div>
  );
}

export default mapper