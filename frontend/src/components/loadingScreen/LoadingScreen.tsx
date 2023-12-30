import { Modal } from "react-bootstrap";
import { RingLoader } from "react-spinners";


interface Props {
    show: boolean;
}


const LoadingScreen = (props: Props) => {
    const { show } = props;

    return (
        <Modal show={show} centered>
            <Modal.Body className="bg-dark">
                <div>
                    <h3 style={{color: "green"}}className="d-flex justify-content-center mb-4">LOADING</h3>
                    <div className="d-flex justify-content-center">
                    <RingLoader
                        color="green"
                        size={150}
                    ></RingLoader>
                    </div>

                </div>
            </Modal.Body>
        </Modal>
    )
};

export default LoadingScreen;