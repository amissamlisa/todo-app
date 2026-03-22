import { memo } from "react";
import { Incomplete } from "./Incomplete";

export const ServerConnectionIncomplete = memo(() => {
  return (
    <Incomplete
      title="サーバー接続失敗"
      message="サーバーに接続できません。復旧後に再度アクセスしてください。"
      hasLogoutButton={false}
      hasButton={false}
    />
  );
});