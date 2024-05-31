import {
  ConnectButton,
  useCurrentAccount,
  useSignPersonalMessage,
} from "@mysten/dapp-kit";
import { useState } from "react";

export function UseSignPersonal() {
  const { mutate: signPersonalMessage } = useSignPersonalMessage();
  const [message, setMessage] = useState("hello, World!");
  const [signature, setSignature] = useState("");
  const currentAccount = useCurrentAccount();

  return (
    <div style={{ padding: 20 }}>
      <ConnectButton />
      {currentAccount && (
        <>
          <div>
            <label>
              Message:{" "}
              <input
                type="text"
                value={message}
                onChange={(ev) => setMessage(ev.target.value)}
              />
            </label>
          </div>
          <button
            onClick={() => {
              signPersonalMessage(
                {
                  message: new TextEncoder().encode(message),
                },
                {
                  onSuccess: (result) => setSignature(result.signature),
                },
              );
            }}
          >
            Sign message
          </button>
          <div>Signature: {signature}</div>
        </>
      )}
    </div>
  );
}
