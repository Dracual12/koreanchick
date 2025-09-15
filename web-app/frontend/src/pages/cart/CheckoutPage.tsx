import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { apiClient } from '../../utils/api';
import { formatPrice } from '../../utils/helpers';
import { useCartStore } from '../../stores/cart';
import { ArrowLeft, CreditCard, Smartphone, QrCode } from 'lucide-react';

const CheckoutPage: React.FC = () => {
  const navigate = useNavigate();
  const { cart, clearCart } = useCartStore();
  const [tableNumber, setTableNumber] = useState('');
  const [notes, setNotes] = useState('');
  const [paymentMethod, setPaymentMethod] = useState<'cash' | 'card' | 'qr'>('cash');

  const createOrderMutation = useMutation({
    mutationFn: async (orderData: any) => {
      const response = await apiClient.post('/orders/create', orderData);
      return response.data;
    },
    onSuccess: (order) => {
      // Очищаем корзину после успешного заказа
      clearCart();
      // Перенаправляем на страницу заказа
      navigate(`/orders/${order.id}`);
    },
    onError: (error: any) => {
      console.error('Order creation error:', error);
      alert('Ошибка при создании заказа: ' + (error.response?.data?.detail || 'Неизвестная ошибка'));
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (cart.is_empty) {
      alert('Корзина пуста');
      return;
    }

    const orderData = {
      table_number: tableNumber ? parseInt(tableNumber) : undefined,
      notes: notes.trim() || undefined,
      payment_method: paymentMethod,
    };

    createOrderMutation.mutate(orderData);
  };

  if (cart.is_empty) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Корзина пуста
          </h2>
          <p className="text-gray-600 mb-6">
            Добавьте блюда в корзину, чтобы оформить заказ
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
      <div className="flex items-center mb-6">
        <Button
          variant="ghost"
          onClick={() => navigate('/cart')}
          className="mr-4"
        >
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Оформление заказа</h1>
          <p className="text-gray-600">Заполните данные для завершения заказа</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Информация о заказе */}
        <Card>
          <CardHeader>
            <CardTitle>Ваш заказ</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {cart.items.map((item) => (
                <div key={item.dish_id} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{item.dish_name}</p>
                    <p className="text-sm text-gray-500">
                      {item.quantity} × {formatPrice(item.price)}
                    </p>
                  </div>
                  <p className="font-bold">{formatPrice(item.total_price)}</p>
                </div>
              ))}
            </div>
            <div className="border-t pt-3 mt-3">
              <div className="flex items-center justify-between">
                <p className="text-lg font-semibold">Итого:</p>
                <p className="text-xl font-bold text-primary-600">
                  {formatPrice(cart.total_price)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Номер стола */}
        <Card>
          <CardHeader>
            <CardTitle>Номер стола</CardTitle>
          </CardHeader>
          <CardContent>
            <Input
              type="number"
              placeholder="Введите номер стола (необязательно)"
              value={tableNumber}
              onChange={(e) => setTableNumber(e.target.value)}
              min="1"
            />
          </CardContent>
        </Card>

        {/* Способ оплаты */}
        <Card>
          <CardHeader>
            <CardTitle>Способ оплаты</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="radio"
                  name="payment"
                  value="cash"
                  checked={paymentMethod === 'cash'}
                  onChange={(e) => setPaymentMethod(e.target.value as 'cash')}
                  className="text-primary-600"
                />
                <CreditCard className="h-5 w-5 text-gray-500" />
                <span>Наличные</span>
              </label>
              
              <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="radio"
                  name="payment"
                  value="card"
                  checked={paymentMethod === 'card'}
                  onChange={(e) => setPaymentMethod(e.target.value as 'card')}
                  className="text-primary-600"
                />
                <Smartphone className="h-5 w-5 text-gray-500" />
                <span>Банковская карта</span>
              </label>
              
              <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="radio"
                  name="payment"
                  value="qr"
                  checked={paymentMethod === 'qr'}
                  onChange={(e) => setPaymentMethod(e.target.value as 'qr')}
                  className="text-primary-600"
                />
                <QrCode className="h-5 w-5 text-gray-500" />
                <span>QR-код</span>
              </label>
            </div>
          </CardContent>
        </Card>

        {/* Комментарии */}
        <Card>
          <CardHeader>
            <CardTitle>Комментарии к заказу</CardTitle>
          </CardHeader>
          <CardContent>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={3}
              placeholder="Дополнительные пожелания к заказу..."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </CardContent>
        </Card>

        {/* Кнопки */}
        <div className="flex space-x-4">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/cart')}
            className="flex-1"
          >
            Назад к корзине
          </Button>
          <Button
            type="submit"
            loading={createOrderMutation.isPending}
            className="flex-1"
          >
            {createOrderMutation.isPending ? 'Создание заказа...' : 'Оформить заказ'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default CheckoutPage;
