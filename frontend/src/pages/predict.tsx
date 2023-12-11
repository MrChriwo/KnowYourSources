import AbstractFrame from "../components/abstractFrame/AbstractFrame";
import RecommendationList from "../components/recommendationList/RecommendationList";
import {Row, Col} from "react-bootstrap";

const Predict = () => {
    return (
        <div className="page">
        <h1 className="mb-4">Find the best papers for your work</h1>
        <Row>
            <Col md={8}>
                <AbstractFrame/>
            </Col>
            <Col md={4} className="p-0">
                <RecommendationList abstract="lorem ipsum"/>
            </Col>
        </Row>
        </div>
    );
};

export default Predict;