import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import SearchBar from './SearchBar';

const Header = () => {
  const location = useLocation();
  const homePath = '/';
  const isHomePage = location.pathname === homePath;

  const headerClasses = `
    fixed top-0 left-0 right-0 grid items-center w-full text-light-text bg-widget-background z-50 p-4 border-b border-gray-700
    min-h-20 /* Adjust min height as needed */
    max-md:grid-cols-1 max-md:py-3 max-md:gap-3
    ${isHomePage ? 'grid-cols-[auto_1fr_auto]' : 'md:grid-cols-3'}
  `;

  return (
    <header className={headerClasses.trim()}>
      {/* Left Column: Logo + Text Link */}
      <div className="flex justify-start md:justify-start max-md:order-1 max-md:justify-center">
        <Link
            to="/"
            className="flex items-center gap-2 group rounded-md"
            aria-label="Episteme Home Page"
        >
            <img
                src="/vectorized_logo_scaled.svg"
                className="object-contain overflow-hidden shrink-0 aspect-square w-[41px] h-[41px]"
                alt=""
            />
            <span className="text-xl lg:text-2xl font-bold text-white-text group-hover:text-episteme-teal transition-colors duration-300">
              Episteme
            </span>
        </Link>
      </div>

      {/* Center Column: Search Bar Container OR Null */}
      {!isHomePage && (
        <div className="relative w-full max-w-xl mx-auto px-2 md:px-4 flex items-center">
          <SearchBar />
        </div>
      )}

      {/* Right Column: Navigation */}
      <nav className="flex gap-4 md:gap-6 justify-end items-center text-sm font-medium max-md:order-2 max-md:w-full max-md:justify-center max-md:mt-2">
        <div className="flex gap-5 items-center">
          <a href="https://docs.episteme.cloud" className="hover:text-blue-400 transition-colors">Docs</a>
        </div>
      </nav>
    </header>
  );
};

export default Header;