// Утилиты для работы с данными

// Форматирование цены
export const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
  }).format(price);
};

// Форматирование даты
export const formatDate = (date: string | Date): string => {
  const d = new Date(date);
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(d);
};

// Обрезка текста
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

// Генерация случайного ID
export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9);
};

// Дебаунс функция
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: number | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeout !== null) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => func(...args), wait);
  };
};

// Проверка на пустое значение
export const isEmpty = (value: any): boolean => {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string') return value.trim() === '';
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value).length === 0;
  return false;
};

// Валидация email
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Валидация телефона
export const isValidPhone = (phone: string): boolean => {
  const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
};

// Утилита для объединения классов (cn)
export const cn = (...classes: (string | undefined | null | false)[]): string => {
  return classes.filter(Boolean).join(' ');
};

// Получение полного имени пользователя
export const getFullName = (user: { first_name?: string; last_name?: string; username?: string }): string => {
  const firstName = user.first_name || '';
  const lastName = user.last_name || '';
  const username = user.username || '';
  
  if (firstName && lastName) {
    return `${firstName} ${lastName}`;
  } else if (firstName) {
    return firstName;
  } else if (username) {
    return `@${username}`;
  }
  
  return 'Пользователь';
};

// Получение текста статуса заказа
export const getOrderStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'pending': 'Ожидает подтверждения',
    'confirmed': 'Подтвержден',
    'preparing': 'Готовится',
    'ready': 'Готов к выдаче',
    'delivered': 'Доставлен',
    'cancelled': 'Отменен'
  };
  
  return statusMap[status] || status;
};

// Получение цвета статуса заказа
export const getOrderStatusColor = (status: string): string => {
  const colorMap: Record<string, string> = {
    'pending': 'text-yellow-600 bg-yellow-100',
    'confirmed': 'text-blue-600 bg-blue-100',
    'preparing': 'text-orange-600 bg-orange-100',
    'ready': 'text-green-600 bg-green-100',
    'delivered': 'text-green-600 bg-green-100',
    'cancelled': 'text-red-600 bg-red-100'
  };
  
  return colorMap[status] || 'text-gray-600 bg-gray-100';
};
