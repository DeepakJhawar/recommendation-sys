import './App.css';
import Personalized from './Personalized';
import TopProducts from './TopProducts';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TopProducts />} />
        <Route path="/recommend" element={<Personalized />} />
      </Routes>
    </Router>
  );
}

export default App;
