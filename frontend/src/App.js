import logo from './logo.svg';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './Home/Home';
import Login from './Login/Login';
import Loan from './Loan/Loan';
import LoanDetails from './LoanDetails/LoanDetails';

function App() {
  return (
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/loan" element={<Loan />} />
        <Route path="/LoanDetails" element={<LoanDetails />} />
      </Routes>
  );
}

export default App;
