"use client"

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import Spinner from 'react-bootstrap/Spinner';

const Dashboard = () => {
    const {farmId} = useParams();
    const [farmData, setFarmData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (farmId) {
            console.log(`Fetching data for farmId: ${farmId}`);
            axios.get(`http://127.0.0.1:8000/api/v1/farms/${farmId}/`)
            .then(response => {
                console.log("Response data:", response.data);
                setFarmData(response.data.properties);
            })
            .catch(error => {
                console.error("Error fetching farm data:", error);
            })
            .finally(() => {
                setLoading(false);
            });
        }
    }, [farmId]);

    if (loading) {
        return <Spinner animation = "border" role = "status">
                <span className = "visually-hidden">Loading...</span>
            </Spinner>
    }

    if (!farmData) {
        return <div> Error Loading farm data</div>
    }

    return (
        <div>
            <h1>{farmData.name}</h1>
            <p>Size: {farmData.size}</p>
            <p>Crop: {farmData.crop}</p>
            <div>
                <h2>Satellite Image</h2>
                <img src = {`http://127.0.0.1:8000/${farmData.image_path}`} alt = "Satellite Image"/>
            </div>
            <div>
                <h2>NDVI Image</h2>
                <img src = {`http://127.0.0.1:8000/${farmData.ndvi_path}`} alt = "NDVI Image"/>
            </div>
            <div>
                <h2>NDMI Image</h2>
                <img src = {`http://127.0.0.1:8000/${farmData.ndmi_path}`} alt = "NDMI Image"/>
            </div>
            <div>
                <h2>NDWI Image</h2>
                <img src = {`http://127.0.0.1:8000/${farmData.ndwi_path}`} alt = "NDWI Image"/>
            </div>
        </div>
    )

}

export default Dashboard;