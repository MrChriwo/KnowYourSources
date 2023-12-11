import { Row, Col, Form, Button } from 'react-bootstrap';
import { IoSend } from 'react-icons/io5';
import { useState, FormEvent } from 'react';
import './AbstractFrame.scss';

const AbstractFrame = () => {
  const [abstract, setAbstract] = useState<string>('');

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Access the value of the textarea
    const abstractText = (e.currentTarget.elements.namedItem(
      'abstractTextarea'
    ) as HTMLInputElement).value;

    // Update the state with the entered abstract
    setAbstract(abstractText);

    // Handle the API call to predict abstract if needed
  };

  return (
    <div className='row abstract-frame d-flex justify-content-center'>
      <div className="abstract-message mb-3">
          {abstract !== '' ? (
            <div className="message-text">
            <h4>Your Abstract</h4>
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
              <Form.Control
                as="textarea"
                rows={2}
                name="abstractTextarea"
                placeholder="paste your abstract here"
              />
            </Col>
            <Col>
              <Button variant="success" type="submit" style={{marginTop: "2%"}}>
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
