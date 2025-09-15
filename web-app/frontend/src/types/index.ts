// Базовые типы
export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

// Пользователь
export interface User {
  id: number;
  user_id: number;
  first_name?: string;
  last_name?: string;
  username?: string;
  foodToMoodCoin?: number;
  is_banned: boolean;
  registration_date: string;
}

export interface TelegramUser {
  id: number;
  first_name?: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  is_premium: boolean;
  photo_url?: string;
}

export interface UserPreferences {
  mood?: string;
  hungry?: string;
  style?: string;
  sex?: string;
  age?: string;
  dish_style?: string;
  ccal?: string;
  dislike?: string;
  like?: string;
}

export interface UserStats {
  total_orders: number;
  total_spent: number;
  average_order_value: number;
  favorite_dishes: string[];
  last_order_date?: string;
}

// Блюда и меню
export interface Dish {
  id: number;
  dish_name: string;
  dish_price: number;
  dish_category?: string;
  dish_image?: string;
  dish_description?: string;
  dish_weight?: string;
  dish_calories?: number;
  dish_ingredients?: string;
  dish_allergens?: string;
  is_available: boolean;
  is_stop_list: boolean;
  rest_name: string;
  rest_address: string;
  iiko_id?: string;
}

export interface DishListItem {
  id: number;
  dish_name: string;
  dish_price: number;
  dish_image?: string;
  dish_category?: string;
  is_available: boolean;
  is_stop_list: boolean;
}

export interface Category {
  name: string;
  dishes: DishListItem[];
  total_count: number;
}

export interface Menu {
  categories: Category[];
  total_dishes: number;
  available_dishes: number;
}

export interface DishRecommendation {
  dish: Dish;
  score: number;
  reason: string;
  mood_match?: string;
  preference_match?: string;
}

// Корзина и заказы
export interface CartItem {
  dish_id: number;
  dish_name: string;
  quantity: number;
  price: number;
  total_price: number;
  options?: Record<string, any>;
}

export interface Cart {
  items: CartItem[];
  total_items: number;
  total_price: number;
  is_empty: boolean;
}

export interface OrderItem {
  dish_id: number;
  dish_name: string;
  quantity: number;
  price: number;
  total_price: number;
}

export interface Order {
  id: number;
  user_id: number;
  waiter_id?: number;
  table_number?: number;
  order_time: string;
  status: 'pending' | 'confirmed' | 'preparing' | 'ready' | 'completed' | 'cancelled';
  total_amount: number;
  items: OrderItem[];
  notes?: string;
  payment_method: string;
  qr_code?: string;
}

export interface OrderCreate {
  table_number?: number;
  notes?: string;
  payment_method: 'cash' | 'card' | 'qr';
}

// Админка
export interface AdminStats {
  total_users: number;
  total_orders: number;
  total_revenue: number;
  average_order_value: number;
  daily_stats: Record<string, { orders: number; revenue: number }>;
  popular_dishes: Array<[string, number]>;
}

// Telegram WebApp
export interface TelegramWebApp {
  initData: string;
  initDataUnsafe: {
    query_id?: string;
    user?: TelegramUser;
    auth_date?: number;
    hash?: string;
  };
  version: string;
  platform: string;
  colorScheme: 'light' | 'dark';
  themeParams: {
    bg_color?: string;
    text_color?: string;
    hint_color?: string;
    link_color?: string;
    button_color?: string;
    button_text_color?: string;
    secondary_bg_color?: string;
  };
  isExpanded: boolean;
  viewportHeight: number;
  viewportStableHeight: number;
  headerColor: string;
  backgroundColor: string;
  isClosingConfirmationEnabled: boolean;
  BackButton: {
    isVisible: boolean;
    onClick: (callback: () => void) => void;
    offClick: (callback: () => void) => void;
    show: () => void;
    hide: () => void;
  };
  MainButton: {
    text: string;
    color: string;
    textColor: string;
    isVisible: boolean;
    isProgressVisible: boolean;
    isActive: boolean;
    setText: (text: string) => void;
    onClick: (callback: () => void) => void;
    offClick: (callback: () => void) => void;
    show: () => void;
    hide: () => void;
    enable: () => void;
    disable: () => void;
    showProgress: (leaveActive?: boolean) => void;
    hideProgress: () => void;
    setParams: (params: {
      text?: string;
      color?: string;
      text_color?: string;
      is_active?: boolean;
      is_visible?: boolean;
    }) => void;
  };
  HapticFeedback: {
    impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
    notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
    selectionChanged: () => void;
  };
  ready: () => void;
  expand: () => void;
  close: () => void;
  sendData: (data: string) => void;
  switchInlineQuery: (query: string, choose_chat_types?: string[]) => void;
  openLink: (url: string, options?: { try_instant_view?: boolean }) => void;
  openTelegramLink: (url: string) => void;
  openInvoice: (url: string, callback?: (status: string) => void) => void;
  showPopup: (params: {
    title?: string;
    message: string;
    buttons?: Array<{
      id?: string;
      type?: 'default' | 'ok' | 'close' | 'cancel' | 'destructive';
      text?: string;
    }>;
  }, callback?: (buttonId: string) => void) => void;
  showAlert: (message: string, callback?: () => void) => void;
  showConfirm: (message: string, callback?: (confirmed: boolean) => void) => void;
  showScanQrPopup: (params: {
    text?: string;
  }, callback?: (text: string) => void) => void;
  closeScanQrPopup: () => void;
  readTextFromClipboard: (callback?: (text: string) => void) => void;
  requestWriteAccess: (callback?: (granted: boolean) => void) => void;
  requestContact: (callback?: (granted: boolean) => void) => void;
}

// Глобальные типы
declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp;
    };
  }
}
