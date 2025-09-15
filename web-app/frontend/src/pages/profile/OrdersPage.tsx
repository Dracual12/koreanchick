import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { apiClient } from '../../utils/api';
import { formatPrice, formatDate, getOrderStatusText, getOrderStatusColor } from '../../utils/helpers';
import { Package, Clock, CheckCircle, XCircle } from 'lucide-react';

const OrdersPage: React.FC = () => {
  const { data: orders, isLoading } = useQuery({
    queryKey: ['userOrders'],
    queryFn: async () => {
      const response = await apiClient.get('/orders/');
      return response.data;
    },
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'cancelled':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'pending':
      case 'confirmed':
      case 'preparing':
      case 'ready':
        return <Clock className="h-5 w-5 text-yellow-600" />;
      default:
        return <Package className="h-5 w-5 text-gray-600" />;
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Заголовок */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Мои заказы</h1>
        <p className="text-gray-600">История ваших заказов</p>
      </div>

      {orders && orders.orders && orders.orders.length > 0 ? (
        <div className="space-y-6">
          {orders.orders.map((order: any) => (
            <Card key={order.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center">
                      {getStatusIcon(order.status)}
                      <span className="ml-2">Заказ #{order.id}</span>
                    </CardTitle>
                    <p className="text-sm text-gray-500 mt-1">
                      {formatDate(order.order_time)}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-primary-600">
                      {formatPrice(order.total_amount)}
                    </div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getOrderStatusColor(order.status)}`}>
                      {getOrderStatusText(order.status)}
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {/* Товары в заказе */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Товары:</h4>
                    <div className="space-y-1">
                      {order.items.map((item: any, index: number) => (
                        <div key={index} className="flex items-center justify-between text-sm">
                          <span>{item.dish_name} × {item.quantity}</span>
                          <span className="font-medium">{formatPrice(item.total_price)}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Дополнительная информация */}
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    {order.table_number && (
                      <div>
                        <span className="text-gray-500">Стол:</span>
                        <span className="ml-2 font-medium">{order.table_number}</span>
                      </div>
                    )}
                    <div>
                      <span className="text-gray-500">Оплата:</span>
                      <span className="ml-2 font-medium">
                        {order.payment_method === 'cash' ? 'Наличные' : 
                         order.payment_method === 'card' ? 'Карта' : 'QR-код'}
                      </span>
                    </div>
                  </div>

                  {order.notes && (
                    <div>
                      <span className="text-sm text-gray-500">Комментарий:</span>
                      <p className="text-sm text-gray-700 mt-1">{order.notes}</p>
                    </div>
                  )}

                  {/* QR-код если есть */}
                  {order.qr_code && (
                    <div className="text-center">
                      <img
                        src={order.qr_code}
                        alt="QR код заказа"
                        className="mx-auto h-32 w-32"
                      />
                      <p className="text-xs text-gray-500 mt-2">
                        Покажите QR-код официанту
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <Package className="h-24 w-24 mx-auto text-gray-300 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Заказов пока нет
          </h2>
          <p className="text-gray-600 mb-6">
            Сделайте свой первый заказ, чтобы увидеть его здесь
          </p>
          <Button onClick={() => window.location.href = '/menu'}>
            Перейти к меню
          </Button>
        </div>
      )}
    </div>
  );
};

export default OrdersPage;
