import React from 'react';
import SearchBar from '../components/SearchBar';
import Header from '../components/Header';

const HomePage = () => {
  const headerHeight = '80px';

  return (
    <>
    <Header />
    <div
        className="flex flex-col items-center min-h-screen w-full bg-dark-background text-light-text px-4 sm:px-6 lg:px-8"
        style={{ paddingTop: `calc(${headerHeight} + 2rem)` }} // Add padding top dynamically
    >
        <div className="flex flex-col items-center text-center w-full max-w-2xl mt-12 sm:mt-16">

            {/* Larger Logo */}
            <img src="/vectorized_logo_scaled.svg" alt="Episteme Logo" className="w-30 h-30 mb-6" /> 

            {/* Headline */}
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white-text mb-4">
                Stock Analysis Insights
            </h1>

            {/* Description/Instructions */}
            <p className="text-base sm:text-lg text-slate-400 mb-8 px-4">
                Enter a stock ticker below to access detailed analysis, including sentiment scores, financial data, and expert ratings.
            </p>

            {/* Large, Centered Search Bar */}
            <div className="w-full max-w-xl mb-8">
                 <SearchBar />
            </div>
        </div>
    </div>

    </>
  );
};

export default HomePage;