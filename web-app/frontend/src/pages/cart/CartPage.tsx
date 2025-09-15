import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { apiClient } from '../../utils/api';
import { formatPrice } from '../../utils/helpers';
import { useCartStore } from '../../stores/cart';
import { Minus, Plus, Trash2, ShoppingBag } from 'lucide-react';

const CartPage: React.FC = () => {
  const navigate = useNavigate();
  const { cart, updateCartItem, removeFromCart, clearCart, isLoading } = useCartStore();

  const handleQuantityChange = async (dishId: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      await removeFromCart(dishId, 1);
    } else {
      await updateCartItem(dishId, newQuantity);
    }
  };

  const handleRemoveItem = async (dishId: number) => {
    await removeFromCart(dishId, 1);
  };

  const handleClearCart = async () => {
    if (window.confirm('Вы уверены, что хотите очистить корзину?')) {
      await clearCart();
    }
  };

  if (cart.is_empty) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center py-12">
          <ShoppingBag className="h-24 w-24 mx-auto text-gray-300 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Корзина пуста
          </h2>
          <p className="text-gray-600 mb-6">
            Добавьте блюда из меню, чтобы сделать заказ
          </p>
          <Button onClick={() => navigate('/menu')}>
            Перейти к меню
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Заголовок */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Корзина</h1>
          <p className="text-gray-600">
            {cart.total_items} {cart.total_items === 1 ? 'товар' : 'товаров'} на сумму {formatPrice(cart.total_price)}
          </p>
        </div>
        {cart.items.length > 0 && (
          <Button
            variant="danger"
            size="sm"
            onClick={handleClearCart}
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Очистить
          </Button>
        )}
      </div>

      {/* Список товаров */}
      <div className="space-y-4 mb-6">
        {cart.items.map((item) => (
          <Card key={item.dish_id}>
            <CardContent className="p-4">
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-gray-900">
                    {item.dish_name}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {formatPrice(item.price)} за шт.
                  </p>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleQuantityChange(item.dish_id, item.quantity - 1)}
                    disabled={isLoading}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  
                  <span className="w-8 text-center font-medium">
                    {item.quantity}
                  </span>
                  
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleQuantityChange(item.dish_id, item.quantity + 1)}
                    disabled={isLoading}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="text-right">
                  <p className="text-lg font-bold text-primary-600">
                    {formatPrice(item.total_price)}
                  </p>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => handleRemoveItem(item.dish_id)}
                    disabled={isLoading}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Итого */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Итого
              </h3>
              <p className="text-sm text-gray-500">
                {cart.total_items} {cart.total_items === 1 ? 'товар' : 'товаров'}
              </p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-primary-600">
                {formatPrice(cart.total_price)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Кнопки действий */}
      <div className="flex space-x-4">
        <Button
          variant="outline"
          onClick={() => navigate('/menu')}
          className="flex-1"
        >
          Продолжить покупки
        </Button>
        <Button
          onClick={() => navigate('/checkout')}
          className="flex-1"
          disabled={isLoading}
        >
          Оформить заказ
        </Button>
      </div>
    </div>
  );
};

export default CartPage;
