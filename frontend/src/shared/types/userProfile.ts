export type UserProfileProps = { 
  username: string; 
  email: string; 
  showUserInfo: boolean; 
  setShowUserInfo: (show: boolean) => void; 
};