import axios from "axios";
import crypto from "crypto";
import hmac from "crypto-js/hmac-sha512";
import { Application } from "express";

const randomCharts = (length: number): string => {
  let result = "";
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
};

const generateSignedPayload = (
  payload: string
): { nonce: string; timestamp: number; signature: string } => {
  const timestamp = Date.now();
  const nonce = randomCharts(32);
  const payload_to_sign = `${timestamp}\n${nonce}\n${payload}\n`;
  const signature = hmac(
    payload_to_sign,
    process.env.BINANCE_SECRET_API_KEY || ""
  )
    .toString()
    .toUpperCase();

  return { nonce, timestamp, signature };
};

const verifyWebhookSignature = async (
  binancePayTimestamp: string,
  binancePayNonce: string,
  bianacePaySignature: string,
  data: any
): Promise<boolean> => {
  console.log("Verifying Signature...");
  const payload = `${binancePayTimestamp}\n${binancePayNonce}\n${JSON.stringify(
    data
  )}`;
  const publicKey = await getPubKey();
  console.log("PublicKey: ", publicKey);

  const decodedSignature = Buffer.from(bianacePaySignature, "base64");

  const verify = crypto.createVerify("SHA256");
  verify.write(payload);
  verify.end();

  return await verify.verify(publicKey, decodedSignature);
};

const getPubKey = async (): Promise<string> => {
  const { nonce, timestamp, signature } = generateSignedPayload(
    JSON.stringify({})
  );
  const result = await axios.post(
    "https://bpay.binanceapi.com/binancepay/openapi/certificates",
    {},
    {
      headers: {
        "BinancePay-Certificate-SN": process.env.BINANCE_API_KEY,
        "Content-Type": "application/json;charset=utf-8",
        "BinancePay-Timestamp": timestamp,
        "BinancePay-Nonce": nonce,
        "BinancePay-Signature": signature,
      },
    }
  );

  return result.data.data[0].certPublic;
};

export const loadWebHookEndpoints = (app: Application): void => {
  app.post("/binance/order/notification", async (req, res) => {
    const verified = await verifyWebhookSignature(
      req.headers["binancepay-timestamp"] as string,
      req.headers["binancepay-nonce"] as string,
      req.headers["binancepay-signature"] as string,
      req.body
    );

    console.log(
      "********************BINANCE WEBHOOK CALL*******************",
      req.body
    );
    if (verified) {
      return res.status(200).send({
        returnCode: "SUCCESS",
        returnMessage: null,
      });
    } else {
      return res
        .status(401)
        .send({ returnCode: "ERROR", returnMessage: "Not authorized" });
    }
  });
};
