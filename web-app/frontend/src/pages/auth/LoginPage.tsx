import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTelegramUser, isTelegramWebApp } from '../../utils/telegram';
import { useAuthStore } from '../../stores/auth';
import { Button } from '../../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';

const LoginPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuthStore();

  const handleTelegramLogin = async () => {
    setIsLoading(true);
    try {
      const telegramUser = getTelegramUser();
      if (telegramUser) {
        await login();
        navigate('/');
      } else {
        alert('Не удалось получить данные пользователя из Telegram');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Ошибка входа');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuestLogin = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center">Вход в приложение</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {isTelegramWebApp() ? (
            <Button
              onClick={handleTelegramLogin}
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? 'Вход...' : 'Войти через Telegram'}
            </Button>
          ) : (
            <div className="text-center text-gray-600">
              <p>Откройте приложение в Telegram</p>
            </div>
          )}
          
          <Button
            onClick={handleGuestLogin}
            variant="outline"
            className="w-full"
          >
            Продолжить как гость
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;
