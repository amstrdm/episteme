import React, { useState, useEffect, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../api/axiosinstance';
import axios from 'axios';

import StockInfo from '../components/StockInfo';
import PointsList from '../components/PointsList';
import ErrorMessage from '../components/ErrorMessage';

const StockPage = () => {
  const { ticker } = useParams();
  const [stockData, setStockData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    setError(null);
    setStockData(null);
    setIsDescriptionExpanded(false);

    if (!ticker) {
      setIsLoading(false);
      setError("No ticker provided.");
      return;
    }

    const abortController = new AbortController();
    const fetchData = async () => {
      let userTimezone = 'UTC'; // Default
      try {
          userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      } catch(e) {
          console.warn("Could not determine user timezone, defaulting to UTC.", e);
      }

      const relativePath = `/retrieve-analysis`;

      try {
        const response = await apiClient.get(relativePath, {
          signal: abortController.signal,
          params: {
            ticker: ticker,
            timezone: userTimezone
          }
        });
        setStockData(response.data);
      } catch (err) {
        if (axios.isCancel(err)) {
          console.log('Request canceled:', err.message);
        } else {
          console.error("Error fetching stock data:", err);
          let errorMessage = "Failed to fetch data. Please try again.";
          if (err.response) {
            errorMessage = `API Error: ${err.response.status} - ${err.response.data?.message || err.response.data?.detail || err.response.statusText || 'Error'}`;
          } else if (err.request) {
            errorMessage = "Network Error: No response received from server.";
          } else {
            errorMessage = err.message || errorMessage;
          }
          setError(errorMessage);
        }
      } finally {
        if (!abortController.signal.aborted) {
            setIsLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      console.log("Aborting stock data request...");
      abortController.abort();
    };

  }, [ticker]);

  const toggleDescription = () => {
    setIsDescriptionExpanded(!isDescriptionExpanded);
  };

  // Using useMemo, recalculates only when stockData.points changes
  const { bullishPoints, bearishPoints } = useMemo(() => {
    const safePoints = Array.isArray(stockData?.points) ? stockData.points : [];
    const bp = safePoints.filter(p => p.sentimentScore >= 50);
    const brp = safePoints.filter(p => p.sentimentScore < 50);
    return { bullishPoints: bp, bearishPoints: brp };
  }, [stockData?.points]);


  if (isLoading) {
    return (
        <div className="flex justify-center items-center min-h-[calc(100vh-var(--header-height,80px)-3rem)]">
            <div className="loader ml-1"></div>
        </div>
    );
  }

  if (error) {
    return (
        <div className="flex justify-center items-center min-h-[calc(100vh-var(--header-height,80px)-3rem)]">
            <ErrorMessage message={error} />
        </div>
     );
  }

   if (!ticker) {
     return (
        <div className="flex justify-center items-center min-h-[calc(100vh-var(--header-height,80px)-3rem)]">
            <ErrorMessage message="No stock ticker specified in the URL." />
        </div>
     );
  }

  if (!stockData || !stockData.company) {
     return (
        <div className="flex flex-col justify-center items-center text-center min-h-[calc(100vh-var(--header-height,80px)-3rem)] p-6 rounded-2xl bg-widget-background">
            <h2 className="text-2xl font-semibold text-white-text mb-4">Data Not Found</h2>
            <p className="text-slate-400">No analysis data could be found for the ticker "{ticker}".</p>
        </div>
     );
  }

  return (
    <div className="space-y-6">
        <StockInfo
            company={{
                ...stockData.company,
            }}
            isDescriptionExpanded={isDescriptionExpanded}
            onToggleDescription={toggleDescription}
        />

        <div className="flex gap-5 max-md:flex-col min-h-[200px]">
            {/* Bullish Points */}
            <div className="w-full md:w-6/12">
                <PointsList
                    title="Bullish"
                    points={bullishPoints}
                    type="bullish"
                />
            </div>
            {/* Bearish Points */}
            <div className="w-full md:w-6/12">
                <PointsList
                    title="Bearish"
                    points={bearishPoints}
                    type="bearish"
                />
            </div>
        </div>
    </div>
  );
};

export default StockPage;