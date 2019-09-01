import {Dictionary} from 'vue-router/types/router';

export const backendBaseUrl = "http://localhost:8000";
export const backendUrls = {
  login: backendBaseUrl + "/user/login",
  getLayersSchemas: backendBaseUrl + "/user/layers_schemas",
};
export const JSONTypes = ['string', 'integer', 'number', 'array', 'boolean', 'object'];
export const JSONDefaults: Dictionary<any> = {
  'string': "",
  "integer": 0,
  "number": 0.0,
  "array": [],
  "boolean": false,
  "object": {}
};