import { useState, useCallback } from 'react';
import { VALIDATION_RULES } from '../config/constants';

const useValidation = () => {
  const [errors, setErrors] = useState({});

  const validateField = useCallback((name, value, rules = {}) => {
    const fieldErrors = [];

    // Required validation
    if (rules.required && (!value || value.trim() === '')) {
      fieldErrors.push(`${name} is required`);
    }

    // Min length validation
    if (rules.minLength && value && value.length < rules.minLength) {
      fieldErrors.push(`${name} must be at least ${rules.minLength} characters`);
    }

    // Max length validation
    if (rules.maxLength && value && value.length > rules.maxLength) {
      fieldErrors.push(`${name} must be no more than ${rules.maxLength} characters`);
    }

    // Pattern validation
    if (rules.pattern && value && !rules.pattern.test(value)) {
      fieldErrors.push(rules.message || `${name} format is invalid`);
    }

    // Custom validation
    if (rules.custom && value) {
      const customError = rules.custom(value);
      if (customError) {
        fieldErrors.push(customError);
      }
    }

    return fieldErrors;
  }, []);

  const validateForm = useCallback((formData, validationRules) => {
    const newErrors = {};

    Object.keys(validationRules).forEach(field => {
      const value = formData[field];
      const rules = validationRules[field];
      const fieldErrors = validateField(field, value, rules);
      
      if (fieldErrors.length > 0) {
        newErrors[field] = fieldErrors[0]; // Take first error
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [validateField]);

  const validateSingleField = useCallback((field, value, rules) => {
    const fieldErrors = validateField(field, value, rules);
    
    setErrors(prev => ({
      ...prev,
      [field]: fieldErrors.length > 0 ? fieldErrors[0] : null
    }));

    return fieldErrors.length === 0;
  }, [validateField]);

  const clearError = useCallback((field) => {
    setErrors(prev => ({
      ...prev,
      [field]: null
    }));
  }, []);

  const clearAllErrors = useCallback(() => {
    setErrors({});
  }, []);

  const hasError = useCallback((field) => {
    return !!errors[field];
  }, [errors]);

  const getError = useCallback((field) => {
    return errors[field] || null;
  }, [errors]);

  return {
    errors,
    validateForm,
    validateSingleField,
    clearError,
    clearAllErrors,
    hasError,
    getError
  };
};

export default useValidation;
