import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../stores/auth';
import { getTelegramUser, initTelegramWebApp } from '../../utils/telegram';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading, error } = useAuthStore();

  useEffect(() => {
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Проверяем, есть ли пользователь Telegram
    const telegramUser = getTelegramUser();
    if (telegramUser) {
      // Автоматически логинимся
      handleLogin();
    }
  }, []);

  const handleLogin = async () => {
    try {
      await login();
      navigate('/');
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Korean Chick
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Добро пожаловать в наш ресторан
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-center">
              Вход в приложение
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <div className="text-center">
              <p className="text-sm text-gray-600 mb-4">
                Для входа в приложение необходимо авторизоваться через Telegram
              </p>
              
              <Button
                onClick={handleLogin}
                loading={isLoading}
                className="w-full"
                size="lg"
              >
                {isLoading ? 'Вход...' : 'Войти через Telegram'}
              </Button>
            </div>

            <div className="text-center">
              <p className="text-xs text-gray-500">
                Нажимая "Войти", вы соглашаетесь с условиями использования
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="text-center">
          <p className="text-sm text-gray-600">
            Если у вас возникли проблемы с входом, обратитесь в поддержку
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
