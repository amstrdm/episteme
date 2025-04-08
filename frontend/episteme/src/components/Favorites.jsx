import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from "../api/axiosinstance";

const Favorites = () => {
  const [favoriteDetails, setFavoriteDetails] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFavoriteDetails = async () => {
      setIsLoading(true);
      setError(null);
      setFavoriteDetails([]);

      let favoriteItems = [];
      const storageKey = 'favorites';

      try {
        const storedFavorites = localStorage.getItem(storageKey);
        if (storedFavorites) {
          const parsedFavorites = JSON.parse(storedFavorites);
           // **Expect array of objects with ticker and logo**
          if (Array.isArray(parsedFavorites)) {
             favoriteItems = parsedFavorites.filter(
               item => typeof item === 'object' && item !== null && typeof item.ticker === 'string' && item.ticker.trim() !== ''
             );
             if (favoriteItems.length !== parsedFavorites.length) {
                localStorage.setItem(storageKey, JSON.stringify(favoriteItems));
             }
          } else {
            console.error("Stored favorites is not a valid array:", parsedFavorites);
            localStorage.setItem(storageKey, "[]");
            throw new Error("Invalid data format in local storage.");
          }
        }
      } catch (err) {
        console.error("Error accessing or parsing local storage:", err);
        setError("Could not load favorite tickers.");
        setIsLoading(false);
        return;
      }

      if (favoriteItems.length === 0) {
        setIsLoading(false);
        return;
      }

      let userTimezone = 'UTC';
      try {
        userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      } catch (tzError) {
        console.warn("Could not detect user timezone, defaulting to UTC.", tzError);
      }

      try {
        const fetchPromises = favoriteItems.map(favItem => {
          const ticker = favItem.ticker;
          const logoFromStorage = favItem.logo;

          return apiClient.get('/retrieve-analysis', {
            params: {
                ticker: ticker,
                timezone: userTimezone,
                only_database: true
            }
          })
            .then(response => {
              const data = response.data;
              if (data && data.company) {
                return {
                  ticker: data.company.ticker || ticker,
                  title: data.company.title || 'Unknown Company',
                  sentimentScore: data.company.sentimentScore ?? null,
                  logo: logoFromStorage,
                };
              } else {
                 console.warn(`Received invalid data structure for ticker: ${ticker}`, data);
                 return { ticker: ticker, title: 'Data Error', sentimentScore: null, logo: logoFromStorage, error: true };
              }
            })
            .catch(err => {
               console.error(`Failed to fetch details for ticker ${ticker}:`, err.response?.data || err.message || err);
               return { ticker: ticker, title: 'Fetch Error', sentimentScore: null, logo: logoFromStorage, error: true };
            });
        });

        const results = await Promise.all(fetchPromises);
        const validDetails = results.filter(detail => detail && !detail.error);
        setFavoriteDetails(validDetails);

      } catch (fetchError) {
        console.error("An error occurred during batch API requests:", fetchError);
        setError("Failed to fetch details for some favorites.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchFavoriteDetails();
  }, []);


  const handleImageError = (e) => {
    e.target.onerror = null;
    e.target.src = '';
  };


  return (
    <section className="flex flex-col justify-center p-8 w-full rounded-2xl bg-widget-background text-light-text max-md:px-5 max-md:max-w-full">
      <h2 className="text-2xl font-semibold mb-6 text-white-text">Favorites</h2>

      {isLoading && ( <div className="text-gray-400 p-4 text-center">Loading favorite details...</div> )}
      {!isLoading && error && ( <div className="text-red-500 p-4 text-center">{error}</div> )}

      {!isLoading && !error && (
        <>
          {favoriteDetails.length === 0 ? (
            <p className="text-gray-400 p-4 text-center">You haven't added any stocks to your favorites yet.</p>
          ) : (
            <ul className="list-none p-0 m-0">
              {favoriteDetails.map((fav) => (
                <li key={fav.ticker} className="mb-4 last:mb-0">
                  <Link
                    to={`/stock/${fav.ticker.toLowerCase()}`}
                    className="flex items-center gap-4 p-4 bg-dark-background rounded-lg hover:opacity-50 transition-opacity duration-150 cursor-pointer w-full"
                  >
                    <img
                      src={fav.logo || 'https://via.placeholder.com/40?text=N/A'}
                      alt={`${fav.title || 'Stock'} logo`}
                      className="w-10 h-10 rounded-full object-contain flex-shrink-0 p-0.5"
                      onError={handleImageError}
                    />
                    <div className="flex-1 flex items-center gap-4 overflow-hidden">
                      <span className="font-semibold text-lg w-16 flex-shrink-0 text-white-text">
                        {fav.ticker.toUpperCase()}
                      </span>
                      <span className="text-base text-gray-300 truncate" title={fav.title}>
                        {fav.title}
                      </span>
                    </div>
                    <span className={`ml-auto font-medium text-lg px-3 py-1 rounded whitespace-nowrap ${
                          fav.sentimentScore === null ? 'text-gray-400 bg-gray-700/50'
                          : fav.sentimentScore > 60 ? 'text-green-300 bg-green-900/50'
                          : fav.sentimentScore >= 40 ? 'text-orange-300 bg-orange-900/50'
                          : 'text-red-300 bg-red-900/50'
                          }`}>
                      {typeof fav.sentimentScore === 'number' ? fav.sentimentScore : '-'}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </section>
  );
};

export default Favorites;