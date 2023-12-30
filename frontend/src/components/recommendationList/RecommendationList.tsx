import { Button, Card } from "react-bootstrap";
import { useState } from "react";
import "./RecommendationList.scss";
import { responseBody } from "../../models/predict";
import RecommendationDetail from "../recommendationDetail/RecommendationDetail";
interface Props {
    recommendations: responseBody[] | null;   
}
const RecommendationList = (props: Props) => {
    const { recommendations } = props;

    const [showRecommendationDetail, setShowRecommendationDetail] = useState<boolean>(true);
    const [selectedRecommendation, setSelectedRecommendation] = useState<responseBody | null>(null);

    const handleCardClick = (recommendation: responseBody) => {
        setSelectedRecommendation(recommendation);
        setShowRecommendationDetail(true);
    }
    return (
        <>
        {showRecommendationDetail && selectedRecommendation && (
            <RecommendationDetail show={showRecommendationDetail} onHide={() => setShowRecommendationDetail(!showRecommendationDetail)} recommendation={selectedRecommendation} />
        )}

        <div className="recommendation-list">
            <div className="d-flex justify-content-between recommendation-list-header">
            <h3>Recommendations</h3>
            {recommendations && recommendations.length > 0 && (
                <Button variant="outline-success">Copy to BibTex</Button>
            )}
            </div>
            {recommendations && recommendations.length > 0 ? (
                <div className="recommendation-list-inner p-3">
                        {recommendations.map((recommendation, index) => (
                            <a key={index}  onClick={() => handleCardClick(recommendation)}>
                            <Card key={index} className="mb-4 recommendation-item">
                                <Card.Body>
                                    <Card.Title className="mb-3">{recommendation.title}</Card.Title>
                                    <Card.Subtitle className="mb-2 text-muted">{recommendation.authors}</Card.Subtitle>
                                    <Card.Text>Matching: {recommendation.score}</Card.Text>
                                    <Card.Link href={recommendation.doi}>DOI</Card.Link>
                                </Card.Body>
                            </Card>
                            </a>
                        ))}
                    </div>
            ) : (
                <h4 className="d-flex justify-content-center">No Recommendations yet</h4>
            )}
        </div>
        </>
    )

};

export default RecommendationList;