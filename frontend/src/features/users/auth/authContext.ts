import { createContext } from "react";
import type { AxiosInstance } from "axios";

export const AuthContext = createContext<{
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  isLoggedIn: boolean;
  token: string | null;
  loginErrorMessageFromServer: string | null;
  sendResetEmailAndComplete: (email: string) => Promise<void>;
  verifyPasswordResetLink: (token: string) => Promise<void>;
  canResetPassword: (password: string, token: string) => Promise<boolean>;
  validateAccessToken: () => boolean;
  clearLoginErrorMessage: () => void;
  api: AxiosInstance;
} | null>(null);