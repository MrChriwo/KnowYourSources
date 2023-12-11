import './App.scss'
import {Routes, Route} from 'react-router-dom'
import Sidebar from './components/sidebar/Sidebar'
import Predict from './pages/predict'
import { Row, Col} from 'react-bootstrap';
import TopBanner from './components/topBanner/TopBanner';

const App = () => {

  return (
    <div className='app'>
      Tihs is a ci/cd test
      <TopBanner/>
      <Row>
        {/* Sidebar */}
        <Col xs={1} className="sidebar">
          <Sidebar/>
        </Col>

        {/* Content */}
        <Col className="content">
          <Routes>
            <Route path="/" element={<Predict/>}/>
          </Routes>
        </Col>
      </Row>
  </div>
  )
}

export default App
