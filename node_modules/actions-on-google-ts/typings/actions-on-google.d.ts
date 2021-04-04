/**
 * Copyright 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * The Actions on Google client library.
 * https://developers.google.com/actions/
 */

export { AssistantApp, AssistantAppOptions, RequestHandler, SessionStartedFunction, State } from './assistant-app';
export { ActionsSdkApp, ActionsSdkAppOptions } from './actions-sdk-app';
export { ApiAiApp, ApiAiAppOptions } from './api-ai-app';
export { default as Transactions } from './transactions';
export { default as Responses } from './response-builder';
// Backwards compatibility
export { AssistantApp as Assistant } from './assistant-app';
export { ActionsSdkApp as ActionsSdkAssistant } from './actions-sdk-app';
export { ApiAiApp as ApiAiAssistant } from './api-ai-app';
