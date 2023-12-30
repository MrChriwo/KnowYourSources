import { Row, Col, Form, Button } from 'react-bootstrap';
import { IoSend } from 'react-icons/io5';
import { useState, FormEvent } from 'react';
import { requestBody, responseBody } from '../../models/predict';
import './AbstractFrame.scss';
import { predictPapers } from '../../services/api/PredictService';
import LoadingScreen from '../loadingScreen/LoadingScreen';

interface Props {
  setResponse: (response: responseBody[] | null) => void;
}

const AbstractFrame = (props: Props) => {
  const { setResponse } = props;
  const [abstract, setAbstract] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const requestBody: requestBody = {
    title: '',
    abstract: '',
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Access the values of the input fields
    const titleValue = (e.currentTarget.elements.namedItem(
      'titleInput'
    ) as HTMLInputElement).value;
    const abstractValue = (e.currentTarget.elements.namedItem(
      'abstractTextarea'
    ) as HTMLInputElement).value;

    // Update the state with the entered values
    setTitle(titleValue);
    setAbstract(abstractValue);

    // Update the requestBody array
    requestBody.title = titleValue;
    requestBody.abstract = abstractValue;

    try { 
      setIsProcessing(true);
      const response = await predictPapers(requestBody, "specter");
      setIsProcessing(false);

      setResponse(response);
    }

    catch (error) {
      setIsProcessing(false);
      console.log(error);
    }
  }
  ;

  return (
    <div className='row abstract-frame d-flex justify-content-center'>
      {isProcessing && <LoadingScreen show={isProcessing} />}
      <div className="abstract-message mb-3">
          {abstract !== '' ? (
            <div className="message-text">
            <h4>{title}</h4>
            {abstract}
            </div>
          ) : (
            <h4 className="d-flex justify-content-center">No Abstract yet</h4>
          )}
      </div>
      <div className="send-message-form d-flex justify-content-center">
        <Form onSubmit={handleSubmit}>
          <Form.Group>
            <Row>
              <Col xs={8}>
                <Form.Control className='mb-3'
                  type="text"
                  name="titleInput"
                  placeholder="Type the title here"
                  required
                />
                <Form.Control
                  as="textarea"
                  rows={2}
                  name="abstractTextarea"
                  placeholder="Paste your abstract here"
                  required
                />
              </Col>
              <Col>
                <Button variant="success" type="submit" style={{ marginTop: "33%" }}>
                  {<IoSend />}
                </Button>
              </Col>
            </Row>
          </Form.Group>
        </Form>
      </div>
    </div>
  );
};

export default AbstractFrame;
