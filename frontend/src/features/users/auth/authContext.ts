import { createContext } from "react";
import type { AxiosInstance } from "axios";

export const AuthContext = createContext<{
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  token: string | null;
  loginErrorMessageFromServer: string | null;
  sendPasswordResetEmail: (email: string) => Promise<void>;
  verifyPasswordResetLink: (token: string) => Promise<void>;
  isRehydrating: boolean;
  canResetPassword: (password: string, token: string) => Promise<boolean>;
  clearLoginErrorMessage: () => void;
  api: AxiosInstance;
} | null>(null);