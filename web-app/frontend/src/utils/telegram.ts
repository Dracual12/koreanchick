import { TelegramWebApp, TelegramUser } from '../types';
import { isDevelopment, initMockTelegramWebApp } from './dev';

// Получение экземпляра Telegram WebApp
export const getTelegramWebApp = (): TelegramWebApp | null => {
  // Инициализируем мок для разработки
  if (isDevelopment()) {
    initMockTelegramWebApp();
  }
  
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    return window.Telegram.WebApp;
  }
  return null;
};

// Инициализация Telegram WebApp
export const initTelegramWebApp = (): void => {
  const tg = getTelegramWebApp();
  if (tg) {
    tg.ready();
    tg.expand();
    
    // Настраиваем тему
    document.documentElement.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
    document.documentElement.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
    document.documentElement.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color || '#999999');
    document.documentElement.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color || '#2481cc');
    document.documentElement.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#2481cc');
    document.documentElement.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
    document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', tg.themeParams.secondary_bg_color || '#f1f1f1');
  }
};

// Получение данных пользователя из Telegram
export const getTelegramUser = (): TelegramUser | null => {
  const tg = getTelegramWebApp();
  if (tg?.initDataUnsafe?.user) {
    return tg.initDataUnsafe.user;
  }
  return null;
};

// Получение initData
export const getInitData = (): string => {
  const tg = getTelegramWebApp();
  return tg?.initData || '';
};

// Вибрация
export const hapticFeedback = {
  light: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.impactOccurred('light');
  },
  medium: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.impactOccurred('medium');
  },
  heavy: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.impactOccurred('heavy');
  },
  success: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.notificationOccurred('success');
  },
  error: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.notificationOccurred('error');
  },
  warning: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.notificationOccurred('warning');
  },
  selection: () => {
    const tg = getTelegramWebApp();
    tg?.HapticFeedback?.selectionChanged();
  },
};

// Управление главной кнопкой
export const mainButton = {
  show: (text: string, onClick: () => void) => {
    const tg = getTelegramWebApp();
    if (tg?.MainButton) {
      tg.MainButton.setText(text);
      tg.MainButton.show();
      tg.MainButton.onClick(onClick);
    }
  },
  hide: () => {
    const tg = getTelegramWebApp();
    tg?.MainButton?.hide();
  },
  setText: (text: string) => {
    const tg = getTelegramWebApp();
    tg?.MainButton?.setText(text);
  },
  enable: () => {
    const tg = getTelegramWebApp();
    tg?.MainButton?.enable();
  },
  disable: () => {
    const tg = getTelegramWebApp();
    tg?.MainButton?.disable();
  },
  showProgress: () => {
    const tg = getTelegramWebApp();
    tg?.MainButton?.showProgress();
  },
  hideProgress: () => {
    const tg = getTelegramWebApp();
    tg?.MainButton?.hideProgress();
  },
};

// Управление кнопкой "Назад"
export const backButton = {
  show: (onClick: () => void) => {
    const tg = getTelegramWebApp();
    if (tg?.BackButton) {
      tg.BackButton.show();
      tg.BackButton.onClick(onClick);
    }
  },
  hide: () => {
    const tg = getTelegramWebApp();
    tg?.BackButton?.hide();
  },
};

// Показ уведомлений
export const showAlert = (message: string): Promise<void> => {
  return new Promise((resolve) => {
    const tg = getTelegramWebApp();
    if (tg?.showAlert) {
      tg.showAlert(message, resolve);
    } else {
      alert(message);
      resolve();
    }
  });
};

export const showConfirm = (message: string): Promise<boolean> => {
  return new Promise((resolve) => {
    const tg = getTelegramWebApp();
    if (tg?.showConfirm) {
      tg.showConfirm(message, resolve);
    } else {
      resolve(confirm(message));
    }
  });
};

// Закрытие приложения
export const closeApp = (): void => {
  const tg = getTelegramWebApp();
  tg?.close();
};

// Отправка данных в бот
export const sendDataToBot = (data: string): void => {
  const tg = getTelegramWebApp();
  tg?.sendData(data);
};

// Проверка, запущено ли приложение в Telegram
export const isTelegramWebApp = (): boolean => {
  return typeof window !== 'undefined' && !!window.Telegram?.WebApp;
};

// Получение информации о платформе
export const getPlatform = (): string => {
  const tg = getTelegramWebApp();
  return tg?.platform || 'unknown';
};

// Получение версии WebApp
export const getVersion = (): string => {
  const tg = getTelegramWebApp();
  return tg?.version || 'unknown';
};
