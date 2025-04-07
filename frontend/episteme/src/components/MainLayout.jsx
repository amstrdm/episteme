// src/components/MainLayout.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './SideBar';

const MainLayout = () => {
  // Define header height for padding calculation
  const headerHeight = '80px';

  return (
    <div className="min-h-screen bg-dark-background">
      <Header />
      <div className="flex pt-[--header-height]" style={{'--header-height': headerHeight}}>
        <Sidebar />
        {/* Main content area with padding for header and sidebar */}
        <main
            className="flex-grow p-6 md:pl-[calc(var(--sidebar-width,80px)+1.5rem)]"
            style={{paddingTop: `calc(${headerHeight} + 1.5rem)`}}
        >
          <Outlet /> {/* Child routes will render here */}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;