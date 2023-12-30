import { useState } from "react";
import AbstractFrame from "../components/abstractFrame/AbstractFrame";
import RecommendationList from "../components/recommendationList/RecommendationList";
import {Row, Col} from "react-bootstrap";
import { responseBody } from "../models/predict";

const Predict = () => {
    const [response, setResponse] = useState<responseBody[] | null>(null);

    return (
        <div className="page">
        <h1 className="mb-4">Find the best papers for your work</h1>
        <Row>
            <Col md={8}>
                <AbstractFrame setResponse={setResponse}/>
            </Col>
            <Col md={4} className="p-0">
                <RecommendationList recommendations={response}/>
            </Col>
        </Row>
        </div>
    );
};

export default Predict;