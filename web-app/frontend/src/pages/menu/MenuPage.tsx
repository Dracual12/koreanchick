import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { apiClient } from '../../utils/api';
import { formatPrice } from '../../utils/helpers';
import { Search, Plus, Filter } from 'lucide-react';
import { useCartStore } from '../../stores/cart';

const MenuPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const { addToCart } = useCartStore();

  // Получаем меню
  const { data: menu, isLoading: menuLoading } = useQuery({
    queryKey: ['menu', selectedCategory],
    queryFn: async () => {
      const response = await apiClient.get('/menu/', {
        params: { category: selectedCategory || undefined }
      });
      return response.data;
    },
  });

  // Получаем категории
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await apiClient.get('/menu/categories');
      return response.data;
    },
  });

  // Поиск блюд
  const { data: searchResults, isLoading: searchLoading } = useQuery({
    queryKey: ['search', searchQuery],
    queryFn: async () => {
      if (!searchQuery.trim()) return null;
      const response = await apiClient.get('/menu/search', {
        params: { q: searchQuery }
      });
      return response.data;
    },
    enabled: !!searchQuery.trim(),
  });

  const handleAddToCart = async (dishId: number) => {
    try {
      await addToCart(dishId, 1);
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  const displayData = searchQuery.trim() ? searchResults : menu;
  const isLoading = searchQuery.trim() ? searchLoading : menuLoading;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Заголовок */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Меню</h1>
        <p className="text-gray-600">
          Выберите понравившиеся блюда и добавьте их в корзину
        </p>
      </div>

      {/* Поиск */}
      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <Input
            placeholder="Поиск блюд..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* Фильтр по категориям */}
      {categories && categories.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-3">
            <Filter className="h-5 w-5 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Категории:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              variant={selectedCategory === null ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setSelectedCategory(null)}
            >
              Все
            </Button>
            {categories.map((category: string) => (
              <Button
                key={category}
                variant={selectedCategory === category ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setSelectedCategory(category)}
              >
                {category}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Содержимое */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : displayData ? (
        <div className="space-y-6">
          {displayData.categories ? (
            // Отображение по категориям
            displayData.categories.map((category: any) => (
              <Card key={category.name}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{category.name}</span>
                    <span className="text-sm font-normal text-gray-500">
                      {category.total_count} блюд
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {category.dishes.map((dish: any) => (
                      <div
                        key={dish.id}
                        className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0">
                            {dish.dish_image ? (
                              <img
                                src={dish.dish_image}
                                alt={dish.dish_name}
                                className="h-16 w-16 rounded-lg object-cover"
                              />
                            ) : (
                              <div className="h-16 w-16 rounded-lg bg-gray-200 flex items-center justify-center">
                                <span className="text-gray-400 text-xs">Фото</span>
                              </div>
                            )}
                          </div>
                          <div className="flex-1 min-w-0">
                            <h3 className="text-sm font-medium text-gray-900 truncate">
                              {dish.dish_name}
                            </h3>
                            <p className="text-lg font-bold text-primary-600 mt-1">
                              {formatPrice(dish.dish_price)}
                            </p>
                            {dish.is_stop_list && (
                              <p className="text-xs text-red-600 mt-1">
                                Нет в наличии
                              </p>
                            )}
                          </div>
                        </div>
                        <div className="mt-3 flex space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => navigate(`/menu/${dish.id}`)}
                            className="flex-1"
                          >
                            Подробнее
                          </Button>
                          <Button
                            size="sm"
                            onClick={() => handleAddToCart(dish.id)}
                            disabled={dish.is_stop_list}
                            className="flex-1"
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            // Отображение результатов поиска
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {displayData.items?.map((dish: any) => (
                <Card key={dish.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        {dish.dish_image ? (
                          <img
                            src={dish.dish_image}
                            alt={dish.dish_name}
                            className="h-16 w-16 rounded-lg object-cover"
                          />
                        ) : (
                          <div className="h-16 w-16 rounded-lg bg-gray-200 flex items-center justify-center">
                            <span className="text-gray-400 text-xs">Фото</span>
                          </div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-sm font-medium text-gray-900 truncate">
                          {dish.dish_name}
                        </h3>
                        <p className="text-lg font-bold text-primary-600 mt-1">
                          {formatPrice(dish.dish_price)}
                        </p>
                        {dish.is_stop_list && (
                          <p className="text-xs text-red-600 mt-1">
                            Нет в наличии
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="mt-3 flex space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => navigate(`/menu/${dish.id}`)}
                        className="flex-1"
                      >
                        Подробнее
                      </Button>
                      <Button
                        size="sm"
                        onClick={() => handleAddToCart(dish.id)}
                        disabled={dish.is_stop_list}
                        className="flex-1"
                      >
                        <Plus className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500">Меню не найдено</p>
        </div>
      )}
    </div>
  );
};

export default MenuPage;
