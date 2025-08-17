import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Welcome from './pages/Welcome';
import CreateBot from './pages/CreateBot';
import BotChat from './pages/BotChat';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/welcome" element={<Welcome />} />
      <Route path="/bots/new" element={<CreateBot />} />
      <Route path="/bots/:botId/chat" element={<BotChat />} />
    </Routes>
  );
}

export default App;

