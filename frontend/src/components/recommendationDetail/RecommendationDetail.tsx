import { Modal } from "react-bootstrap";
import { responseBody } from "../../models/predict";


interface Props {
    show: boolean;
    onHide: () => void;
    recommendation: responseBody;
}


const RecommendationDetail = (props: Props) => {
    const { show, recommendation, onHide } = props;

    return (
        <Modal size="lg" show={show} centered onHide={onHide}>
            <Modal.Header>
                <div>
                <Modal.Title className="mb-2">{recommendation.title}</Modal.Title>
                <h6>by {recommendation.authors}</h6>
                <p>Matching to your request: {recommendation.score}</p>
                </div>
            </Modal.Header>
            <Modal.Body >
                <div style={{maxHeight: "12em" , overflowY: "auto"}} className="d-flex justify-conent-center">
                    {recommendation.abstract}
                </div>
            </Modal.Body>
        </Modal>
    )
};

export default RecommendationDetail;