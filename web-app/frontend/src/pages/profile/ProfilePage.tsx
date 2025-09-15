import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { apiClient } from '../../utils/api';
import { formatPrice, formatDate, getFullName } from '../../utils/helpers';
import { useAuthStore } from '../../stores/auth';
import { User, ShoppingBag, TrendingUp, Star, Settings } from 'lucide-react';

const ProfilePage: React.FC = () => {
  const { user, telegramUser } = useAuthStore();

  const { data: userStats } = useQuery({
    queryKey: ['userStats'],
    queryFn: async () => {
      const response = await apiClient.get('/users/stats');
      return response.data;
    },
  });

  const { data: preferences } = useQuery({
    queryKey: ['userPreferences'],
    queryFn: async () => {
      const response = await apiClient.get('/users/preferences');
      return response.data;
    },
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Заголовок */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Профиль</h1>
        <p className="text-gray-600">Управление вашим аккаунтом и настройками</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Информация о пользователе */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <User className="h-5 w-5 mr-2" />
                Личная информация
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Имя</label>
                  <p className="text-lg font-medium text-gray-900">
                    {getFullName(user?.first_name, user?.last_name) || 'Не указано'}
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Username</label>
                  <p className="text-lg font-medium text-gray-900">
                    @{user?.username || 'Не указано'}
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Дата регистрации</label>
                  <p className="text-lg font-medium text-gray-900">
                    {user?.registration_date ? formatDate(user.registration_date) : 'Не указано'}
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Бонусные баллы</label>
                  <p className="text-lg font-medium text-primary-600">
                    {user?.foodToMoodCoin || 0} баллов
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Предпочтения */}
          {preferences && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Settings className="h-5 w-5 mr-2" />
                  Ваши предпочтения
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  {preferences.mood && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Настроение</label>
                      <p className="text-sm text-gray-900">{preferences.mood}</p>
                    </div>
                  )}
                  {preferences.hungry && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Голод</label>
                      <p className="text-sm text-gray-900">{preferences.hungry}</p>
                    </div>
                  )}
                  {preferences.style && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Стиль</label>
                      <p className="text-sm text-gray-900">{preferences.style}</p>
                    </div>
                  )}
                  {preferences.age && (
                    <div>
                      <label className="text-sm font-medium text-gray-500">Возраст</label>
                      <p className="text-sm text-gray-900">{preferences.age}</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Статистика */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2" />
                Статистика
              </CardTitle>
            </CardHeader>
            <CardContent>
              {userStats ? (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-primary-600">
                      {userStats.total_orders}
                    </div>
                    <div className="text-sm text-gray-500">Всего заказов</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {formatPrice(userStats.total_spent)}
                    </div>
                    <div className="text-sm text-gray-500">Потрачено</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {formatPrice(userStats.average_order_value)}
                    </div>
                    <div className="text-sm text-gray-500">Средний чек</div>
                  </div>
                  
                  {userStats.favorite_dishes.length > 0 && (
                    <div>
                      <div className="text-sm font-medium text-gray-700 mb-2">
                        Любимые блюда:
                      </div>
                      <div className="space-y-1">
                        {userStats.favorite_dishes.slice(0, 3).map((dish: string, index: number) => (
                          <div key={index} className="text-sm text-gray-600">
                            {dish}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Быстрые действия */}
          <Card>
            <CardHeader>
              <CardTitle>Быстрые действия</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start">
                <ShoppingBag className="h-4 w-4 mr-2" />
                Мои заказы
              </Button>
              
              <Button variant="outline" className="w-full justify-start">
                <Star className="h-4 w-4 mr-2" />
                Избранное
              </Button>
              
              <Button variant="outline" className="w-full justify-start">
                <Settings className="h-4 w-4 mr-2" />
                Настройки
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
