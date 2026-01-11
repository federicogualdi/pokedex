import http from 'k6/http';
import { check, group, sleep } from 'k6';

// =======================
// Config via env vars
// =======================
// Example: k6 run -e BASE_URL=http://localhost:8000 loadtest/pokedex.k6.js
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

// Pokemon name list
const POKEMON_NAMES = (__ENV.POKEMON_NAMES || 'pikachu,charizard,mewtwo,bulbasaur,squirtle,eevee')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);

// helper: pick random pokemon
function pickName() {
  return POKEMON_NAMES[Math.floor(Math.random() * POKEMON_NAMES.length)];
}

// =======================
// Scenari (2 endpoint separati)
// =======================
export const options = {
  scenarios: {
    pokemon_plain: {
      executor: 'ramping-vus',
      exec: 'hitPlain',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 10 },
        { duration: '30s', target: 10 },
        { duration: '10s', target: 0 },
      ],
      gracefulRampDown: '5s',
    },
    pokemon_translated: {
      executor: 'ramping-vus',
      exec: 'hitTranslated',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 5 },
        { duration: '30s', target: 5 },
        { duration: '10s', target: 0 },
      ],
      gracefulRampDown: '5s',
    },
  },

  // Soglie (fallisce il run se non rispettate)
  thresholds: {
    // tempo totale request (tutti gli endpoint)
    http_req_failed: ['rate<0.01'],         // <1% errori
    http_req_duration: ['p(95)<500'],       // 95% sotto 500ms (aggiusta per il tuo caso)

    // metriche per "gruppi"/tag
    'http_req_duration{endpoint:plain}': ['p(95)<400'],
    'http_req_duration{endpoint:translated}': ['p(95)<800'],
  },
};

// =======================
// Funzioni scenario
// =======================
export function hitPlain() {
  const name = pickName();
  const url = `${BASE_URL}/api/pokemon/${encodeURIComponent(name)}`;

  group('GET /api/pokemon/{name}', () => {
    const res = http.get(url, { tags: { endpoint: 'plain' } });

    check(res, {
      'status is 200': (r) => r.status === 200,
      'has pokemon.name': (r) => {
        try {
          return r.json('pokemon.name') != null;
        } catch (_) {
          return false;
        }
      },
    });

    sleep(0.2);
  });
}

export function hitTranslated() {
  const name = pickName();
  const url = `${BASE_URL}/api/pokemon/translated/${encodeURIComponent(name)}`;

  group('GET /api/pokemon/translated/{name}', () => {
    const res = http.get(url, { tags: { endpoint: 'translated' } });

    check(res, {
      'status is 200': (r) => r.status === 200,
      'has pokemon.description': (r) => {
        try {
          return (r.json('pokemon.description') || '').length > 0;
        } catch (_) {
          return false;
        }
      },
    });

    sleep(0.2);
  });
}
