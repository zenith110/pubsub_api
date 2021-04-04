"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.fulfillment = void 0;
const functions = require("firebase-functions");
const node_fetch_1 = require("node-fetch");
const actions_on_google_1 = require("actions-on-google");
const app = actions_on_google_1.dialogflow({ debug: true });
app.intent("get_pub_sub", async (conv, params) => {
    const data = await getSubData(params);
    if (data["status"] === "True") {
        conv.close(new actions_on_google_1.SimpleResponse({
            text: "${data.sub_name} is currently on sale for" +
                "${data.price} from ${data.last_sale}",
        }));
    }
    else if (data["status"] === "False") {
        conv.close(new actions_on_google_1.SimpleResponse({
            text: "${data.name} was last on on ${data.last_sale}" +
                "for ${data.price}",
        }));
    }
});
async function getSubData(params) {
    const url = "https://api.pubsub-api.dev/subs/?name=" + params;
    const page = await node_fetch_1.default(url);
    const object = await page.json();
    console.log(object);
    return {
        status: object["status"],
        sub_name: object["sub_name"],
        last_sale: object["last_sale"],
        price: object["price"],
    };
}
exports.fulfillment = functions.https.onRequest(app);
//# sourceMappingURL=index.js.map