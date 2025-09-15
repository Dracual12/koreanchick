import { TelegramWebApp, TelegramUser } from '../types';
import { isDevelopment, getMockTelegramWebApp } from './dev';

// Получение экземпляра Telegram WebApp
export const getTelegramWebApp = (): TelegramWebApp | null => {
  // Инициализируем мок для разработки
  if (isDevelopment()) {
    return getMockTelegramWebApp() as unknown as TelegramWebApp;
  }
  
  // В продакшене используем реальный Telegram WebApp
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    return window.Telegram.WebApp;
  }
  
  return null;
};

// Получение данных пользователя
export const getTelegramUser = (): TelegramUser | null => {
  const webApp = getTelegramWebApp();
  if (!webApp) return null;
  
  return webApp.initDataUnsafe?.user || null;
};

// Получение initData
export const getInitData = (): string => {
  const webApp = getTelegramWebApp();
  return webApp?.initData || '';
};

// Проверка, что мы в Telegram WebApp
export const isTelegramWebApp = (): boolean => {
  return getTelegramWebApp() !== null;
};
