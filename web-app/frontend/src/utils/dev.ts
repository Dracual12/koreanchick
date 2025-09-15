// Утилиты для режима разработки

// Моковые данные для локальной разработки
export const mockTelegramUser = {
  id: 123456789,
  first_name: 'Test',
  last_name: 'User',
  username: 'testuser',
  language_code: 'ru',
  is_premium: false,
  photo_url: null
};

// Проверка, находимся ли мы в режиме разработки
export const isDevelopment = (): boolean => {
  return import.meta.env.DEV || window.location.hostname === 'localhost';
};

// Получение моковых данных Telegram WebApp
export const getMockTelegramWebApp = () => {
  return {
    initData: 'user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Afalse%7D&chat_instance=-123456789&chat_type=sender&auth_date=1234567890&hash=mock_hash',
    initDataUnsafe: {
      user: mockTelegramUser
    },
    version: '6.0',
    platform: 'web',
    colorScheme: 'light',
    themeParams: {
      bg_color: '#ffffff',
      text_color: '#000000',
      hint_color: '#999999',
      link_color: '#2481cc',
      button_color: '#2481cc',
      button_text_color: '#ffffff',
      secondary_bg_color: '#f1f1f1'
    },
    isExpanded: true,
    viewportHeight: 600,
    viewportStableHeight: 600,
    headerColor: '#ffffff',
    backgroundColor: '#ffffff',
    isClosingConfirmationEnabled: false,
    isVerticalSwipesEnabled: true,
    ready: () => console.log('Mock Telegram WebApp ready'),
    expand: () => console.log('Mock Telegram WebApp expanded'),
    close: () => console.log('Mock Telegram WebApp close'),
    sendData: (data: string) => console.log('Mock sendData:', data),
    showAlert: (message: string, callback?: () => void) => {
      alert(message);
      if (callback) callback();
    },
    showConfirm: (message: string, callback?: (confirmed: boolean) => void) => {
      const confirmed = confirm(message);
      if (callback) callback(confirmed);
    },
    MainButton: {
      text: '',
      color: '#2481cc',
      textColor: '#ffffff',
      isVisible: false,
      isActive: true,
      isProgressVisible: false,
      setText: (text: string) => console.log('Mock MainButton setText:', text),
      onClick: (callback: () => void) => console.log('Mock MainButton onClick'),
      show: () => console.log('Mock MainButton show'),
      hide: () => console.log('Mock MainButton hide'),
      enable: () => console.log('Mock MainButton enable'),
      disable: () => console.log('Mock MainButton disable'),
      showProgress: () => console.log('Mock MainButton showProgress'),
      hideProgress: () => console.log('Mock MainButton hideProgress')
    },
    BackButton: {
      isVisible: false,
      onClick: (callback: () => void) => console.log('Mock BackButton onClick'),
      show: () => console.log('Mock BackButton show'),
      hide: () => console.log('Mock BackButton hide')
    },
    HapticFeedback: {
      impactOccurred: (style: 'light' | 'medium' | 'heavy') => console.log('Mock HapticFeedback impact:', style),
      notificationOccurred: (type: 'error' | 'success' | 'warning') => console.log('Mock HapticFeedback notification:', type),
      selectionChanged: () => console.log('Mock HapticFeedback selection')
    }
  };
};

// Инициализация мокового Telegram WebApp для разработки
export const initMockTelegramWebApp = (): void => {
  if (isDevelopment() && !window.Telegram?.WebApp) {
    console.log('🚀 Инициализация мокового Telegram WebApp для разработки');
    
    // Создаем моковый объект Telegram
    (window as any).Telegram = {
      WebApp: getMockTelegramWebApp()
    };
  }
};
