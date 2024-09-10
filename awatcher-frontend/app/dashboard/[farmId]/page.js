"use client"


import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Spinner from 'react-bootstrap/Spinner';

import {Line} from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard = () => {
    const {farmId} = useParams();
    const [farmData, setFarmData] = useState(null);
    const [loading, setLoading] = useState(true);

    const [timeSeriesData, setTimeSeriesData] = useState({dates: [], ndvi: [], ndmi: [], ndwi: [] });

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

            //Fetch time series data
        axios.get(`http://127.0.0.1:8000/api/v1/farms/${farmId}/time_series/`)
            .then(response => {
                const timeSeries = response.data.time_series;

                // Extracting the time series data
                const dates = timeSeries.map(entry => new Date(entry.date).toLocaleDateString());
                const ndvi = timeSeries.map(entry => entry.NDVI);
                const ndmi = timeSeries.map(entry => entry.NDMI);
                const ndwi = timeSeries.map(entry => entry.NDWI);

                setTimeSeriesData({dates, ndvi, ndmi, ndwi});
            })
            .catch(error => {
                console.error("error fetching indices data:", error);
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

    // Setup data for the chart
    const chartData = {
        labels: timeSeriesData.dates, // Dates from the time series data
        datasets: [
            {
                label: "NDVI",
                data: timeSeriesData.ndvi,
                borderColor: "green",
                fill: false,
            },
            {
                label: "NDMI",
                data: timeSeriesData.ndmi,
                borderColor: "blue",
                fill: false,
            },
            {
                label: "NDWI",
                data: timeSeriesData.ndwi,
                borderColor: "cyan",
                fill: false,
            },
        ]
    }

    return (
        <Container className = "my-8">
            <h1 className = "text-3xl font-bold text-center mb-8">{farmData.name}</h1>

            {/* Farm details and satellite images */}
            <Row className = "mb-8">
                <Col md = {6}>
                    <Card className = "shadow-lg">
                        <Card.Body className = "p-6">
                            <Card.Title className = "text-xl font-semibold text-gray-700">Farm Details</Card.Title>
                            <Card.Text className = "mt-4 text-gray-600">
                                <span className = "font-bold">Size:</span> {farmData.size} Hectares</Card.Text>
                            <Card.Text className = "text-gray-600">
                                <span className = "font-bold">Crop:</span> {farmData.crop}
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md = {6}>
                    <Card className = "shadow-lg">
                        <Card.Body className = "p-6">
                            <Card.Title className = "text-xl font-semibold text-gray-700">Satellite Image</Card.Title>
                            <Card.Img 
                                src = {`http://127.0.0.1:8000/${farmData.image_path}`}
                                alt = "satellite Image"
                                className = "rounded-lg mt-4"/>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            {/* Index Images */}
            <Row className = "mb-8">
                <Col md = {4}>
                    <Card className = "shadow-lg">
                        <Card.Body className = "p-6">
                            <Card.Title className="text-x1 font-semibold text-gray-700">NDVI Image</Card.Title>
                            <Card.Img
                                src = {`http://127.0.0.1:8000/${farmData.ndvi_path}`}
                                alt = "NDVI Image"
                                className = "rounded-lg mt-4"/>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md = {4}>
                    <Card className = "shadow-lg">
                        <Card.Body className = "p-6">
                            <Card.Title className = "text-xl font-semibold text-gray-700">NDMI Image</Card.Title>
                            <Card.Img
                                src = {`http://127.0.0.1:8000/${farmData.ndmi_path}`}
                                alt = "NDMI Image"
                                className = "rounded-lg mt-4"/>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md = {4}>
                    <Card className = "mb-4">
                        <Card.Body>
                            <Card.Title className = "text-xl font-semibold text-gray-700">NDWI Image</Card.Title>
                            <Card.Img
                                src = {`http://127.0.0.1:8000/${farmData.ndwi_path}`}
                                alt = "NDWI Image"
                                className = "rounded-lg mt-4"/>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            {/* Indices Time Series */}
            <Row className = "mb-8">
                <Col md = {12}>
                    <Card className = "shadow-lg">
                        <Card.Body className = "p-6">
                            <Card.Title className = "text-xl font-semibold text-gray-700">Indices Over Time</Card.Title>
                            <Line data = {chartData} />
                            <div className = "mt-4">
                                <p className = "text-gray-600">
                                Time series chart for NDVI, NDMI, NDWI indices.
                                </p>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

        </Container>
    )

}

export default Dashboard;