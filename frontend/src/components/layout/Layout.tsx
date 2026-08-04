import React from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import { useWebSocket } from '../../hooks/useWebSocket';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  useWebSocket(); // Initialize websocket connection
  
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <TopBar />
        <div className="content-area">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
