import http from 'k6/http';

const endpoint = __ENV.CHAOS_K6_URL;

export default function () {
  const result = http.get(endpoint);
}
