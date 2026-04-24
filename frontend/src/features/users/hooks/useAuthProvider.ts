import { useCallback, useEffect, useState } from "react";
import axios, { type AxiosInstance } from "axios";
import {
  loginRequest,
  logoutRequest,
  refreshAccessTokenRequest,
  resetPasswordRequest,
  sendPasswordResetEmailRequest,
  verifyPasswordResetLinkRequest,
} from "../api/authApi";

let authRestorePromise: Promise<string | null> | null = null;

export const useAuthProvider = (api: AxiosInstance) => {
  const [token, setToken] = useState<string | null>(null);
  const [loginErrorMessageFromServer, setLoginErrorMessageFromServer] = useState<string | null>(null);
  const [isRehydrating, setIsRehydrating] = useState(true);

  useEffect(() => {
    if (token) {
      api.defaults.headers.common.Authorization = `Bearer ${token}`;
    } else {
      delete api.defaults.headers.common.Authorization;
    }
  }, [token, api]);

  const login = async (email: string, password: string): Promise<void> => {
    try {
      const accessToken = await loginRequest(api, email, password);
      setToken(accessToken);
      setLoginErrorMessageFromServer(null);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (err.response?.data?.error_code === "INVALID_PASSWORD_OR_EMAIL") {
          setLoginErrorMessageFromServer("メールアドレスまたはパスワードが正しくありません");
        } else {
          setLoginErrorMessageFromServer("ログインに失敗しました");
        }
      } else {
        console.error("Unexpected error", err);
      }
      setToken(null);
    }
  };

  const logout = useCallback(async (): Promise<void> => {
    try {
      await logoutRequest(api);
    } catch (err) {
      console.log("logout error", err);
    } finally {
      setToken(null);
    }
  }, [api]);

  const clearLoginErrorMessage = (): void => {
    setLoginErrorMessageFromServer(null);
  };

  const sendPasswordResetEmail = async (email: string): Promise<void> => {
    try {
      await sendPasswordResetEmailRequest(api, email);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const errorCode = err.response?.data?.error_code;
        const errorMessage = err.response?.data?.error_message;
        console.error(errorCode + " " + errorMessage);
      } else {
        console.error("Unexpected error", err);
      }
      throw err;
    }
  };

  const verifyPasswordResetLink = async (tokenValue: string): Promise<void> => {
    try {
      await verifyPasswordResetLinkRequest(api, tokenValue);
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        const errorCode = err.response?.data?.error_code;
        const errorMessage = err.response?.data?.error_message;
        console.error(errorMessage);
        throw new Error(errorCode || "UNKNOWN_ERROR");
      }
      console.error("Unexpected error", err);
      throw new Error("UNKNOWN_ERROR");
    }
  };

  const canResetPassword = async (password: string, tokenValue: string | null): Promise<boolean> => {
    try {
      await resetPasswordRequest(api, password, tokenValue);
      setToken(null);
      return true;
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        console.error(err.response?.data?.message);
      } else {
        console.error("Unexpected error", err);
      }
      return false;
    }
  };

  useEffect(() => {
    const restoreAccessToken = async () => {
      try {
        if (!authRestorePromise) {
          authRestorePromise = (async () => {
            try {
              const accessToken = await refreshAccessTokenRequest(api);
              return accessToken;
            } catch (err) {
              if (axios.isAxiosError(err)) {
                console.error("[restoreAccessToken] Response:", err.response?.data);
                console.error("[restoreAccessToken] Status:", err.response?.status);
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
  }, [api, logout]);

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
          requestUrl.includes("/auth/login") ||
          requestUrl.includes("/auth/refresh") ||
          requestUrl.includes("/auth/logout");

        if (error.response?.status === 401 && !originalRequest._retry && !shouldSkipRefresh) {
          originalRequest._retry = true;
          try {
            const accessToken = await refreshAccessTokenRequest(api);
            setToken(accessToken);

            originalRequest.headers = originalRequest.headers ?? {};
            originalRequest.headers.Authorization = `Bearer ${accessToken}`;
            return api(originalRequest);
          } catch (err) {
            console.log("refresh failed", err);
            setToken(null);
            await logout();
            return Promise.reject(error);
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.response.eject(interceptor);
    };
  }, [api, logout]);

  return {
    login,
    logout,
    token,
    loginErrorMessageFromServer,
    sendPasswordResetEmail,
    canResetPassword,
    verifyPasswordResetLink,
    clearLoginErrorMessage,
    isRehydrating,
  };
};
