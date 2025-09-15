import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { apiClient } from '../../utils/api';
import { formatPrice } from '../../utils/helpers';
import { useAuthStore } from '../../stores/auth';

const HomePage = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Добро пожаловать в Korean Chick!
          </h1>
          <p className="text-gray-600">
            {user ? `Привет, ${user.first_name || 'Пользователь'}!` : 'Выберите действие'}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Меню</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Посмотрите наше меню и выберите блюда
              </p>
              <Button 
                onClick={() => navigate('/menu')}
                className="w-full"
              >
                Открыть меню
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Корзина</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Просмотрите товары в корзине
              </p>
              <Button 
                onClick={() => navigate('/cart')}
                variant="outline"
                className="w-full"
              >
                Открыть корзину
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Профиль</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Управляйте своим профилем
              </p>
              <Button 
                onClick={() => navigate('/profile')}
                variant="outline"
                className="w-full"
              >
                Открыть профиль
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
