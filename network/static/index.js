import ApiHandler from "./api_handler.js"

const test = new ApiHandler("likes_api/1", {})
console.log(ApiHandler, test.Get("likes_api/1"));