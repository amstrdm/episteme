import React, { useState, useEffect } from "react";
import MetricCard from "./MetricCard";
import SentimentScore from "./SentimentScore";
import StarIcon from "./StarIcon";

const formatMarketCap = (value) => {
  const num = Number(value);
  if (value == null || isNaN(num)) { return "N/A"; }
  if (num >= 1e12) { return `$${(num / 1e12).toFixed(2)}T`; }
  if (num >= 1e9) { return `$${(num / 1e9).toFixed(2)}B`; }
  if (num >= 1e6) { return `$${(num / 1e6).toFixed(2)}M`; }
  if (num >= 1e3) { return `$${(num / 1e3).toFixed(2)}K`; }
  return `$${num.toFixed(2)}`;
};

const formatEarningsDate = (dateString) => {
  if (!dateString) return "N/A";
  try {
    const dateParts = dateString.split(' ');
    let dateToParse = dateString;
    if (dateParts.length > 2 && /^[A-Z]{3,4}$/.test(dateParts[dateParts.length - 1])) {
      dateToParse = dateParts.slice(0, -1).join(' ');
    }
    const date = new Date(dateToParse);
    if (isNaN(date.getTime())) {
        const simpleDate = new Date(dateParts[0]);
        if (!isNaN(simpleDate.getTime())) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Intl.DateTimeFormat('en-US', options).format(simpleDate) + " (Time N/A)";
        }
        return "N/A";
    }
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false };
    return new Intl.DateTimeFormat('en-US', options).format(date);
  } catch (error) {
    console.error("Error formatting date:", error);
    return "N/A";
  }
};

const capitalizeWord = (word) => {
  if (!word) return '';
  return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
};

const formatAnalystRating = (rating, defaultText = "N/A") => {
  if (!rating || typeof rating !== 'string') {
    return defaultText;
  }
  const spacedRating = rating.replace(/_/g, ' ');
  const formattedRating = spacedRating
    .split(' ')
    .map(capitalizeWord)
    .join(' ');
  return formattedRating;
};


const getDcfColorClass = (dcf, price) => {
  const dcfNum = Number(dcf);
  const priceNum = Number(price);
  if (dcf == null || price == null || isNaN(dcfNum) || isNaN(priceNum)) { return ''; }
  if (dcfNum > priceNum) return 'text-green-500';
  if (dcfNum < priceNum) return 'text-red-500';
  return '';
};

const getRatingColorClass = (rating) => {
    if (!rating || typeof rating !== 'string') return '';
    const lowerRating = rating.toLowerCase().replace(/_/g, ' ');
    // Define keywords for categories broadly
    const positiveKeywords = ['buy', 'outperform', 'overweight', 'accumulate', 'strong buy'];
    const negativeKeywords = ['sell', 'underperform', 'underweight', 'reduce', 'strong sell'];
    const neutralKeywords = ['hold', 'neutral', 'market perform', 'equal-weight']

    if (positiveKeywords.some(keyword => lowerRating.includes(keyword))) return 'text-green-500';
    if (negativeKeywords.some(keyword => lowerRating.includes(keyword))) return 'text-red-500';
    if (neutralKeywords.some(keyword => lowerRating.includes(keyword))) return 'text-yellow-500';

    return '';
};


const getForwardPEColorClass = (forwardPE) => {
  const peNum = Number(forwardPE);
  if (forwardPE == null || isNaN(peNum)) { return ''; }
  if (peNum < 0) return 'text-red-500'; // Negative PE is generally unfavorable
  return '';
};

const getBetaColorClass = (beta) => {
    const betaNum = Number(beta);
    if (beta == null || isNaN(betaNum)) { return ''; }
    const highBetaThreshold = 1.5;
    const lowBetaThreshold = 0.8;

    if (betaNum > highBetaThreshold) return 'text-red-500'; // High volatility
    if (betaNum < lowBetaThreshold) return 'text-green-500'; // Low volatility
    return 'text-yellow-500'; // Moderate volatility (or around market average)
};

const StockInfo = ({ company, isDescriptionExpanded, onToggleDescription }) => {
  const defaultText = "N/A";
  const noDescriptionText = "No Description available.";

  const [isFavorite, setIsFavorite] = useState(false);
  const [animateStar, setAnimateStar] = useState(false);

  useEffect(() => {
    if (company && company.ticker) {
      try {
        const storedFavoritesRaw = localStorage.getItem('favorites');
        let storedFavorites = [];

        if (storedFavoritesRaw) {
            storedFavorites = JSON.parse(storedFavoritesRaw);
            if (!Array.isArray(storedFavorites)) {
                console.error("Favorites in localStorage is not an array. Resetting.");
                localStorage.setItem('favorites', "[]");
                storedFavorites = [];
            } else {
                 storedFavorites = storedFavorites.filter(item => typeof item === 'object' && item !== null && typeof item.ticker === 'string');
                 if (storedFavorites.length !== JSON.parse(storedFavoritesRaw).length) {
                     localStorage.setItem('favorites', JSON.stringify(storedFavorites));
                 }
            }
        }

        // **Check for object with matching ticker**
        const isFav = storedFavorites.some(fav => fav.ticker === company.ticker);
        setIsFavorite(isFav);

      } catch (error) {
        console.error("Error reading/parsing favorites from localStorage:", error);
        if (error instanceof SyntaxError) {
             localStorage.setItem('favorites', "[]");
        }
        setIsFavorite(false);
      }
    } else {
        setIsFavorite(false);
    }
  }, [company]);

  const toggleFavorite = () => {
    if (!company || !company.ticker) return;

    try {
        const storedFavoritesRaw = localStorage.getItem('favorites');
        let storedFavorites = [];

        if (storedFavoritesRaw) {
            storedFavorites = JSON.parse(storedFavoritesRaw);
            if (!Array.isArray(storedFavorites)) {
                console.error("Favorites in localStorage is not an array during toggle. Resetting.");
                localStorage.setItem('favorites', "[]");
                storedFavorites = [];
            } else {
                 storedFavorites = storedFavorites.filter(item => typeof item === 'object' && item !== null && typeof item.ticker === 'string');
            }
        }

        const favoriteIndex = storedFavorites.findIndex(fav => fav.ticker === company.ticker);
        let updatedFavorites;

        if (favoriteIndex > -1) {
            updatedFavorites = storedFavorites.filter((_, index) => index !== favoriteIndex);
            setIsFavorite(false);
        } else {
            const newFavorite = {
                ticker: company.ticker,
                logo: company.logo || null
            };
            updatedFavorites = [...storedFavorites, newFavorite];
            setIsFavorite(true);
        }

        localStorage.setItem('favorites', JSON.stringify(updatedFavorites));

    } catch (error) {
        console.error("Error updating favorites in localStorage:", error);
        if (error instanceof SyntaxError) {
             localStorage.setItem('favorites', "[]");
             setIsFavorite(false); // Also reset component state
        }
    }
  };

  const dcfColor = getDcfColorClass(company.dcf, company.price);
  const ratingColor = getRatingColorClass(company.analystRating);
  const forwardPEColor = getForwardPEColorClass(company.forwardPE);
  const betaColor = getBetaColorClass(company.beta);
  const displayRating = formatAnalystRating(company.analystRating, defaultText);

  return (
    <section className="flex flex-col justify-center p-8 w-full rounded-2xl bg-widget-background max-md:px-5 max-md:max-w-full">
      <div className="flex gap-6 justify-between items-stretch max-md:flex-col max-md:max-w-full">
        <div className="flex flex-col flex-1 items-start max-md:max-w-full">
          {/* Header: Logo, Ticker, Price, Name, Favorite Button */}
          <div className="flex items-center gap-4">
            {company.logo && (
              <img
                src={company.logo}
                className="object-contain overflow-hidden aspect-square w-[70px] h-[70px] mb-0" // Adjusted size and margin
                alt={`${company.title || "Company"} logo`}
              />
            )}
            <div className={company.logo ? "mt-0" : "mt-8"}>
              {" "}
              {/* Conditional margin if no logo */}
              <div className="flex gap-2 items-center text-3xl whitespace-nowrap">
                {/* Ticker with Link */}
                {company.ticker &&
                company.ticker !== defaultText &&
                company.website &&
                company.website !== defaultText ? (
                  <a
                    href={company.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    title={`Open ${company.ticker}'s website`}
                  >
                    <h1 className="font-medium text-white-text hover:text-green-400 transition-colors duration-450 ease-in-out">
                      {company.ticker?.toUpperCase() || defaultText}
                    </h1>
                  </a>
                ) : (
                  <h1 className="font-medium text-white-text">
                    {company.ticker?.toUpperCase() || defaultText}
                  </h1>
                )}
                {/* Price */}
                <span className="font-semibold text-green-500">
                  {company.price != null ? `$${company.price}` : defaultText}
                </span>
                {/* Favorite Button */}
                <button
                  onClick={() => {
                    toggleFavorite();
                    setAnimateStar(true);
                    setTimeout(() => setAnimateStar(false), 300);
                  }}
                  aria-label="Toggle Favorite"
                  className="focus:outline-none hover:cursor-pointer"
                >
                  <StarIcon
                    isFavorite={isFavorite}
                    className={`transition-transform duration-300 ${
                      animateStar ? "scale-125" : ""
                    }`}
                  />
                </button>
              </div>
              {/* Company Name */}
              <p className="mt-1 text-sm text-slate-400">
                {company.title || defaultText}
              </p>
            </div>
          </div>

          {/* Metric Cards */}
          <div className="self-stretch mt-6 w-full text-sm tracking-wide leading-none max-md:max-w-full">
            {/* First row of metric cards */}
            <div className="flex flex-wrap gap-4 items-center w-full max-md:max-w-full">
              <MetricCard
                label="Exchange:"
                value={company.exchangeShortName || defaultText}
                className="min-w-60 w-[245px]"
              />
              <MetricCard
                label="Market Cap:"
                value={formatMarketCap(company.mktCap)}
                className="min-w-60 w-[245px]"
              />
              <MetricCard
                label="Industry:"
                value={company.industry || defaultText}
                className="min-w-60 w-[245px]"
              />
            </div>
            {/* Second row of metric cards */}
            <div className="flex flex-wrap gap-4 items-center mt-4 w-full max-md:max-w-full">
              <MetricCard
                label="Next Earnings Call:"
                value={formatEarningsDate(company.earningsCallDate)}
              />
              <MetricCard
                label="DCF Value:"
                value={company.dcf != null ? `$${company.dcf}` : defaultText}
                valueClassName={dcfColor}
                className="w-fit"
              />
              <MetricCard
                label="Beta:"
                value={company.beta ?? defaultText}
                valueClassName={betaColor}
              />
              <MetricCard
                label="Analyst Rating:"
                value={displayRating}
                valueClassName={ratingColor}
              />
              <MetricCard
                label="Forward PE:"
                value={company.forwardPE ?? defaultText}
                valueClassName={forwardPEColor}
                className="w-fit"
              />
            </div>
          </div>
        </div>

        {/* Right Side: Sentiment Score Component */}
        <div className="flex flex-col items-center max-md:mt-6">
          <SentimentScore score={company.sentimentScore ?? null} />
        </div>
      </div>

      {/* Description Section */}
      <div className="flex flex-col justify-center p-4 mt-6 w-full text-sm tracking-wide rounded-lg bg-dark-background">
          <div className="flex items-center mb-3">
            <h2 className="text-xl font-semibold text-white-text tracking-normal mr-1.5">
              Description
            </h2>
            <div className="group relative flex items-center">
                <img 
                src="/deepseek_logo.webp" 
                alt="Information"
                className="h-4 w-auto cursor-pointer mt-1" 
                />
                <span
                className="
                  absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2
                  w-max max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg
                  invisible group-hover:visible opacity-0 group-hover:opacity-100
                  bg-slate-700 text-white-text text-xs rounded py-1.5 px-3 shadow-lg
                  transition-all duration-200 ease-in-out z-10 whitespace-nowrap"
                >
                  Powered by DeepSeek
                </span>
            </div>
          </div>
        <div className="mt-2 leading-relaxed text-slate-200 text-max-md:max-w-full">
          {!company.description ? (
            <p>{noDescriptionText}</p>
          ) : isDescriptionExpanded ? (
            <p>{company.description}</p> // Show full description if expanded
          ) : (
            // Show truncated description if not expanded
            <p>{`${company.description.substring(0, 500)}...`}</p>
          )}
          {company.description && company.description.length > 500 && (
            <button
              className="
                    block mt-2
                    text-base
                    font-medium
                    rounded-md
                    text-green-400
                    cursor-pointer
                    hover:text-green-300
                    transition duration-200 ease-in-out
                  "
              onClick={onToggleDescription}
            >
              {isDescriptionExpanded ? "See less" : "See more"}
            </button>
          )}
        </div>
      </div>
    </section>
  );
};

export default StockInfo;