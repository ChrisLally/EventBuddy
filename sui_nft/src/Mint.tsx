import React, { useState, useCallback, useEffect } from "react";
import { useSignTransaction, useSuiClient } from "@mysten/dapp-kit";
import { SuiTransactionBlockResponseOptions } from "@mysten/sui/client";
import { Transaction } from "@mysten/sui/transactions";
import { CONTRACT, imageUrl } from "../lib/constants";
import { bcs } from "@mysten/sui/bcs";

// A helper to execute transactions by:
// 1. Signing them using the wallet
// 2. Executing them using the rpc provider
export function useTransactionExecution() {
  const provider = useSuiClient();

  // sign transaction from the wallet
  const { mutateAsync: signTransaction } = useSignTransaction();

  const signAndExecute = async ({
    tx,
    options = { showEffects: true, showObjectChanges: true },
  }: {
    tx: Transaction;
    options?: SuiTransactionBlockResponseOptions | undefined;
  }) => {
    const signedTx = await signTransaction({ transaction: tx });

    const res = await provider.executeTransactionBlock({
      transactionBlock: signedTx.bytes,
      signature: signedTx.signature,
      options,
    });

    const status = res.effects?.status?.status === "success";

    if (status) return res;
    else throw new Error("Transaction execution failed.");
  };

  return { signAndExecute };
}

// Helper function to convert string to Uint8Array
function stringToUint8Array(str: string): Uint8Array {
  return new TextEncoder().encode(str);
}

// Hook to mint tokens
export function useMintToken() {
  const { signAndExecute } = useTransactionExecution();
  const [nftObjectId, setNftObjectId] = useState<string | undefined>(undefined);
  const mintToken = async ({
    name,
    description,
    url,
  }: {
    name: string;
    description: string;
    url: string;
  }) => {
    try {
      const tx = new Transaction();
      tx.moveCall({
        target: `${CONTRACT}::ethos_example_nft::mint_to_sender`,
        arguments: [
          tx.pure(bcs.vector(bcs.U8).serialize(stringToUint8Array(name))),
          tx.pure(
            bcs.vector(bcs.U8).serialize(stringToUint8Array(description)),
          ),
          tx.pure(bcs.vector(bcs.U8).serialize(stringToUint8Array(url))),
        ],
      });

      tx.setGasBudget(20000000);

      const response = await signAndExecute({
        tx,
        options: { showEffects: true, showObjectChanges: true },
      });

      if (response?.objectChanges) {
        const createdObject = response.objectChanges.find(
          (e) => e.type === "created",
        );
        if (createdObject && "objectId" in createdObject) {
          setNftObjectId(createdObject.objectId);
        }
      }
    } catch (error) {
      console.log(">>>>>", error);
    }
  };

  const reset = useCallback(() => {
    setNftObjectId(undefined);
  }, []);

  useEffect(() => {
    reset();
  }, [reset]);

  return { mintToken, nftObjectId, reset };
}

// Type for SuccessMessage props
interface SuccessMessageProps {
  reset: () => void;
  children: React.ReactNode;
}
const MintNFT = () => {
  const { mintToken, nftObjectId, reset } = useMintToken();
  const [address, setAddress] = useState<string>("");

  const mint = () => {
    mintToken({
      name: "Event Buddy NFT",
      //"Builder Demo Days. Hosted by Cartesi! Rated 5 Out of 5!"
      //"Builder Demo Days. Hosted by Cartesi! Rated 5 Out of 5!",
      description:
        "Builder Demo Days. Hosted by Cartesi! June 1, 2024 10 AM to 5 PM. 2930 E 12th Street Austin, TX. Enjoy the event!",
      url: imageUrl,
    });
  };

  // SuccessMessage Component
  const SuccessMessage: React.FC<SuccessMessageProps> = ({
    reset,
    children,
  }) => (
    <div className="success-message">
      <p>{children}</p>
      <button onClick={reset}>Reset</button>
    </div>
  );

  // Component that uses the mintToken hook

  return (
    <div className="flex flex-col gap-6">
      <input
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />{" "}
      <button
        className="mx-auto px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        onClick={mint}
      >
        Mint an NFT
      </button>
      <button
        onClick={async () => {
          // const details = await provider.getObject(obj.objectId);
          // const imageUrl = details.fields.url; // Adjust according to your schema

          console.log(imageUrl);
        }}
      >
        Fetch Image
      </button>
      {nftObjectId && (
        <SuccessMessage reset={reset}>
          NFT minted successfully! NFT Object ID: {nftObjectId}
          <a
            href={`https://explorer.sui.io/objects/${nftObjectId}?network=testnet`}
            target="_blank"
            rel="noreferrer"
            className="underline font-blue-600"
          >
            View Your NFT on the TestNet Explorer
          </a>
        </SuccessMessage>
      )}
    </div>
  );
};

export default MintNFT;
