import React from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';
import { Button } from './ui/button';

const NotificationToast = ({ 
  type = 'info', 
  title, 
  message, 
  onClose, 
  actions = [],
  duration = 4000 
}) => {
  const icons = {
    success: CheckCircle,
    error: XCircle,
    warning: AlertCircle,
    info: Info
  };

  const colors = {
    success: 'text-green-600 bg-green-50 border-green-200',
    error: 'text-red-600 bg-red-50 border-red-200',
    warning: 'text-yellow-600 bg-yellow-50 border-yellow-200',
    info: 'text-blue-600 bg-blue-50 border-blue-200'
  };

  const darkColors = {
    success: 'dark:text-green-400 dark:bg-green-900/20 dark:border-green-800',
    error: 'dark:text-red-400 dark:bg-red-900/20 dark:border-red-800',
    warning: 'dark:text-yellow-400 dark:bg-yellow-900/20 dark:border-yellow-800',
    info: 'dark:text-blue-400 dark:bg-blue-900/20 dark:border-blue-800'
  };

  const Icon = icons[type];
  const colorClasses = `${colors[type]} ${darkColors[type]}`;

  React.useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose?.();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  return (
    <div className={`max-w-sm w-full border rounded-lg shadow-lg p-4 transition-all duration-300 ${colorClasses}`}>
      <div className="flex items-start gap-3">
        <Icon className="w-5 h-5 mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          {title && (
            <h4 className="font-semibold text-sm mb-1">
              {title}
            </h4>
          )}
          {message && (
            <p className="text-sm opacity-90">
              {message}
            </p>
          )}
          {actions.length > 0 && (
            <div className="flex gap-2 mt-3">
              {actions.map((action, index) => (
                <Button
                  key={index}
                  size="sm"
                  variant={action.variant || 'outline'}
                  onClick={action.onClick}
                  className="h-7 text-xs"
                >
                  {action.label}
                </Button>
              ))}
            </div>
          )}
        </div>
        <Button
          size="sm"
          variant="ghost"
          onClick={onClose}
          className="h-6 w-6 p-0 flex-shrink-0 opacity-70 hover:opacity-100"
        >
          <X className="w-3 h-3" />
        </Button>
      </div>
    </div>
  );
};

export default NotificationToast;
