import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const StatsCard = ({ 
  title, 
  value, 
  change, 
  changeType = 'neutral', // 'positive', 'negative', 'neutral'
  icon: Icon,
  description,
  className = ''
}) => {
  const changeColors = {
    positive: 'text-green-600 bg-green-100',
    negative: 'text-red-600 bg-red-100',
    neutral: 'text-gray-600 bg-gray-100'
  };

  const darkChangeColors = {
    positive: 'dark:text-green-400 dark:bg-green-900/20',
    negative: 'dark:text-red-400 dark:bg-red-900/20',
    neutral: 'dark:text-gray-400 dark:bg-gray-900/20'
  };

  const changeIcons = {
    positive: TrendingUp,
    negative: TrendingDown,
    neutral: Minus
  };

  const ChangeIcon = changeIcons[changeType];

  return (
    <Card className={`transition-all duration-300 hover:shadow-lg ${className}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        {Icon && (
          <Icon className="h-4 w-4 text-muted-foreground" />
        )}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">
            {description}
          </p>
        )}
        {change && (
          <div className="flex items-center gap-1 mt-2">
            <Badge 
              variant="secondary" 
              className={`text-xs ${changeColors[changeType]} ${darkChangeColors[changeType]}`}
            >
              <ChangeIcon className="w-3 h-3 mr-1" />
              {change}
            </Badge>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default StatsCard;
