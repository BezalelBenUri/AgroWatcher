"use client"

import {useEffect, useState} from "react";
import { MapContainer, TileLayer, GeoJSON, Popup} from "react-leaflet";
import { Alert, Spinner } from "react-bootstrap";

import "leaflet/dist/leaflet.css"

import useSWR from "swr";

import axios from "axios";

const url = "http://127.0.0.1:8000/api/v1/farms/";

const fetcher = (url) => axios.get(url).then((res) => res.data);
//const fetcher = (...args) => fetch(...args).then((res) => res.json());
  

const Map = () => {
    const { data, error } = useSWR(url, fetcher);

    console.log(data);

    if (error) {
        return <Alert variant = "danger">Failed to load data!</Alert>;
    }
    if (!data) {
        return (
        <Spinner
            animation = "border"
            variant = "danger"
            role = "status"
            className = "w-48 h-48 mx-auto block"
            >
                <span className = "sr-only">Loading...</span>
        </Spinner>
        );
    }

    const features = data?.features;

    const onEachFeature = (feature, layer) => {
        const popupContent = `
        <div>
            <h6>${feature.properties.name}</h6>
            <p>Size: ${feature.properties.size}</p>
            <p>Crop: ${feature.properties.crop}</p>
        </div>
    `;
    layer.bindPopup(popupContent);
    };

    return (
        <MapContainer center = {[12.71671, 4.50154]} zoom = {10} style = {{height: "95vh"}}>
            <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {features && (
                <GeoJSON data = {features} style = {{color: "green"}} onEachFeature = {onEachFeature}></GeoJSON>
            )}
        </MapContainer>
    )
}

export default Map;