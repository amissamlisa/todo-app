import type { AxiosInstance } from "axios";
import type { RegistrationFormType } from "../types/registrationForm";
import type { AuthMessageResponse, AuthTokenResponse } from "../types/authApiContract";

export const registerAccount = async (api: AxiosInstance, body: RegistrationFormType): Promise<void> => {
  await api.post<AuthMessageResponse>("/api/auth/registration", {
    ...body,
    confirmation_password: body.confirmationPassword,
  });
};

export const loginRequest = async (api: AxiosInstance, email: string, password: string): Promise<string> => {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  const response = await api.post<AuthTokenResponse>(
    "/api/auth/login",
    params,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data.access_token;
};

export const logoutRequest = async (api: AxiosInstance): Promise<void> => {
  await api.delete<AuthMessageResponse>("/api/auth/logout", {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export const sendPasswordResetEmailRequest = async (api: AxiosInstance, email: string): Promise<void> => {
  await api.post<AuthMessageResponse>("/api/auth/password-reset/request", { email });
};

export const verifyPasswordResetLinkRequest = async (api: AxiosInstance, token: string): Promise<void> => {
  await api.get<AuthMessageResponse>("/api/auth/password-reset/verification", { params: { token } });
};

export const resetPasswordRequest = async (api: AxiosInstance, password: string, token: string | null): Promise<void> => {
  await api.put<AuthMessageResponse>("/api/auth/password-reset", {
    password,
    token,
  });
};

export const refreshAccessTokenRequest = async (api: AxiosInstance): Promise<string> => {
  const response = await api.post<AuthTokenResponse>("/api/auth/refresh", {});
  return response.data.access_token;
};
