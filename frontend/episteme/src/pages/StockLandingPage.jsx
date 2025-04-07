import React from 'react';
import { Link } from 'react-router-dom';
const IconHomeOutline = (props) => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
    </svg>
);

const StockLandingPage = () => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 rounded-2xl bg-widget-background min-h-[60vh]">
      <h2 className="text-2xl font-semibold text-white-text mb-4">
        No Stock Selected
      </h2>
      <p className="text-slate-400 max-w-md">
        Please use the search bar in the header or navigate via the Home icon <IconHomeOutline className="inline w-5 h-5 mx-1 align-text-bottom" /> to find and select a stock for analysis.
      </p>
       {/* Link back to home */}
       <Link to="/" className="mt-6 text-green-400 hover:text-green-300 font-medium">Go to Home/Search</Link> 
    </div>
  );
};

export default StockLandingPage;