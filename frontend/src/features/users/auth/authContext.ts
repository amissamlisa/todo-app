import { createContext } from "react";

export const AuthContext = createContext<{
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<boolean>;
  isLoggedIn: boolean;
  token: string | null;
  errorMessageFromServer: string | null;
  canSendResetPasswordEmail: (email: string) => Promise<void>;
  verifyPasswordResetLink: (token: string) => Promise<void>;
  canResetPassword: (password: string, token: string) => Promise<boolean>;
  validateAccessToken: () => boolean;
} | null>(null);