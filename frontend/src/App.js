import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './Home/Home';
import Login from './Login/Login';
import Loan from './Loan/Loan';

function App() {
  return (
      <div>
        <title>Aqua Bank</title>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/loan" element={<Loan />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
