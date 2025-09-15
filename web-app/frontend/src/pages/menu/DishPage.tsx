import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { apiClient } from '../../utils/api';
import { formatPrice } from '../../utils/helpers';
import { useCartStore } from '../../stores/cart';
import { ArrowLeft, Plus, Minus, Star, Clock, Users } from 'lucide-react';

const DishPage: React.FC = () => {
  const { dishId } = useParams<{ dishId: string }>();
  const navigate = useNavigate();
  const { addToCart, cart } = useCartStore();
  const [quantity, setQuantity] = React.useState(1);

  const { data: dish, isLoading } = useQuery({
    queryKey: ['dish', dishId],
    queryFn: async () => {
      const response = await apiClient.get(`/menu/dish/${dishId}`);
      return response.data;
    },
    enabled: !!dishId,
  });

  const cartItem = cart.items.find(item => item.dish_id === parseInt(dishId || '0'));

  const handleAddToCart = async () => {
    if (dish && !dish.is_stop_list) {
      await addToCart(dish.id, quantity);
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

  if (!dish) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Блюдо не найдено
          </h2>
          <Button onClick={() => navigate('/menu')}>
            Вернуться к меню
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
          onClick={() => navigate('/menu')}
          className="mr-4"
        >
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{dish.dish_name}</h1>
          <p className="text-gray-600">{dish.dish_category}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Изображение */}
        <div>
          {dish.dish_image ? (
            <img
              src={dish.dish_image}
              alt={dish.dish_name}
              className="w-full h-64 lg:h-96 object-cover rounded-lg"
            />
          ) : (
            <div className="w-full h-64 lg:h-96 bg-gray-200 rounded-lg flex items-center justify-center">
              <span className="text-gray-400 text-lg">Фото недоступно</span>
            </div>
          )}
        </div>

        {/* Информация о блюде */}
        <div className="space-y-6">
          {/* Цена и статус */}
          <div className="flex items-center justify-between">
            <div className="text-3xl font-bold text-primary-600">
              {formatPrice(dish.dish_price)}
            </div>
            {dish.is_stop_list ? (
              <span className="px-3 py-1 bg-red-100 text-red-800 text-sm font-medium rounded-full">
                Нет в наличии
              </span>
            ) : (
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                В наличии
              </span>
            )}
          </div>

          {/* Описание */}
          {dish.dish_description && (
            <Card>
              <CardHeader>
                <CardTitle>Описание</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700">{dish.dish_description}</p>
              </CardContent>
            </Card>
          )}

          {/* Детали */}
          <Card>
            <CardHeader>
              <CardTitle>Детали</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {dish.dish_weight && (
                <div className="flex items-center space-x-2">
                  <Users className="h-4 w-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Вес: {dish.dish_weight}</span>
                </div>
              )}
              {dish.dish_calories && (
                <div className="flex items-center space-x-2">
                  <Star className="h-4 w-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Калории: {dish.dish_calories}</span>
                </div>
              )}
              {dish.dish_ingredients && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-1">Ингредиенты:</p>
                  <p className="text-sm text-gray-600">{dish.dish_ingredients}</p>
                </div>
              )}
              {dish.dish_allergens && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-1">Аллергены:</p>
                  <p className="text-sm text-red-600">{dish.dish_allergens}</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Добавление в корзину */}
          {!dish.is_stop_list && (
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    >
                      <Minus className="h-4 w-4" />
                    </Button>
                    <span className="w-8 text-center font-medium">{quantity}</span>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setQuantity(quantity + 1)}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                  
                  <Button
                    onClick={handleAddToCart}
                    className="flex-1"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Добавить в корзину
                  </Button>
                </div>
                
                {cartItem && (
                  <p className="text-sm text-gray-600 mt-2">
                    В корзине: {cartItem.quantity} шт.
                  </p>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default DishPage;
