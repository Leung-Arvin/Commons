import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { FloorPlansPage } from './pages/FloorPlans';
import { FloorMap } from './components/FloorMap';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FloorPlansPage />} />
        <Route path="/floor-plan/:mapId" element={<FloorMapWrapper />} />
      </Routes>
    </BrowserRouter>
  );
}

function FloorMapWrapper() {
  // Extract mapId from URL params
  const mapId = window.location.pathname.split('/').pop() || '';
  return <FloorMap mapId={mapId} />;
}

export default App;