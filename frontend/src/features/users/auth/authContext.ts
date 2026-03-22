import { createContext } from "react";
import type { AxiosInstance } from "axios";

export const AuthContext = createContext<{
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<boolean>;
  isLoggedIn: boolean;
  token: string | null;
  errorMessageFromServer: string | null;
  sendResetEmailAndComplete: (email: string) => Promise<void>;
  verifyPasswordResetLink: (token: string) => Promise<void>;
  canResetPassword: (password: string, token: string) => Promise<boolean>;
  validateAccessToken: () => boolean;
  clearErrorMessage: () => void;
  api: AxiosInstance;
} | null>(null);