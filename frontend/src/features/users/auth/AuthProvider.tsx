import { useEffect, useState, type ReactNode } from "react";
import axios from "axios";
import { AuthContext } from "./authContext";

type AuthProviderProps = {
  children: ReactNode;
};
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true
});

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [errorMessageFromServer, setErrorMessageFromServer] = useState<string | null>(null);
  const [isRehydrating, setIsRehydrating] = useState(true);
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const response = await api.post(
        '/auth/login',
        params,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      setToken(response.data.access_token);
      setIsLoggedIn(true);
      return true;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (err.response?.data?.error_code === "INVALID_PASSWORD_OR_EMAIL") {
          setErrorMessageFromServer("メールアドレスまたはパスワードが正しくありません");
        } else {
          setErrorMessageFromServer("ログインに失敗しました");
        }
      }
      else {
        console.error("予期しないエラー", err);
      }
      setToken(null);
      setIsLoggedIn(false);
      return false;
    }
  }

  const logout = async (): Promise<boolean> => {
    try {
      await api.delete(
        '/auth/logout',
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      setToken(null);
      setIsLoggedIn(false);
      return true;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        return false;
      } else {
        console.error("予期しないエラー", err);
        return false;
      }

    }
  };

  const validateAccessToken = (): boolean => {
    const isValid = isLoggedIn && token !== null;
    return isValid;
  }

  const sendResetEmailAndComplete = async (email: string): Promise<void> => {
    try {
      await api.post(
        '/auth/password-reset/request',
        {
          email: email,
        }
      );
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        const errorCode = e.response?.data?.error_code;
        const errorMessage = e.response?.data?.error_message;
        console.error(errorCode + " " + errorMessage);
      } else {
        console.error("予期しないエラー", e);
      }
    }
  }
  const verifyPasswordResetLink = async (token: string): Promise<void> => {
    try {
      await api.get("/auth/password-reset/verification", { params: { token } })
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        const errorCode = e.response?.data?.error_code;
        const errorMessage = e.response?.data?.error_message;
        console.error(errorMessage);
        throw new Error(errorCode || "UNKNOWN_ERROR");
      } else {
        console.error("予期しないエラー", e);
        throw new Error("UNKNOWN_ERROR");
      }
    }
  }

  const canResetPassword = async (password: string, token: string | null): Promise<boolean> => {
    try {
      await api.put(
        '/auth/password-reset',
        {
          password,
          token
        }
      );
      setIsLoggedIn(false);
      setToken(null);
      return true
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        console.error(e.response?.data?.message);
      } else {
        console.error("予期しないエラー", e);
      }
      return false;
    }
  }

  useEffect(() => {
    const rehydrateToken = async () => {
      try {
        const res = await api.post('/auth/refresh');
        setToken(res.data.access_token);
        setIsLoggedIn(true);
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error('[rehydrateToken] Response:', error.response?.data);
          console.error('[rehydrateToken] Status:', error.response?.status);
        }
        setToken(null);
        setIsLoggedIn(false);
      } finally {
        setIsRehydrating(false);
      }
    };
    rehydrateToken();
  }, []);

  useEffect(() => {
    const interceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url?.includes('/auth/login')
          && !originalRequest.url?.includes('/auth/refresh')

        ) {
          originalRequest._retry = true;
          try {
            const res = await api.post(
              '/auth/refresh',
              {},
            );

            const accessToken = res.data.access_token;
            setToken(accessToken);

            api.defaults.headers.common.Authorization =
              `Bearer ${accessToken}`;

            return api(originalRequest);
          } catch (e) {
            setIsLoggedIn(false);
            setToken(null);
            console.log(e);
            logout();
          }
        }
        return Promise.reject(error);
      }
    );
    return () => {
      api.interceptors.response.eject(interceptor);
    };
  }, []);



  if (isRehydrating) {
    return null;
  }

  return (
    <AuthContext.Provider value={{ login, logout, isLoggedIn, token, errorMessageFromServer, sendResetEmailAndComplete, canResetPassword, verifyPasswordResetLink, validateAccessToken }}>
      {children}
    </AuthContext.Provider>
  );
};