import React from "react";
import { motion } from "framer-motion";
import { useNavigate, useLocation } from "react-router-dom";

// Icon for Home/Search (Magnifying Glass) - Will be Index 0
const Icon0Outline = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
  </svg>
);
const Icon0Solid = Icon0Outline;

// Icon for Stock Info (Chart/Graph) - Will be Index 1
const Icon1Outline = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
  </svg>
);
const Icon1Solid = (props) => (
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" {...props}>
    <path d="M18.375 2.25c-1.035 0-1.875.84-1.875 1.875v15.75c0 1.035.84 1.875 1.875 1.875h.75c1.035 0 1.875-.84 1.875-1.875V4.125c0-1.036-.84-1.875-1.875-1.875h-.75ZM9.75 8.625c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v11.25c0 1.035-.84 1.875-1.875 1.875h-.75a1.875 1.875 0 0 1-1.875-1.875V8.625ZM3 13.125c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v6.75c0 1.035-.84 1.875-1.875 1.875h-.75A1.875 1.875 0 0 1 3 19.875v-6.75Z" />
  </svg>
);

// Icon for Favorites (Star) - Will be Index 2
const Icon2Outline = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
  </svg>
);
const Icon2Solid = (props) => (
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" {...props}>
    <path fillRule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z" clipRule="evenodd" />
  </svg>
);


const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // 0: Home, 1: Stock, 2: Favorites
  const routes = ['/', '/stock', '/favorites'];

  let selectedIndex = -1; // Default: none selected
  if (location.pathname === routes[0]) { // Check for Home first
    selectedIndex = 0;
  } else if (location.pathname.startsWith(routes[1])) { // Then check for Stock
    selectedIndex = 1;
  } else if (location.pathname.startsWith(routes[2])) { // Then check for Favorites
    selectedIndex = 2;
  }

  const getButtonBaseClasses = () => "group relative flex justify-center items-center w-12 h-12 cursor-pointer rounded-xl transition-colors duration-150 ease-in-out";
  const getIconClasses = (index) => {
    const base = "w-6 h-6 transition-colors duration-150 ease-in-out";
    return selectedIndex === index ? `${base} text-white` : `${base} text-gray-400 group-hover:text-white`;
  };
  const renderIcon = (index, IconSolid, IconOutline) => (
    <span className="relative z-10">
      {selectedIndex === index ? <IconSolid className={getIconClasses(index)} /> : <IconOutline className={getIconClasses(index)} />}
    </span>
  );

  const handleNavigate = (path) => {
    navigate(path);
  };

  const headerHeight = '80px';
  const sidebarTopMargin = '1rem';

  return (
    <aside
      className="fixed left-4 flex flex-col items-center p-2 bg-widget-background rounded-[64px] max-md:hidden z-40 bottom-5"
      style={{ top: `calc(${headerHeight} + ${sidebarTopMargin})` }}
    >
      <div className="flex flex-col items-center w-full max-w-12 gap-2 mt-2">

        {/* Button 0: Home/Search*/}
        <button
          className={getButtonBaseClasses()}
          onClick={() => handleNavigate(routes[0])} // Navigate to '/'
          aria-label="Home / Search"
          aria-pressed={selectedIndex === 0}
        >
           {/* Hover BG */}
           {selectedIndex !== 0 && <div className="absolute inset-0 rounded-full bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-150 ease-in-out z-0"></div>}
           {/* Selected Indicator */}
           {selectedIndex === 0 && <motion.div layoutId="activeIndicator" className="absolute inset-0 bg-green-500 rounded-full z-0" transition={{ type: "spring", stiffness: 500, damping: 30 }} />}
           {/* Icon */}
           {renderIcon(0, Icon0Solid, Icon0Outline)}
        </button>

        {/* Button 1: Stock Info*/}
        <button
          className={getButtonBaseClasses()}
          onClick={() => handleNavigate(routes[1])} // Navigate to '/stock'
          aria-label="Stock Information"
          aria-pressed={selectedIndex === 1}
        >
           {/* Hover BG */}
           {selectedIndex !== 1 && <div className="absolute inset-0 rounded-full bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-150 ease-in-out z-0"></div>}
           {/* Selected Indicator */}
           {selectedIndex === 1 && <motion.div layoutId="activeIndicator" className="absolute inset-0 bg-green-500 rounded-full z-0" transition={{ type: "spring", stiffness: 500, damping: 30 }} />}
           {/* Icon */}
           {renderIcon(1, Icon1Solid, Icon1Outline)}
        </button>

        {/* Button 2: Favorites*/}
        <button
          className={getButtonBaseClasses()}
          onClick={() => handleNavigate(routes[2])} // Navigate to '/favorites'
          aria-label="View Favorites"
          aria-pressed={selectedIndex === 2}
        >
           {/* Hover BG */}
           {selectedIndex !== 2 && <div className="absolute inset-0 rounded-full bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-150 ease-in-out z-0"></div>}
           {/* Selected Indicator */}
           {selectedIndex === 2 && <motion.div layoutId="activeIndicator" className="absolute inset-0 bg-green-500 rounded-full z-0" transition={{ type: "spring", stiffness: 500, damping: 30 }} />}
           {/* Icon */}
           {renderIcon(2, Icon2Solid, Icon2Outline)}
        </button>

      </div>
    </aside>
  );
};

export default Sidebar;