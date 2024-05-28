"use client"


import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
// import LineChart from './LineChart';
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
        <Container>
            <h1 className = "my-4">{farmData.name}</h1>
            <Row>
                <Col md = {6}>
                    <Card className = "mb-6">
                        <Card.Body>
                            <Card.Title>Farm Details</Card.Title>
                            <Card.Text>Size: {farmData.size}</Card.Text>
                            <Card.Text>Crop: {farmData.crop}</Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md = {6}>
                    <Card className = "mb-4">
                        <Card.Body>
                            <Card.Title>Satellite Image</Card.Title>
                            <Card.Img src = {`http://127.0.0.1:8000/${farmData.image_path}`}/>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            <Row>
                <Col md = {6}>
                    <Card className = "mb-4">
                        <Card.Body>
                            <Card.Title>NDVI Image</Card.Title>
                            <Card.Img src = {`http://127.0.0.1:8000/${farmData.ndvi_path}`} />
                        </Card.Body>
                    </Card>
                </Col>
                <Col md = {6}>
                    <Card className = "mb-4">
                        <Card.Body>
                            <Card.Title>NDMI Image</Card.Title>
                            <Card.Img src = {`http://127.0.0.1:8000/${farmData.ndmi_path}`}/>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            <Row>
                <Col md={6}>
                    <Card className="mb-4">
                        <Card.Body>
                            <Card.Title>NDWI Image</Card.Title>
                            <img src={`http://127.0.0.1:8000/${farmData.ndwi_path}`} alt="NDWI Image" className="img-fluid" />
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={6}>
                    <Card className="mb-4">
                        <Card.Body>
                            <Card.Title>Indices Over Time</Card.Title>
                            {/* <LineChart data={farmData.indicesOverTime} /> Assume you have this data */}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            {/* <div>
                <h2>NDMI Image</h2>
                <img src = {`http://127.0.0.1:8000/${farmData.ndmi_path}`} alt = "NDMI Image"/>
            </div>
            <div>
                <h2>NDWI Image</h2>
                <img src = {`http://127.0.0.1:8000/${farmData.ndwi_path}`} alt = "NDWI Image"/>
            </div> */}
        </Container>
    )

}

export default Dashboard;