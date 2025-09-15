import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Menu, ShoppingCart, User } from 'lucide-react';
import { useCartStore } from '../../stores/cart';

const BottomNavigation: React.FC = () => {
  const location = useLocation();
  const { getCartCount } = useCartStore();
  const cartCount = getCartCount();

  const navItems = [
    {
      path: '/',
      icon: Home,
      label: 'Главная',
    },
    {
      path: '/menu',
      icon: Menu,
      label: 'Меню',
    },
    {
      path: '/cart',
      icon: ShoppingCart,
      label: 'Корзина',
      badge: cartCount,
    },
    {
      path: '/profile',
      icon: User,
      label: 'Профиль',
    },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="flex items-center justify-around h-16">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
                isActive
                  ? 'text-primary-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="relative">
                <Icon className="h-6 w-6" />
                {item.badge && item.badge > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {item.badge}
                  </span>
                )}
              </div>
              <span className="text-xs mt-1">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNavigation;
