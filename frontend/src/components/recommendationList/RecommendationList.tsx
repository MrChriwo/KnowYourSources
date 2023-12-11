import { useEffect, useState} from "react";
import { Button, Card } from "react-bootstrap";
import "./RecommendationList.scss";


interface Props {
    abstract: string;    
}
const RecommendationList = (props: Props) => {
    const { abstract } = props;
    const [recommendations, setRecommendations] = useState<{"title": string, "author": string, "doi": string}[]>([]); // TODO: Change to Recommendation type


    useEffect(() => {
        // Make API call to get recommendations
        // create a sample array of recommendations
        const sampleRecommendations = [
            {
                "title": "The title of the first recommendation",
                "author": "The author of the first recommendation",
                "doi": "The doi of the first recommendation"
            },
            {
                "title": "The title of the second recommendation",
                "author": "The author of the second recommendation",
                "doi": "The doi of the second recommendation"
            },
            {
                "title": "The title of the third recommendation",
                "author": "The author of the third recommendation",
                "doi": "The doi of the third recommendation"
            },
            {
                "title": "The title of the third recommendation",
                "author": "The author of the third recommendation",
                "doi": "The doi of the third recommendation"
            }
        ];
        setRecommendations(sampleRecommendations);
    }, [abstract]);

    return (
        <div className="recommendation-list">
            <div className="d-flex justify-content-between recommendation-list-header">
            <h3>Recommendations</h3>
            {recommendations.length > 0 && (
                <Button variant="outline-success">Copy to BibTex</Button>
            )}
            </div>
            {recommendations.length > 0 ? (
                <div className="recommendation-list-inner p-3">
                        {recommendations.map((recommendation, index) => (
                            <Card key={index} className="mb-4 recommendation-item">
                                <Card.Body>
                                    <Card.Title className="mb-3">{recommendation.title}</Card.Title>
                                    <Card.Subtitle className="mb-2 text-muted">{recommendation.author}</Card.Subtitle>
                                    <Card.Link href={recommendation.doi}>DOI</Card.Link>
                                </Card.Body>
                            </Card>
                        ))}
                    </div>
            ) : (
                <h4 className="d-flex justify-content-center">No Recommendations yet</h4>
            )}
        </div>
    )
};

export default RecommendationList;