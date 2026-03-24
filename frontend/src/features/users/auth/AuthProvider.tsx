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

let authRestorePromise: Promise<string | null> | null = null;

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [token, setToken] = useState<string | null>(null);
  const [loginErrorMessageFromServer, setLoginErrorMessageFromServer] = useState<string | null>(null);
  const [isRehydrating, setIsRehydrating] = useState(true);

  useEffect(() => {
    if (token) {
      api.defaults.headers.common.Authorization = `Bearer ${token}`;
    }
    else {
      delete api.defaults.headers.common.Authorization;
    }
  }, [token]);

  const login = async (email: string, password: string): Promise<void> => {
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
      const accessToken = response.data.access_token as string;
      setToken(accessToken);
    }
    catch (err) {
      if (axios.isAxiosError(err)) {
        if (err.response?.data?.error_code === "INVALID_PASSWORD_OR_EMAIL") {
          setLoginErrorMessageFromServer("メールアドレスまたはパスワードが正しくありません");
        } else {
          setLoginErrorMessageFromServer("ログインに失敗しました");
        }
      }
      else {
        console.error("Unexpected error", err);
      }
      setToken(null);
    }
  }

  const logout = async (): Promise<void> => {
    try {
      await api.delete(
        '/auth/logout',
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
    }
    catch (err) {
      console.log("logout error", err);
    }
    finally {
      setToken(null);
    }
  };

  const clearLoginErrorMessage = (): void => {
    setLoginErrorMessageFromServer(null);
  }

  const sendResetEmailAndComplete = async (email: string): Promise<void> => {
    try {
      await api.post(
        '/auth/password-reset/request',
        {
          email: email,
        }
      );
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const errorCode = err.response?.data?.error_code;
        const errorMessage = err.response?.data?.error_message;
        console.error(errorCode + " " + errorMessage);
      } else {
        console.error("Unexpected error", err);
      }
    }
  }
  const verifyPasswordResetLink = async (token: string): Promise<void> => {
    try {
      await api.get("/auth/password-reset/verification", { params: { token } })
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const errorCode = err.response?.data?.error_code;
        const errorMessage = err.response?.data?.error_message;
        console.error(errorMessage);
        throw new Error(errorCode || "UNKNOWN_ERROR");
      } else {
        console.error("Unexpected error", err);
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
      setToken(null);
      return true
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        console.error(err.response?.data?.message);
      } else {
        console.error("Unexpected error", err);
      }
      return false;
    }
  }

  useEffect(() => {
    const restoreAccessToken = async () => {
      try {
        if (!authRestorePromise) {
          authRestorePromise = (async () => {
            try {
              const res = await api.post('/auth/refresh');
              return res.data.access_token as string;
            } catch (err) {
              if (axios.isAxiosError(err)) {
                console.error('[restoreAccessToken] Response:', err.response?.data);
                console.error('[restoreAccessToken] Status:', err.response?.status);
              }
              return null;
            }
          })();
        }

        const restoredAccessToken = await authRestorePromise;
        if (restoredAccessToken) {
          setToken(restoredAccessToken);
          api.defaults.headers.common.Authorization = `Bearer ${restoredAccessToken}`;
        } else {
          setToken(null);
        }
      } finally {
        setIsRehydrating(false);
      }
    };
    restoreAccessToken();
  }, []);

  useEffect(() => {
    const interceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (!originalRequest) {
          return Promise.reject(error);
        }

        const requestUrl = String(originalRequest.url ?? "");
        const shouldSkipRefresh =
          requestUrl.includes('/auth/login') ||
          requestUrl.includes('/auth/refresh') ||
          requestUrl.includes('/auth/logout');

        if (error.response?.status === 401 && !originalRequest._retry && !shouldSkipRefresh) {
          originalRequest._retry = true;
          try {
            const res = await api.post('/auth/refresh', {});
            const accessToken = res.data.access_token as string;
            setToken(accessToken);

            originalRequest.headers = originalRequest.headers ?? {};
            originalRequest.headers.Authorization = `Bearer ${accessToken}`;
            return api(originalRequest);
          } catch (err) {
            console.log('refresh failed', err);
            setToken(null);
            logout();
            return Promise.reject(error);
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
  else {
    return (
      <AuthContext.Provider value={{ login, logout, token, loginErrorMessageFromServer, sendResetEmailAndComplete, canResetPassword, verifyPasswordResetLink, clearLoginErrorMessage, api, isRehydrating }}>
        {children}
      </AuthContext.Provider>
    );
  }
};