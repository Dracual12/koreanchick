import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/utils/api';
import { formatPrice } from '@/utils/helpers';
import { Menu, ShoppingCart, Star, TrendingUp } from 'lucide-react';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  // Получаем рекомендации
  const { data: recommendations, isLoading: recommendationsLoading } = useQuery({
    queryKey: ['recommendations'],
    queryFn: async () => {
      const response = await apiClient.get('/menu/recommendations');
      return response.data;
    },
  });

  // Получаем статистику пользователя
  const { data: userStats } = useQuery({
    queryKey: ['userStats'],
    queryFn: async () => {
      const response = await apiClient.get('/users/stats');
      return response.data;
    },
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Приветствие */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Добро пожаловать в Korean Chick! 🍗
        </h1>
        <p className="text-gray-600">
          Откройте для себя вкус настоящей корейской кухни
        </p>
      </div>

      {/* Быстрые действия */}
      <div className="grid grid-cols-2 gap-4 mb-8">
        <Button
          onClick={() => navigate('/menu')}
          className="h-20 flex flex-col items-center justify-center"
        >
          <Menu className="h-8 w-8 mb-2" />
          <span>Меню</span>
        </Button>
        <Button
          variant="secondary"
          onClick={() => navigate('/cart')}
          className="h-20 flex flex-col items-center justify-center"
        >
          <ShoppingCart className="h-8 w-8 mb-2" />
          <span>Корзина</span>
        </Button>
      </div>

      {/* Статистика пользователя */}
      {userStats && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Ваша статистика
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-primary-600">
                  {userStats.total_orders}
                </div>
                <div className="text-sm text-gray-500">Заказов</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">
                  {formatPrice(userStats.total_spent)}
                </div>
                <div className="text-sm text-gray-500">Потрачено</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">
                  {userStats.favorite_dishes.length}
                </div>
                <div className="text-sm text-gray-500">Любимых блюд</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Рекомендации */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Star className="h-5 w-5 mr-2" />
            Рекомендуем попробовать
          </CardTitle>
        </CardHeader>
        <CardContent>
          {recommendationsLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : recommendations && recommendations.length > 0 ? (
            <div className="space-y-4">
              {recommendations.slice(0, 3).map((rec: any) => (
                <div
                  key={rec.dish.id}
                  className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/menu/${rec.dish.id}`)}
                >
                  <div className="flex-shrink-0">
                    {rec.dish.dish_image ? (
                      <img
                        src={rec.dish.dish_image}
                        alt={rec.dish.dish_name}
                        className="h-16 w-16 rounded-lg object-cover"
                      />
                    ) : (
                      <div className="h-16 w-16 rounded-lg bg-gray-200 flex items-center justify-center">
                        <Menu className="h-8 w-8 text-gray-400" />
                      </div>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      {rec.dish.dish_name}
                    </h3>
                    <p className="text-sm text-gray-500 truncate">
                      {rec.reason}
                    </p>
                    <div className="flex items-center mt-1">
                      <span className="text-lg font-bold text-primary-600">
                        {formatPrice(rec.dish.dish_price)}
                      </span>
                      <span className="ml-2 text-sm text-gray-500">
                        Рейтинг: {rec.score.toFixed(1)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Menu className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Пока нет рекомендаций</p>
              <Button
                onClick={() => navigate('/menu')}
                className="mt-4"
              >
                Посмотреть меню
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default HomePage;
