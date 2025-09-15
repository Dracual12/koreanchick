import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { apiClient } from '../../utils/api';
import { formatPrice, formatDate } from '../../utils/helpers';
import { useAuthStore } from '../../stores/auth';
import { 
  BarChart3, 
  Users, 
  ShoppingBag, 
  DollarSign, 
  TrendingUp,
  Package,
  AlertTriangle,
  Download
} from 'lucide-react';

const AdminPage: React.FC = () => {
  const { user } = useAuthStore();

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['adminStats'],
    queryFn: async () => {
      const response = await apiClient.get('/admin/stats');
      return response.data;
    },
  });

  const { data: recentOrders, isLoading: ordersLoading } = useQuery({
    queryKey: ['recentOrders'],
    queryFn: async () => {
      const response = await apiClient.get('/admin/orders?limit=10');
      return response.data;
    },
  });

  // Проверяем права администратора
  const isAdmin = user?.user_id === 1456241115; // ID администратора

  if (!isAdmin) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center py-12">
          <AlertTriangle className="h-24 w-24 mx-auto text-red-300 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Доступ запрещен
          </h2>
          <p className="text-gray-600">
            У вас нет прав для доступа к админ-панели
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Заголовок */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Админ-панель</h1>
        <p className="text-gray-600">Управление рестораном и статистика</p>
      </div>

      {/* Статистика */}
      {statsLoading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : stats ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Пользователи</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_users}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <ShoppingBag className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Заказы</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_orders}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Выручка</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatPrice(stats.total_revenue)}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Средний чек</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatPrice(stats.average_order_value)}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      ) : null}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Популярные блюда */}
        {stats && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Package className="h-5 w-5 mr-2" />
                Популярные блюда
              </CardTitle>
            </CardHeader>
            <CardContent>
              {stats.popular_dishes && stats.popular_dishes.length > 0 ? (
                <div className="space-y-3">
                  {stats.popular_dishes.slice(0, 5).map((dish: any, index: number) => (
                    <div key={index} className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{dish[0]}</p>
                        <p className="text-sm text-gray-500">{dish[1]} заказов</p>
                      </div>
                      <div className="text-right">
                        <span className="text-sm font-medium text-primary-600">
                          #{index + 1}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-4">Нет данных</p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Последние заказы */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <ShoppingBag className="h-5 w-5 mr-2" />
              Последние заказы
            </CardTitle>
          </CardHeader>
          <CardContent>
            {ordersLoading ? (
              <div className="flex items-center justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
              </div>
            ) : recentOrders && recentOrders.orders && recentOrders.orders.length > 0 ? (
              <div className="space-y-3">
                {recentOrders.orders.slice(0, 5).map((order: any) => (
                  <div key={order.id} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Заказ #{order.id}</p>
                      <p className="text-sm text-gray-500">
                        {formatDate(order.order_time)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">{formatPrice(order.total_amount)}</p>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        order.status === 'completed' ? 'bg-green-100 text-green-800' :
                        order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {order.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Нет заказов</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Действия */}
      <div className="mt-8">
        <Card>
          <CardHeader>
            <CardTitle>Действия</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-4">
              <Button variant="outline">
                <Download className="h-4 w-4 mr-2" />
                Экспорт данных
              </Button>
              <Button variant="outline">
                <Package className="h-4 w-4 mr-2" />
                Управление меню
              </Button>
              <Button variant="outline">
                <Users className="h-4 w-4 mr-2" />
                Управление пользователями
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminPage;
