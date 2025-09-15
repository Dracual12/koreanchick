import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Cart, CartItem } from '../types';
import { apiClient } from '../utils/api';

interface CartState {
  cart: Cart;
  isLoading: boolean;
  error: string | null;
}

interface CartActions {
  fetchCart: () => Promise<void>;
  addToCart: (dishId: number, quantity?: number) => Promise<void>;
  removeFromCart: (dishId: number, quantity?: number) => Promise<void>;
  updateCartItem: (dishId: number, quantity: number) => Promise<void>;
  clearCart: () => Promise<void>;
  getCartCount: () => number;
  getTotalPrice: () => number;
  setError: (error: string | null) => void;
}

type CartStore = CartState & CartActions;

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      // Состояние
      cart: {
        items: [],
        total_items: 0,
        total_price: 0,
        is_empty: true,
      },
      isLoading: false,
      error: null,

      // Действия
      fetchCart: async () => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.get('/cart/');
          if (response.success && response.data) {
            set({
              cart: response.data,
              isLoading: false,
            });
          } else {
            set({
              error: response.message || 'Ошибка загрузки корзины',
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Ошибка загрузки корзины',
            isLoading: false,
          });
        }
      },

      addToCart: async (dishId: number, quantity: number = 1) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.post('/cart/add', {
            dish_id: dishId,
            quantity,
            action: 'add',
          });
          if (response.success) {
            await get().fetchCart();
          } else {
            set({
              error: response.message || 'Ошибка добавления в корзину',
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Ошибка добавления в корзину',
            isLoading: false,
          });
        }
      },

      removeFromCart: async (dishId: number, quantity: number = 1) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.post('/cart/add', {
            dish_id: dishId,
            quantity,
            action: 'remove',
          });
          if (response.success) {
            await get().fetchCart();
          } else {
            set({
              error: response.message || 'Ошибка удаления из корзины',
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Ошибка удаления из корзины',
            isLoading: false,
          });
        }
      },

      updateCartItem: async (dishId: number, quantity: number) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.post('/cart/add', {
            dish_id: dishId,
            quantity,
            action: 'set',
          });
          if (response.success) {
            await get().fetchCart();
          } else {
            set({
              error: response.message || 'Ошибка обновления корзины',
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Ошибка обновления корзины',
            isLoading: false,
          });
        }
      },

      clearCart: async () => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.delete('/cart/clear');
          if (response.success) {
            set({
              cart: {
                items: [],
                total_items: 0,
                total_price: 0,
                is_empty: true,
              },
              isLoading: false,
            });
          } else {
            set({
              error: response.message || 'Ошибка очистки корзины',
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'Ошибка очистки корзины',
            isLoading: false,
          });
        }
      },

      getCartCount: () => {
        const { cart } = get();
        return cart.total_items;
      },

      getTotalPrice: () => {
        const { cart } = get();
        return cart.total_price;
      },

      setError: (error: string | null) => {
        set({ error });
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({
        cart: state.cart,
      }),
    }
  )
);
