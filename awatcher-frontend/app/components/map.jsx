"use client"

import {useEffect, useState} from "react";
import { MapContainer, TileLayer, GeoJSON, Popup, useMap} from "react-leaflet";
import {Spinner} from "@nextui-org/react";

import { Alert } from "react-bootstrap";

import "leaflet/dist/leaflet.css"

import useSWR from "swr";

import axios from "axios";

const url = "http://127.0.0.1:8000/api/v1/farms/";

const fetcher = (url) => axios.get(url).then((res) => res.data);
//const fetcher = (...args) => fetch(...args).then((res) => res.json());
const CenterMap = ({coords}) => {
    const map = useMap();
    map.setView(coords, map.getZoom());
    return null;
}
  

const Map = () => {
    const { data, error } = useSWR(url, fetcher);
    const [selectedFarm, setSelectedFarm] = useState(null);
    const [imagePath, setImagePath] = useState(null);
    const [center, setCenter] = useState([12.71671, 4.50154]);
    const [loading, setLoading] = useState(false);

    console.log(data);

    const fetchImage = async (farmId) => {
        setLoading(true);
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/farms/${farmId}/download_image/`);
            setImagePath(response.data.image_path);
        } catch (error) {
            console.error("Error fetching image:", error);
        } finally {
            setLoading(false);
        }
      };

    

    const onEachFeature = (feature, layer) => {
        layer.on({
            click: () => {
                const coordinates = feature.geometry.coordinates[0][0];
                const latLng = [coordinates[0][1], coordinates[0][0]];
                setSelectedFarm(feature);
                setCenter(latLng);
                fetchImage(feature.id);
            },
        });
    };

    if (error) {
        return <Alert variant = "danger">Failed to load data!</Alert>;
    }
    if (!data) {
        return (
            <Spinner
            label = "Warning" size = "md" color = "secondary"
        />
        );
    }

    

    const features = data?.features;

    return (
        <MapContainer center = {[12.71671, 4.50154]} zoom = {10} style = {{height: "95vh"}}>
            <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {features && (
                <GeoJSON data = {features} style = {{color: "green"}} onEachFeature = {onEachFeature}></GeoJSON>
            )}
            {selectedFarm && (
                <Popup position = {
                    [
                    selectedFarm.geometry.coordinates[0][0][0][1],
                    selectedFarm.geometry.coordinates[0][0][0][0],
                ]}
                onClose = {() => {
                    setSelectedFarm(null);
                    setImagePath(null);
                }}
                >
                    <div className = "w-auto max-w-md">
                        <h6 className = "font-bold text-lg mb-2">{selectedFarm.properties.name}</h6>
                        <p className = "mb-1">Size: {selectedFarm.properties.size}</p>
                        <p className = "mb-1">Crop: {selectedFarm.properties.crop}</p>
                        {loading ? (
                            <Spinner label = "Loading" size = "lg" color = "secondary"  />
                        ) : (
                        imagePath && (
                            <img src = {`http://127.0.0.1:8000/${imagePath}`} 
                            alt = "Satellite Image of Farm" 
                            width = {500} height = {500} 
                            className = "h-auto max-w-lg"/>
                        )
                        )}
                    </div>
                </Popup>
            )}
            {selectedFarm && <CenterMap coords = {center} />}
        </MapContainer>
    )
}

export default Map;