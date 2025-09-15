import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import BottomNavigation from './BottomNavigation';

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="pb-20">
        <Outlet />
      </main>
      
      <BottomNavigation />
    </div>
  );
};

export default Layout;
