import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const RedirectIfAuth = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      navigate('/dashboard', { replace: true }); // Redirige al dashboard si ya está logeado
    }
  }, [navigate]);

  return children;
};

export default RedirectIfAuth;
