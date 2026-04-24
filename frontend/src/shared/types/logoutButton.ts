export type UseLogoutButtonParams = {
  onClick?: () => void | Promise<void>;
};

export type LogoutButtonProps = UseLogoutButtonParams & {
  className?: string;
};