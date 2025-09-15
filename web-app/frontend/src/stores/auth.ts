import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, TelegramUser } from '../types';
import { apiClient } from '../utils/api';

interface AuthState {
  user: User | null;
  telegramUser: TelegramUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: () => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  setTelegramUser: (telegramUser: TelegramUser) => void;
  clearError: () => void;
  checkAuth: () => Promise<void>;
}

type AuthStore = AuthState & AuthActions;

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      // Состояние
      user: null,
      telegramUser: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Действия
      login: async () => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.post('/auth/login');
          if (response.success && response.data) {
            set({
              user: response.data.user,
              telegramUser: response.data.telegram_user,
              isAuthenticated: true,
              isLoading: false,
            });
          } else {
            set({
              error: response.message || 'Ошибка авторизации',
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Ошибка авторизации',
            isLoading: false,
          });
        }
      },

      logout: () => {
        set({
          user: null,
          telegramUser: null,
          isAuthenticated: false,
          error: null,
        });
      },

      setUser: (user: User) => {
        set({ user, isAuthenticated: true });
      },

      setTelegramUser: (telegramUser: TelegramUser) => {
        set({ telegramUser });
      },

      clearError: () => {
        set({ error: null });
      },

      checkAuth: async () => {
        set({ isLoading: true });
        try {
          const response = await apiClient.get('/auth/me');
          if (response.success && response.data) {
            set({
              user: response.data.user,
              telegramUser: response.data.telegram_user,
              isAuthenticated: true,
              isLoading: false,
            });
          } else {
            set({
              isAuthenticated: false,
              isLoading: false,
            });
          }
        } catch (error) {
          set({
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        telegramUser: state.telegramUser,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
