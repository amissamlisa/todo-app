import { useNavigate } from "react-router-dom";
import type { RegistrationFormType } from "../types/registrationForm";

export const useAccountRegistrationForm = () => {
  const navigate = useNavigate();

  const handleAccountRegistrationSubmit = (data: RegistrationFormType) => {
    navigate("/user-registration/confirm", { state: data, replace: true });
  };

  const handleNavigateToTop = () => {
    navigate("/", { replace: true });
  };

  return {
    handleAccountRegistrationSubmit,
    handleNavigateToTop,
  };
};
