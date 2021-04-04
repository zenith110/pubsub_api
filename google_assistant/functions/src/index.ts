import * as functions from "firebase-functions";
import fetch from "node-fetch";
import {
  dialogflow,
  SimpleResponse,
  //   BaseicCard,
  //   Button,
  //   Image,
} from "actions-on-google";
const app = dialogflow({debug: true});
app.intent("get_pub_sub", async (conv, params) => {
  const data = await getSubData(params);
  if (data["status"] === "True") {
    conv.close(
        new SimpleResponse({
        text:
            "${data.sub_name} is currently on sale for" +
            "${data.price} from ${data.last_sale}",
        })
    );
  } else if (data["status"] === "False") {
    conv.close(
        new SimpleResponse({
            text: "${data.name} was last on on ${data.last_sale}" +
            "for ${data.price}",
        })
    );
  }
});

async function getSubData(params) {
  const url = "https://api.pubsub-api.dev/subs/?name=" + params;
  const page = await fetch(url);
  const object = await page.json()
  console.log(object)
  return {
    status: object["status"],
    sub_name: object["sub_name"],
    last_sale: object["last_sale"],
    price: object["price"],
  };
}
export const fulfillment = functions.https.onRequest(app);
