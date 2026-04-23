import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import type { PasswordResetType } from "../types/passwordReset";

export const usePasswordResetForm = () => {
  const { canResetPassword, verifyPasswordResetLink } = useAuth();
  const navigate = useNavigate();
  const search = useLocation().search;
  const queryParams = new URLSearchParams(search);
  const token = queryParams.get("token");
  const [isVerifying, setIsVerifying] = useState(true);
  const [isValidToken, setIsValidToken] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const verifyPasswordResetToken = async () => {
      if (token) {
        try {
          await verifyPasswordResetLink(token);
          setIsValidToken(true);
        } catch (err: unknown) {
          const errorCode = (err as Error).message;
          switch (errorCode) {
            case "INVALID_LINK_ERROR":
              navigate("/not-found", { replace: true });
              break;
            case "EXPIRED_LINK_ERROR":
              navigate("/password-reset-incomplete", { replace: true });
              break;
            default:
              navigate("/password-reset-incomplete", { replace: true });
          }
        } finally {
          setIsVerifying(false);
        }
      } else {
        navigate("/not-found", { replace: true });
      }
    };

    verifyPasswordResetToken();
  }, [token, verifyPasswordResetLink, navigate]);

  const handlePasswordReset = async (data: PasswordResetType) => {
    if (token === null) {
      navigate("/password-reset-incomplete", { replace: true });
      return;
    }

    setIsLoading(true);
    const isReset = await canResetPassword(data.password, token);
    if (isReset) {
      navigate("/password-reset-complete", { replace: true });
    } else {
      navigate("/password-reset-incomplete", { replace: true });
    }
  };

  return {
    isVerifying,
    isValidToken,
    isLoading,
    handlePasswordReset,
  };
};
