import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import StockPage from './pages/StockPage';
import AnalysisLoadingPage from './pages/AnalysisLoadingPage';
import MainLayout from './components/MainLayout';
import StockLandingPage from './pages/StockLandingPage';
import FavoritesPage from './pages/FavoritesPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout/>}>
          <Route path="/" element={<HomePage />} />
          <Route path="/stock" element={<StockLandingPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          {/* Dynamic route for individual stock tickers */}
          <Route path="/stock/:ticker" element={<StockPage />} />
        </Route>

        {/* Route for the loading page (this is outside of the Main Layout) */}
        <Route path="/loading-analysis/:taskId/:ticker" element={<AnalysisLoadingPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;