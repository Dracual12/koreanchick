import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { isTelegramWebApp } from './utils/telegram';
import { useAuthStore } from './stores/auth';
import HomePage from './pages/HomePage';
import LoginPage from './pages/auth/LoginPage';
import AdminPage from './pages/admin/AdminPage';
import CartPage from './pages/cart/CartPage';
import ProfilePage from './pages/profile/ProfilePage';
import DishPage from './pages/menu/DishPage';
import './App.css';

function App() {
  const { isLoading, checkAuth } = useAuthStore();

  useEffect(() => {
    // Проверяем аутентификацию при загрузке
    checkAuth();
  }, [checkAuth]);

  // Показываем загрузку пока проверяем аутентификацию
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/dish/:id" element={<DishPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
