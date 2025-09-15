import React from 'react';
import { useLocation } from 'react-router-dom';
import { useCartStore } from '../../stores/cart';
import { ShoppingCart, User, Menu } from 'lucide-react';

const Header: React.FC = () => {
  const location = useLocation();
  const { getCartCount } = useCartStore();
  const cartCount = getCartCount();

  const getPageTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Korean Chick';
      case '/menu':
        return 'Меню';
      case '/cart':
        return 'Корзина';
      case '/profile':
        return 'Профиль';
      case '/orders':
        return 'Мои заказы';
      case '/admin':
        return 'Админ-панель';
      default:
        return 'Korean Chick';
    }
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Логотип/Название */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">
              {getPageTitle()}
            </h1>
          </div>

          {/* Действия */}
          <div className="flex items-center space-x-4">
            {/* Корзина */}
            <div className="relative">
              <button className="p-2 text-gray-600 hover:text-gray-900 transition-colors">
                <ShoppingCart className="h-6 w-6" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </button>
            </div>

            {/* Профиль */}
            <button className="p-2 text-gray-600 hover:text-gray-900 transition-colors">
              <User className="h-6 w-6" />
            </button>

            {/* Меню */}
            <button className="p-2 text-gray-600 hover:text-gray-900 transition-colors">
              <Menu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
